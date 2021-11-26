from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *
from xhtml2pdf import pisa
from ...configuraciones.empresa.managers import *
from ...personal.persona.managers import *
from ...usuarios.ajustes.models import *
from ..correo_rrhh.models import *


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xhtml2pdf import pisa
import requests

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

class CorreoManager(SuperManager):

    def __init__(self, db):
        super().__init__(ServidorCorreo, db)


    def obtener_servidor(self):
        x = self.db.query(self.entity).filter(self.entity.id == 1).first()

        return  x

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Empresa.",
                     fecha=fecha, tabla="rrhh_empresa", identificador=a.id)
        super().insert(b)
        return a

    def update(self, diccionary):
        lista = []
        lista_dict = []
        for x in diccionary['correos']:
            try:
                if x['id']:
                    lista_dict.append(x)
            except Exception as e:
                print("")
            lista.append(x['fkpersona'])

        lista_filtrada = set(lista)

        for rep in lista_dict:
            lista_filtrada.remove(rep['fkpersona'])

        for lf in lista_filtrada:
            lista_dict.append(dict(fkpersona=lf))

        diccionary['correos'] = lista_dict

        objeto = CorreoManager(self.db).entity(**diccionary)
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico servidor.",
                     fecha=fecha, tabla="cb_notificaciones_servidor", identificador=a.id)
        super().insert(b)

        return a

    def update_hora(self, objeto,usuario,ip):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=usuario, ip=ip, accion="Modifico hora de correo.",
                     fecha=fecha, tabla="cb_notificaciones_correo", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, key, state):

        obj = self.db.query(Correos).filter(Correos.fkpersona == key).all()

        for ob in obj:
            ob.enabled = state
            self.db.commit()

        return ob

    def actualizacion_dias(self, key, state):
        id = 1
        obj = self.db.query(self.entity).get(id)

        if (key == 1):
            obj.lunes = state
        elif (key == 2):
            obj.martes = state
        elif (key == 3):
            obj.miercoles = state
        elif (key == 4):
            obj.jueves = state
        elif (key == 5):
            obj.viernes = state
        elif (key == 6):
            obj.sabado = state
        else:
            obj.domingo = state

        self.db.commit()
        return obj

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
                sesion_smtp = smtplib.SMTP(server.servidor,server.puerto)
                # Ciframos la conexión
                sesion_smtp.starttls()
                # Iniciamos sesión en el servidor
                sesion_smtp.login(server.correo, server.password)
                # Convertimos el objeto mensaje a texto
                texto = mensaje.as_string()
                # Enviamos el mensaje
                sesion_smtp.sendmail(remitente, destinatarios, texto)
                # Cerramos la conexión
                sesion_smtp.quit()
                print("correo enviado")

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
        autorizacion = ""
        aprobacion = ""

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(ServidorCorreo.id == 1).first()

        correo_rrhh = self.db.query(Correorrhh).filter(Correorrhh.enabled == True).all()



        if ausencia.persona.empleado[0].autorizacion:
            if ausencia.fkautorizacion:
                 correo = PersonaManager(self.db).obtener_correo(ausencia.fkautorizacion)
                 if correo:
                    correos.append(correo)

        elif ausencia.persona.empleado[0].aprobacion:
            if ausencia.fkaprobacion:
                correo = PersonaManager(self.db).obtener_correo(ausencia.fkaprobacion)
                if correo:
                    correos.append(correo)



        for _rrhh in correo_rrhh:
            correo = PersonaManager(self.db).obtener_correo(_rrhh.fkpersona)
            if correo:
                correos.append(correo)


        if ausencia.fkautorizacion:
            autorizacion = ausencia.autorizacion.fullname
        else:
            autorizacion = "------"

        if ausencia.fkaprobacion:
            aprobacion = ausencia.aprobacion.fullname
        else:
            aprobacion = "------"


        if len(correos)> 0:

            asunto = 'Solicitud de Ausencia :  ' + str(ausencia.persona.fullname)
            cuerpo = "Ha recibido la siguiente solicitud de Ausencia:" + \
                     "\n" + "Por favor Ingrese al Sistema para validar: " + str(ajuste.dominio) + "portal_ausencia" + \
                     "\n" + "\n" + "Nro: "+ str(ausencia.id) + \
                     "\n" + "Persona: "+ str(ausencia.persona.fullname) +\
                     "\n" + "Tipo de Ausencia: "+ str(ausencia.tipoausencia.nombre) + \
                     "\n" + "Descripcion: "+ str(ausencia.descripcion) +\
                     "\n" + "Fecha Inicio: "+ str(ausencia.fechai.strftime("%d/%m/%Y")) + \
                     "\n" + "Fecha Fin: "+ str(ausencia.fechaf.strftime("%d/%m/%Y")) + \
                     "\n" + "\n" + "Autorizado por: " + str(autorizacion)  + \
                     "\n" + "Estado: " + str(ausencia.estadoautorizacion) + \
                     "\n" + "Respuesta autorizacion: " + str(ausencia.respuestaautorizacion) + \
                     "\n" + "\n" + "Aprobado por: " + str(aprobacion) + \
                     "\n" + "Estado: " + str(ausencia.estadoaprobacion) + \
                     "\n" + "Respuesta aprobacion: "+ str(ausencia.respuestaaprobacion) + \
                     "\n" + "\n" +  "Saludos"

            CorreoManager(self.db).funcion_email(server, correos, asunto, cuerpo)

    def notificar_ausencia_respuesta_autorizacion(self,ausencia):
        correos = []
        autorizacion = ""
        aprobacion = ""
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(ServidorCorreo.id == 1).first()
        correo_rrhh = self.db.query(Correorrhh).filter(Correorrhh.enabled == True).all()

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()


        if ausencia.fkpersona:
             correo = PersonaManager(self.db).obtener_correo(ausencia.fkpersona)
             if correo:
                 correos.append(correo)

        for _rrhh in correo_rrhh:
            correo = PersonaManager(self.db).obtener_correo(_rrhh.fkpersona)
            if correo:
                correos.append(correo)

        if ausencia.estadoautorizacion == "Aceptado":

            if ausencia.persona.empleado[0].aprobacion:
                if ausencia.fkaprobacion:
                    correo = PersonaManager(self.db).obtener_correo(ausencia.fkaprobacion)
                    if correo:
                        correos.append(correo)

        if ausencia.fkautorizacion:
            autorizacion = ausencia.autorizacion.fullname
        else:
            autorizacion = "------"

        if ausencia.fkaprobacion:
            aprobacion = ausencia.aprobacion.fullname
        else:
            aprobacion = "------"

        if len(correos)> 0:
            asunto = 'Respuesta de Solicitud:  ' + str(ausencia.persona.fullname)
            cuerpo = "Visite el Portal del Empleado: "+ str(ajuste.dominio) + \
                     "portal_ausencia"+ \
                     "\n" + "\n" + "Nro: "+ str(ausencia.id) + \
                     "\n" + "Persona: "+ str(ausencia.persona.fullname) +\
                     "\n" + "Tipo de Ausencia: "+ str(ausencia.tipoausencia.nombre) + \
                     "\n" + "Descripcion: "+ str(ausencia.descripcion) +\
                     "\n" + "Fecha Inicio: "+ str(ausencia.fechai.strftime("%d/%m/%Y")) + \
                     "\n" + "Fecha Fin: "+ str(ausencia.fechaf.strftime("%d/%m/%Y")) + \
                     "\n" + "\n" + "Autorizado por: " + str(autorizacion)  + \
                     "\n" + "Estado: " + str(ausencia.estadoautorizacion) + \
                     "\n" + "Respuesta autorizacion: " + str(ausencia.respuestaautorizacion) + \
                     "\n" + "\n" + "Aprobado por: " + str(aprobacion) + \
                     "\n" + "Estado: " + str(ausencia.estadoaprobacion) + \
                     "\n" + "Respuesta aprobacion: "+ str(ausencia.respuestaaprobacion) + \
                     "\n" + "\n" +  "Saludos"
            # Creamos el objeto mensaje

            CorreoManager(self.db).funcion_email(server, correos,asunto,cuerpo)


    def notificar_ausencia_respuesta_aprobacion(self, ausencia):
        correos = []
        autorizacion = ""
        aprobacion = ""
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(
            ServidorCorreo.id == 1).first()
        correo_rrhh = self.db.query(Correorrhh).filter(Correorrhh.enabled == True).all()

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()


        if ausencia.fkpersona:
            correo = PersonaManager(self.db).obtener_correo(ausencia.fkpersona)
            if correo:
                correos.append(correo)

        for _rrhh in correo_rrhh:
            correo = PersonaManager(self.db).obtener_correo(_rrhh.fkpersona)
            if correo:
                correos.append(correo)


        if ausencia.persona.empleado[0].autorizacion:
            if ausencia.fkautorizacion:
                correo = PersonaManager(self.db).obtener_correo(ausencia.fkautorizacion)
                if correo:
                    correos.append(correo)

        if ausencia.fkautorizacion:
            autorizacion = ausencia.autorizacion.fullname
        else:
            autorizacion = "------"

        if ausencia.fkaprobacion:
            aprobacion = ausencia.aprobacion.fullname
        else:
            aprobacion = "------"

        if len(correos) > 0:
            asunto = 'Respuesta de Solicitud:  ' + str(ausencia.persona.fullname)
            cuerpo = "Visite el Portal del Empleado: "+ str(ajuste.dominio) + \
                     "portal_ausencia"+ "\n" + "\n" + "Nro: "+ str(ausencia.id) + "\n" + "Persona: "+ str(ausencia.persona.fullname) +\
                     "\n" + "Tipo de Ausencia: "+ str(ausencia.tipoausencia.nombre) + "\n" + "Descripcion: "+ str(ausencia.descripcion) +\
                     "\n" + "Fecha Inicio: "+ str(ausencia.fechai.strftime("%d/%m/%Y")) + "\n" + "Fecha Fin: "+ str(ausencia.fechaf.strftime("%d/%m/%Y")) + \
                     "\n" + "\n" + "Autorizado por: " + str(autorizacion)  + \
                     "\n" + "Estado: " + str(ausencia.estadoautorizacion) + \
                     "\n" + "Respuesta autorizacion: " + str(ausencia.respuestaautorizacion) + \
                     "\n" + "\n" + "Aprobado por: " + str(aprobacion) + \
                     "\n" + "Estado: " + str(ausencia.estadoaprobacion) + \
                     "\n" + "Respuesta aprobacion: "+ str(ausencia.respuestaaprobacion) + "\n" + "\n" +  "Saludos"
            # Creamos el objeto mensaje

            CorreoManager(self.db).funcion_email(server, correos, asunto, cuerpo)


    def notificar_vacacion(self,ausencia):
        correos = []
        autorizacion = ""
        aprobacion = ""
        persona = ""

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(ServidorCorreo.id == 1).first()

        correo_rrhh = self.db.query(Correorrhh).filter(Correorrhh.enabled == True).all()


        if ausencia.fkautorizacion:
             correo = PersonaManager(self.db).obtener_correo(ausencia.fkautorizacion)
             if correo:
                 correos.append(correo)

        for _rrhh in correo_rrhh:
            correo = PersonaManager(self.db).obtener_correo(_rrhh.fkpersona)
            if correo:
                correos.append(correo)

        if ausencia.fkautorizacion:
            autorizacion = ausencia.autorizacion.fullname
        else:
            autorizacion = "------"

        if ausencia.fkaprobacion:
            aprobacion = ausencia.aprobacion.fullname
        else:
            aprobacion = "------"

        if ausencia.fkpersona:
            persona = ausencia.persona.fullname
        else:
            persona = "Varias Personas"

        if len(correos)> 0:

            asunto = 'Solicitud de Vacacion :  ' + str(persona)
            cuerpo = "Ha recibido la siguiente solicitud de vacacion:" + "\n" + "Por favor Ingrese al Sistema para validar: " + str(
                ajuste.dominio) + "portal_ausencia" + \
                     "\n" + "\n" + "Nro: "+ str(ausencia.id) + \
                     "\n" + "Persona: "+ str(persona) +\
                     "\n" + "Tipo de Ausencia: "+ str(ausencia.tipovacacion.nombre) + \
                     "\n" + "Descripcion: "+ str(ausencia.descripcion) +\
                     "\n" + "Fecha Inicio: "+ str(ausencia.fechai.strftime("%d/%m/%Y")) + \
                     "\n" + "Fecha Fin: "+ str(ausencia.fechaf.strftime("%d/%m/%Y")) + \
                     "\n" + "\n" + "Autorizado por: " + str(autorizacion)  + \
                     "\n" + "Estado: " + str(ausencia.estadoautorizacion) + \
                     "\n" + "Respuesta autorizacion: " + str(ausencia.respuestaautorizacion) + \
                     "\n" + "\n" + "Aprobado por: " + str(aprobacion) + \
                     "\n" + "Estado: " + str(ausencia.estadoaprobacion) + \
                     "\n" + "Respuesta aprobacion: "+ str(ausencia.respuestaaprobacion) + \
                     "\n" + "\n" +  "Saludos"

            CorreoManager(self.db).funcion_email(server, correos, asunto, cuerpo)

    def notificar_vacacion_respuesta_autorizacion(self,ausencia):
        correos = []
        autorizacion = ""
        aprobacion = ""
        persona = ""
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(ServidorCorreo.id == 1).first()
        correo_rrhh = self.db.query(Correorrhh).filter(Correorrhh.enabled == True).all()

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()


        if ausencia.fkpersona:
             correo = PersonaManager(self.db).obtener_correo(ausencia.fkpersona)
             if correo:
                 correos.append(correo)

        for _rrhh in correo_rrhh:
            correo = PersonaManager(self.db).obtener_correo(_rrhh.fkpersona)
            if correo:
                correos.append(correo)

        if ausencia.estadoautorizacion == "Aceptado":
            if ausencia.fkpersona:
                if ausencia.persona.empleado[0].aprobacion:
                    if ausencia.fkaprobacion:
                        correo = PersonaManager(self.db).obtener_correo(ausencia.fkaprobacion)
                        if correo:
                            correos.append(correo)

        if ausencia.fkautorizacion:
            autorizacion = ausencia.autorizacion.fullname
        else:
            autorizacion = "------"

        if ausencia.fkaprobacion:
            aprobacion = ausencia.aprobacion.fullname
        else:
            aprobacion = "------"

        if ausencia.fkpersona:
            persona = ausencia.persona.fullname
        else:
            persona = "Varias Personas"

        if len(correos)> 0:
            asunto = 'Respuesta de Solicitud:  ' + str(persona)
            cuerpo = "Visite el Portal del Empleado: "+ str(ajuste.dominio) + \
                     "portal_ausencia"+ \
                     "\n" + "\n" + "Nro: "+ str(ausencia.id) + \
                     "\n" + "Persona: "+ str(persona) +\
                     "\n" + "Tipo de Ausencia: "+ str(ausencia.tipovacacion.nombre) + \
                     "\n" + "Descripcion: "+ str(ausencia.descripcion) +\
                     "\n" + "Fecha Inicio: "+ str(ausencia.fechai.strftime("%d/%m/%Y")) + \
                     "\n" + "Fecha Fin: "+ str(ausencia.fechaf.strftime("%d/%m/%Y")) + \
                     "\n" + "\n" + "Autorizado por: " + str(autorizacion)  + \
                     "\n" + "Estado: " + str(ausencia.estadoautorizacion) + \
                     "\n" + "Respuesta autorizacion: " + str(ausencia.respuestaautorizacion) + \
                     "\n" + "\n" + "Aprobado por: " + str(aprobacion) + \
                     "\n" + "Estado: " + str(ausencia.estadoaprobacion) + \
                     "\n" + "Respuesta aprobacion: "+ str(ausencia.respuestaaprobacion) + \
                     "\n" + "\n" +  "Saludos"
            # Creamos el objeto mensaje

            CorreoManager(self.db).funcion_email(server, correos,asunto,cuerpo)


    def notificar_vacacion_respuesta_aprobacion(self, ausencia):
        correos = []
        autorizacion = ""
        aprobacion = ""
        persona = ""
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(
            ServidorCorreo.id == 1).first()
        correo_rrhh = self.db.query(Correorrhh).filter(Correorrhh.enabled == True).all()

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()


        if ausencia.fkpersona:
            correo = PersonaManager(self.db).obtener_correo(ausencia.fkpersona)
            if correo:
                correos.append(correo)

        for _rrhh in correo_rrhh:
            correo = PersonaManager(self.db).obtener_correo(_rrhh.fkpersona)
            if correo:
                correos.append(correo)

        if ausencia.fkpersona:
            if ausencia.persona.empleado[0].autorizacion:
                if ausencia.fkautorizacion:
                    correo = PersonaManager(self.db).obtener_correo(ausencia.fkautorizacion)
                    if correo:
                        correos.append(correo)

        if ausencia.fkautorizacion:
            autorizacion = ausencia.autorizacion.fullname
        else:
            autorizacion = "------"

        if ausencia.fkaprobacion:
            aprobacion = ausencia.aprobacion.fullname
        else:
            aprobacion = "------"

        if ausencia.fkpersona:
            persona = ausencia.persona.fullname
        else:
            persona = "Varias Personas"


        if len(correos) > 0:
            asunto = 'Respuesta de Solicitud:  ' + str(persona)
            cuerpo = "Visite el Portal del Empleado: "+ str(ajuste.dominio) + \
                     "portal_ausencia"+ \
                     "\n" + "\n" + "Nro: "+ str(ausencia.id) + \
                     "\n" + "Persona: "+ str(persona) +\
                     "\n" + "Tipo de Ausencia: "+ str(ausencia.tipovacacion.nombre) + \
                     "\n" + "Descripcion: "+ str(ausencia.descripcion) +\
                     "\n" + "Fecha Inicio: "+ str(ausencia.fechai.strftime("%d/%m/%Y")) + \
                     "\n" + "Fecha Fin: "+ str(ausencia.fechaf.strftime("%d/%m/%Y")) + \
                     "\n" + "\n" + "Autorizado por: " + str(autorizacion)  + \
                     "\n" + "Estado: " + str(ausencia.estadoautorizacion) + \
                     "\n" + "Respuesta autorizacion: " + str(ausencia.respuestaautorizacion) + \
                     "\n" + "\n" + "Aprobado por: " + str(aprobacion) + \
                     "\n" + "Estado: " + str(ausencia.estadoaprobacion) + \
                     "\n" + "Respuesta aprobacion: "+ str(ausencia.respuestaaprobacion) + \
                     "\n" + "\n" +  "Saludos"
            # Creamos el objeto mensaje

            CorreoManager(self.db).funcion_email(server, correos, asunto, cuerpo)


    def notificar_token_email(self, usuario):
        correos = []
        server = self.db.query(ServidorCorreo).filter(ServidorCorreo.enabled == True).filter(
            ServidorCorreo.id == 1).first()

        if usuario.fkpersona:
            correo = PersonaManager(self.db).obtener_correo(usuario.fkpersona)
            if correo != "" or correo is not None:
                correos.append(correo)

        if len(correos) > 0:
            asunto = 'Solicitud de codigo'
            cuerpo = "Se ha detectado inicio de sesion en 2 pasos para el usuario:" + str(usuario.persona.fullname) + "\n" + "Codigo: " + str(
                usuario.token) + "\n" + "\n" + "Saludos"

            CorreoManager(self.db).funcion_email(server, correos, asunto, cuerpo)


    def funcion_email(self, server,correos,asunto,cuerpo):
        # Iniciamos los parámetros del script

        remitente = "<" + server.correo + ">"
        destinatarios = correos
        asunto = asunto
        cuerpo = cuerpo
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
        print("Se crea conexión con el servidor")
        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP(server.servidor,server.puerto)
        # Ciframos la conexión
        sesion_smtp.starttls()
        # Iniciamos sesión en el servidor
        sesion_smtp.login(server.correo, server.password)
        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()
        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)
        # Cerramos la conexión
        sesion_smtp.quit()
        print("correo enviado")


