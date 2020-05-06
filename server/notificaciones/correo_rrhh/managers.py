from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *
from xhtml2pdf import pisa
from ...configuraciones.empresa.managers import *
from ...personal.persona.managers import *
from ...usuarios.ajustes.models import *
from ..correo.models import *


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xhtml2pdf import pisa

import os.path


class Report:
    def html_to_pdf(self, sourceHtml, nombre):
        outputFilename = 'server/common/resources/downloads/correo/' + nombre

        resultFile = open(outputFilename, "w+b")
        pisaStatus = pisa.CreatePDF(
            sourceHtml,
            dest=resultFile)
        resultFile.close()

        return pisaStatus.err

global report
report = Report()
global image_report

image_report = "../server/common/resources/images/logos/elfec.jpg"

class CorreorrhhManager(SuperManager):

    def __init__(self, db):
        super().__init__(Correorrhh, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Correo rrhh.",
                     fecha=fecha, tabla="cb_notificaciones_correos", identificador=a.id)
        super().insert(b)
        return a


    def delete(self, key, state):

        obj = self.db.query(Correorrhh).filter(Correorrhh.fkpersona == key).all()

        for ob in obj:
            ob.enabled = state
            self.db.commit()

        return ob


    def envio_reporte_correo(self):
        from ...asistencia.asistenciapersonal.managers import AsistenciaManager

        correos = []
        envio = True
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(ServidorCorreo.id == 1).first()

        dia = calendar.day_name[datetime.now().weekday()]

        if dia == "Monday":
            envio = server.lunes
        elif dia == "Tuesday":
            envio = server.martes
        elif dia == "Wednesday":
            envio = server.miercoles
        elif dia == "Thursday":
            envio = server.jueves
        elif dia == "Friday":
            envio = server.viernes
        elif dia == "Saturday":
            envio = server.sabado
        elif dia == "Sunday":
            envio = server.domingo

        if envio:

            empresa = EmpresaManager(self.db).obtener_empresa()
            horarios = AsistenciaManager(self.db).listar_por_dia()
            nombredoc = CorreoManager(self.db).reporte_correo(empresa,horarios)

            for correo in server.correos:
                correos.append(correo.persona.empleado[0].email)

            if len(correos)> 0:

                # Iniciamos los parámetros del script
                remitente = "<"+server.correo+">"
                destinatarios = correos
                asunto = 'Marcaciones Diarias ' + str(empresa.nombre)
                cuerpo = "Buenos dias Estimados"+ "\n" + "Adjunto reporte de marcaciones diarias del personal"+ "\n" + "Saludos"
                ruta_adjunto = './server/common/resources/downloads/correo/'
                nombre_adjunto = nombredoc
                # Creamos el objeto mensaje
                mensaje = MIMEMultipart()
                # Establecemos los atributos del mensaje
                mensaje['From'] = remitente
                mensaje['To'] = ", ".join(destinatarios)
                mensaje['Subject'] = asunto
                # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
                mensaje.attach(MIMEText(cuerpo, 'plain'))
                # Abrimos el archivo que vamos a adjuntar
                archivo_adjunto = open(ruta_adjunto + nombre_adjunto, 'rb')
                # Creamos un objeto MIME base
                adjunto_MIME = MIMEBase('application', 'octet-stream')
                # Y le cargamos el archivo adjunto
                adjunto_MIME.set_payload((archivo_adjunto).read())
                # Codificamos el objeto en BASE64
                encoders.encode_base64(adjunto_MIME)
                # Agregamos una cabecera al objeto
                adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
                # Y finalmente lo agregamos al mensaje
                mensaje.attach(adjunto_MIME)
                # Creamos la conexión con el servidor
                sesion_smtp = smtplib.SMTP(server.servidor)
                # Ciframos la conexión
                # Iniciamos sesión en el servidor
                # Convertimos el objeto mensaje a texto
                texto = mensaje.as_string()
                # Enviamos el mensaje
                sesion_smtp.sendmail(remitente, destinatarios, texto)
                # Cerramos la conexión
                sesion_smtp.quit()


    def reporte_correo(self,empresa,horarios):
        fecha_actual = datetime.now(pytz.timezone('America/La_Paz'))
        detalle = ""
        codigo = ""
        nombre = ""
        fecha = ""
        horaentrada = ""
        marcacion = ""
        correos = []
        objetoempresa = EmpresaManager(self.db).obtener_empresa()

        if objetoempresa:
            if objetoempresa.foto1:
                logoempresa = objetoempresa.foto1
            else:
                logoempresa = "/resources/images/sinImagen.jpg"

        else:
            logoempresa = "/resources/images/sinImagen.jpg"


        for hr in horarios:

            codigo = hr.persona.empleado[0].codigo
            nombre = hr.nombrecompleto
            fecha = hr.fecha.strftime("%d/%m/%Y")
            horaentrada = hr.entrada.strftime("%H:%M")
            if hr.mentrada:
                marcacion = hr.mentrada.strftime("%H:%M:%S")
            else:
                marcacion = "-------"

            detalle = detalle + "<tr style='font-size: 12px; border: 0px; '>" \
                                "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(codigo) + "</font></td>" \
                                "   <td colspan='6' style='border-right: 1px solid grey 'scope='colgroup'align='left'><font>" + str(nombre) + "</font></td>" \
                                "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(fecha) + "</font></td>" \
                                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(horaentrada) + "</font></td>" \
                                "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(marcacion) + "</font></td>" \
                                "</tr>"

        html = "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
               "<style>" \
               "   .border-own { border-left: 0px; border-right: 0px; }" \
               "   .border-own-l { border-right: 0px; }" \
               "   .border-own-r { border-left: 0px; }" \
               "   @page {size: letter portrait; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 772pt; height: 20pt; }}" \
               "</style>" \
               "<div class='container' style='font-size: 12px'>" \
               "   <div class='row'>" \
               "       <div class='col-md-4'>" \
               "           <img src='../server/common" + logoempresa + "' width='134' height='75'>" \
               "       </div>" \
               "   </div>" \
               "</div>"

        html += "<table style='padding: 4px; border: 1px solid grey' width='85%'>" \
                "<tr color='#ffffff' >" \
                "   <th colspan='15' scope='colgroup' align='left' style='background-color: #1976d2; font-size=4; color: white; margin-top: 4px'>REPORTE DE MARCACIONES</th>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='2' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Empresa: </strong></td>" \
                "   <td colspan='13' scope='colgroup'align='left'><font>" + str(empresa.nombre) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='2' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Fecha: </strong></td>" \
                "   <td colspan='13' scope='colgroup'align='left'><font>" + str(fecha_actual.strftime("%d/%m/%Y")) + "</font></td>" \
                "</tr>" \
                "<tr color='#ffffff' >" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Cod</th>" \
                "   <th colspan='6' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Nombre y Apellidos</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Fecha</th>" \
                "   <th colspan='3' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Hora Entrada</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Marcacion</th>" \
                "</tr>" \
                "" + detalle + "" \
                              "</table>" \
                              "</br>"

        nombre = "Marcaciones_" + str(fecha_actual.strftime("%d-%m-%Y")) + ".pdf"

        report.html_to_pdf(html, nombre)

        return nombre


    def notificar_ausencia(self,ausencia):
        correos = []
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(ServidorCorreo.id == 1).first()

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ausencia.fksuperior:
             correo = PersonaManager(self.db).obtener_correo(ausencia.fksuperior)
             correos.append(correo)

        if len(correos)> 0:

            # Iniciamos los parámetros del script
            remitente = "<"+server.correo+">"
            destinatarios = correos
            asunto = 'Solicitud de Ausencia :  ' + str(ausencia.persona.fullname)
            cuerpo = "Ha recibido la siguiente solicitud de Ausencia:"+ "\n" + "Por favor Ingrese al Sistema para validar: "+ str(ajuste.dominio) + "portal_ausencia"+ "\n" + "\n" + "Nro: "+ str(ausencia.id) + "\n" + "Persona: "+ str(ausencia.persona.fullname) + "\n" + "Tipo de Ausencia: "+ str(ausencia.tipoausencia.nombre) + "\n" + "Descripcion: "+ str(ausencia.descripcion) + "\n" + "Fecha Inicio: "+ str(ausencia.fechai.strftime("%d/%m/%Y")) + "\n" + "Fecha Fin: "+ str(ausencia.fechaf.strftime("%d/%m/%Y")) + "\n" + "Estado: "+ str(ausencia.estado) + "\n" + "\n" +  "Saludos"
            # Creamos el objeto mensaje
            mensaje = MIMEMultipart('alternative')
            # Establecemos los atributos del mensaje
            mensaje['From'] = remitente
            mensaje['To'] = ", ".join(destinatarios)
            mensaje['Subject'] = asunto
            # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            # Abrimos el archivo que vamos a adjuntar
            # Creamos un objeto MIME base
            # Creamos la conexión con el servidor
            sesion_smtp = smtplib.SMTP(server.servidor)
            # Ciframos la conexión
            # Convertimos el objeto mensaje a texto
            texto = mensaje.as_string()
            # Enviamos el mensaje
            sesion_smtp.sendmail(remitente, destinatarios, texto)
            # Cerramos la conexión
            sesion_smtp.quit()


    def notificar_ausencia_respuesta(self,ausencia):
        correos = []
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(ServidorCorreo.id == 1).first()

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ausencia.fksuperior:
             correo = PersonaManager(self.db).obtener_correo(ausencia.fksuperior)
             correos.append(correo)

        if ausencia.fkpersona:
             correo = PersonaManager(self.db).obtener_correo(ausencia.fkpersona)
             correos.append(correo)

        if len(correos)> 0:

            # Iniciamos los parámetros del script
            remitente = "<"+server.correo+">"
            destinatarios = correos
            asunto = 'Respuesta de Solicitud:  ' + str(ausencia.persona.fullname)
            cuerpo = "Ha recibido la siguiente Respuesta:"+ "\n" + "Estado: "+ str(ausencia.estado) + "\n" + "Mensaje: "+ str(ausencia.respuesta) + "\n" + "Visite el Portal del Empleado: "+ str(ajuste.dominio) + "portal_ausencia"+ "\n" + "\n" + "Nro: "+ str(ausencia.id) + "\n" + "Persona: "+ str(ausencia.persona.fullname) + "\n" + "Tipo de Ausencia: "+ str(ausencia.tipoausencia.nombre) + "\n" + "Descripcion: "+ str(ausencia.descripcion) + "\n" + "Fecha Inicio: "+ str(ausencia.fechai.strftime("%d/%m/%Y")) + "\n" + "Fecha Fin: "+ str(ausencia.fechaf.strftime("%d/%m/%Y")) + "\n" + "Estado: "+ str(ausencia.estado) + "\n" + "\n" +  "Saludos"
            # Creamos el objeto mensaje
            mensaje = MIMEMultipart('alternative')
            # Establecemos los atributos del mensaje
            mensaje['From'] = remitente
            mensaje['To'] = ", ".join(destinatarios)
            mensaje['Subject'] = asunto
            # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            # Abrimos el archivo que vamos a adjuntar
            # Creamos un objeto MIME base
            # Creamos la conexión con el servidor
            sesion_smtp = smtplib.SMTP(server.servidor)
            # Ciframos la conexión
            # Convertimos el objeto mensaje a texto
            texto = mensaje.as_string()
            # Enviamos el mensaje
            sesion_smtp.sendmail(remitente, destinatarios, texto)
            # Cerramos la conexión
            sesion_smtp.quit()


