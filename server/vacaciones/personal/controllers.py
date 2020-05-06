from .managers import *
from ...common.controllers import CrudController
from ...configuraciones.empresa.managers import *
from ...personal.persona.managers import *
from ...vacaciones.historico.managers import *
from xhtml2pdf import pisa

import os.path
import uuid
import json

class Report:
    def html_to_pdf(self, sourceHtml, nombre):
        outputFilename = 'server/common/resources/downloads/' + nombre

        resultFile = open(outputFilename, "w+b")
        pisaStatus = pisa.CreatePDF(
            sourceHtml,
            dest=resultFile)
        resultFile.close()

        return pisaStatus.err

global report
report = Report()


class V_personalController(CrudController):

    manager = V_personalManager
    html_index = "vacaciones/personal/views/index.html"
    html_table = "vacaciones/personal/views/table.html"
    routes = {
        '/v_personal': {'GET': 'index', 'POST': 'table'},
        '/v_personal_insert': {'POST': 'insert'},
        '/v_personal_update': {'PUT': 'edit', 'POST': 'update'},
        '/v_personal_delete': {'POST': 'delete'},
        '/v_personal_importar': {'POST': 'importar'},
        '/v_personal_historico': {'POST': 'historico'},
        '/v_personal_disponible': {'POST': 'disponible'}

    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        return aux

    def importar(self):
        self.set_session()
        fileinfo = self.request.files['archivo'][0]
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open("server/common/resources/uploads/" + cname, 'wb')
        fh.write(fileinfo['body'])
        fh.close()
        if extn in ['.xlsx', '.xls']:
            mee = self.manager(self.db).importar_excel(cname,self.get_user_id(),self.request.remote_ip)
            self.respond(message=mee['message'], success=mee['success'])
        else:
            self.respond(message='Formato de Archivo no aceptado¡¡', success=False)
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        V_personalManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        V_personalManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip

        result = V_personalManager(self.db).delete(id, estado, user, ip)

        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')

    def disponible(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        fkpersona = diccionary['fkpersona']
        fechai = diccionary['fechai']
        fechaf = diccionary['fechaf']

        respuesta = V_personalManager(self.db).disponibilidad(fkpersona,fechai,fechaf)
        if respuesta['respuesta']:
            self.respond(message=respuesta['mensaje'], success=respuesta['respuesta'], tipo=respuesta['tipo'])
        else:
            self.respond(message=respuesta['mensaje'], success=respuesta['respuesta'], tipo=respuesta['tipo'])

    def historico(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        objetoempresa = EmpresaManager(self.db).obtener_empresa()

        detalle = ""

        if objetoempresa:
            if objetoempresa.foto1:
                logoempresa = objetoempresa.foto1
            else:
                logoempresa = "/resources/images/sinImagen.jpg"

        else:
            logoempresa = "/resources/images/sinImagen.jpg"

        lista_historico = V_historicoManager(self.db).obtener_historico(diccionary['fkpersona'])
        persona = PersonaManager(self.db).obtener_persona(diccionary['fkpersona'])
        v_persona = V_personalManager(self.db).obtener_x_personal(diccionary['fkpersona'])

        for x in lista_historico:

            detalle = detalle + "<tr style='font-size: 12px; border: 0px; '>" \
                                "   <td colspan='5' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(x.fecha.strftime('%d/%m/%Y %H:%M:%S')) + "</font></td>" \
                                "   <td colspan='9' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(x.descripcion) + "</font></td>" \
                                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(x.dias) + "</font></td>" \
                                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(x.operacion) + "</font></td>" \
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

        html += "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "<tr color='#ffffff' >" \
                "   <th colspan='20' scope='colgroup' align='left' style='background-color: #1976d2; font-size=4; color: white; margin-top: 4px'>HISTORICO DE VACACIONES</th>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Nombres y Apellidos: </strong></td>" \
                "   <td colspan='15' scope='colgroup'align='left'><font>" + str(persona.fullname) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Cargo: </strong></td>" \
                "   <td colspan='15' scope='colgroup'align='left'><font>" + str(persona.empleado[0].cargo.nombre) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Codigo: </strong></td>" \
                "   <td colspan='15' scope='colgroup'align='left'><font>" + str(persona.empleado[0].codigo) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px'>" \
                "       <th colspan='5' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Fecha</th>" \
                "       <th colspan='9' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Descripcion</th>" \
                "       <th colspan='3' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Dias</th>" \
                "       <th colspan='3' scope='colgroup' align='center' style='background-color: #1976d2; color: white; margin-top: 4px'>Operacion</th>" \
                "</tr>" \
                "" + detalle + "" \
                "<tr color='#ffffff' >" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>TOTAL DIAS VACACIONES: </strong></td>" \
                "   <td colspan='15' scope='colgroup'align='left'><font>" + str(v_persona.dias) + "</font></td>" \
                "</tr>" \
                "</table>"

        nombre = "Historico-vacaciones.pdf"

        report.html_to_pdf(html, nombre)
        self.respond('/resources/downloads/' + nombre)