class SmsManager(SuperManager):

    def __init__(self, db):
        super().__init__(ServidorCorreo, db)


    def notificar_token_sms(self, usuario):
        telefono = ""
        texto = str(usuario.token) + " es tu codigo para el inicio de sesion en el sistema Cloudgh"

        str(usuario.token)

        if usuario.fkpersona:
            telefono = PersonaManager(self.db).obtener_telefono(usuario.fkpersona)






        SmsManager(self.db).sms(telefono, texto)

    def sms(self,telefono,texto):
        destinations = telefono
        message = texto
        senderId = ""
        debug = True

        SmsManager(self.db).funcion_sms(destinations, message, senderId, debug)

        return texto

    def funcion_sms(self,destinations, message, senderId, debug):
        if debug:
            print('Enter altiriaSms: ' + destinations + ', message: ' + message + ', senderId: ' + senderId)

            try:
                # Se crea la lista de parámetros a enviar en la petición POST
                # XX, YY y ZZ se corresponden con los valores de identificación del usuario en el sistema.
                payload = [
                    ('cmd', 'sendsms'),
                    ('domainId', 'CLI_2776'),
                    ('login', 'hlambert@cloudbit.com.bo'),
                    ('passwd', 'EnviAEses%'),
                    # No es posible utilizar el remitente en América pero sí en España y Europa
                    ('senderId', senderId),
                    ('msg', message)
                ]

                # add destinations
                for destination in destinations.split(","):
                    payload.append(('dest', destination))

                # Se fija la codificacion de caracteres de la peticion POST
                contentType = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}

                # Se fija la URL sobre la que enviar la petición POST
                url = 'http://www.altiria.net/api/http'

                # Se envía la petición y se recupera la respuesta
                r = requests.post(url,
                                  data=payload,
                                  headers=contentType,
                                  # Se fija el tiempo máximo de espera para conectar con el servidor (5 segundos)
                                  # Se fija el tiempo máximo de espera de la respuesta del servidor (60 segundos)
                                  timeout=(5, 60))  # timeout(timeout_connect, timeout_read)

                if debug:
                    if str(r.status_code) != '200':  # Error en la respuesta del servidor
                        print('ERROR GENERAL: ' + str(r.status_code))

                    else:  # Se procesa la respuesta
                        print('Código de estado HTTP: ' + str(r.status_code))

                        if (r.text).find("ERROR errNum:"):
                            print('Error de Altiria: ' + r.text)

                        else:
                            print('Cuerpo de la respuesta: \n' + r.text)

                return r.text

            except requests.ConnectTimeout:
                print("Tiempo de conexión agotado")


            except requests.ReadTimeout:
                print("Tiempo de respuesta agotado")


            except Exception as ex:
                print("Error interno: " + str(ex))


    #print('The function altiriaSms returns: \n' + altiriaSms('346xxxxxxxx,346yyyyyyyy', 'Mesaje de prueba', '', True))


    # No es posible utilizar el remitente en América pero sí en España y Europa
    # Utilizar esta llamada solo si se cuenta con un remitente autorizado por Altiria
    # print 'The function altiriaSms returns: \n'+altiriaSms('346xxxxxxxx,346yyyyyyyy','Mesaje de prueba', 'remitente', True)


