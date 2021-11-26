from .managers import *
from ...common.controllers import CrudController
from ..tipoausencia.managers import *
from ...personal.persona.managers import *
from ...vacaciones.historico.managers import *


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


class RegularizacionController(CrudController):

    manager = RegularizacionManager
    html_index = "ausencia/regularizacion/views/index.html"
    html_table = "ausencia/regularizacion/views/table.html"
    routes = {
        '/regularizacion': {'GET': 'index', 'POST': 'table'},
        '/regularizacion_insert': {'POST': 'insert'},
        '/regularizacion_update': {'PUT': 'edit', 'POST': 'update'},
        '/regularizacion_delete': {'POST': 'delete'},
        '/regularizacion_autorizacion': {'PUT': 'edit', 'POST': 'autorizacion'},
        '/regularizacion_aprobacion': {'PUT': 'edit', 'POST': 'aprobacion'},
        '/regularizacion_imprimir': {'POST': 'imprimir'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['regularizaciones'] = RegularizacionManager(self.db).listar_todo()
        aux['personal'] = PersonaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        regularizacion = RegularizacionManager(self.db).insert(diccionary)

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        RegularizacionManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        estado = diccionary['enabled']
        user = self.get_user_id()
        ip = self.request.remote_ip
        result =RegularizacionManager(self.db).delete(id, estado, user, ip)
        if result.enabled:
            self.respond(success=True, message='Alta Realizada Correctamente.')
        elif not result.enabled:    
            self.respond(success=False, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')

    def autorizacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        solicitud = RegularizacionManager(self.db).autorizacion(diccionary)
        self.respond(success=True, message='Autorizado correctamente.')

    def aprobacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        solicitud = RegularizacionManager(self.db).aprobacion(diccionary)

        self.respond(success=True, message='Aprobado correctamente.')

    def imprimir(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']

        solicitud = RegularizacionManager(self.db).obtener_x_id(id)

        logoempresa = "/resources/images/elfec.png"

        jefe_nombre = ""
        jefe_cargo = ""

        if solicitud.fkautorizacion:
            jefe_nombre = solicitud.autorizacion.fullname
            jefe_cargo = solicitud.autorizacion.empleado[0].cargo.nombre

        elif solicitud.fkaprobacion:
            jefe_nombre = solicitud.aprobacion.fullname
            jefe_cargo = solicitud.aprobacion.empleado[0].cargo.nombre

        hoy = datetime.now().strftime('%d/%m/%Y')

        html = "" \
               "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
               "<style>" \
               "  .format{ font-weight: bold; } " \
               "   @page {size: letter portrait; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 300pt; height: 20pt; }}" \
               "</style>" \
               "</br>"

        html += "" \
                "<table align='center' style='padding: 4px; border: 3px double black;' width='100%'>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <td colspan='12' class='text-normal' align='right' style='padding-right: 15px; padding-top: 15px'>RH-06175-01</td>" \
                "   </tr>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 20px; padding-top: 0px'><img src='../server/common" + logoempresa + "' width='auto' height='75'></th>" \
               "       <td colspan='10' align='center' style='font-weight:bold;font-size: 18px; padding-right: 55px; padding-top: 0px'>REGULARIZACIÓN DE MARCACIONES</td>" \
               "   </tr>" \
               "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
               "       <td colspan='9' class='text-normal' align='right' style='font-weight:bold; padding-right: 4px; padding-top: 0px'>ITEM:</td>" \
               "       <td colspan='3' class='text-normal' align='right' style='padding-top: 2px'>" + str(solicitud.id) + " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>" \
                "   </tr>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <td colspan='9' class='text-normal' align='right' style='font-weight:bold;padding-right: 4px; padding-top: 0px'>FECHA:</td>" \
                "       <td colspan='3' class='text-normal' align='right' style='padding-top: 2px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>" \
               "   </tr>" \
               "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
               "       <th colspan='4' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 2px'>Nombre de Trabajador:</th>" \
               "       <td colspan='8' class='text-normal' align='left' style='padding-top: 2px'>" + str(solicitud.persona.fullname) + "</td>" \
                  "   </tr>" \
                  "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                  "       <th colspan='4' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px'>Unidad:</th>" \
                  "       <td colspan='8' class='text-normal' align='left' style='padding-top: 5px'>" + str(solicitud.persona.empleado[0].gerencia.nombre) + "</td>" \
                 "   </tr>" \
                 "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                 "       <th colspan='4' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px'>Motivo de Salida:</th>" \
                 "       <td colspan='8' class='text-normal' align='left' style='padding-top: 5px'></td>" \
             "   </tr>" \
             "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
             "       <th colspan='4' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px'></th>" \
             "       <td colspan='8' class='text-normal' align='left' style='padding-top: 5px'></td>" \
             "   </tr>" \
             "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
             "       <th colspan='3' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px'>Fecha Salida:</th>" \
             "       <td colspan='3' class='text-normal' align='left' style='padding-top: 5px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>" \
             "       <th colspan='3' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px' >Fecha Retorno:</th>" \
             "       <td colspan='3' class='text-normal' align='left' style='padding-top: 5px'></td>" \
             "   </tr>" \
             "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
             "       <td width='30%' colspan='4' align='left' ><font size=4><i class='format'></i></br> </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______________________</br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Vo.Bo &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RESPONSABLE</br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RECURSOS HUMANOS</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;</br></font></td>" \
             "       <td width='30%' colspan='4' align='left' ><font size=4><i class='format'></i></br> </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______________________ </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TRABAJADOR</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;</br></font></td>" \
             "       <td width='30%' colspan='4' align='left' ><font size=4><i class='format'></i></br> </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______________________ </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; JEFE INMEDIATO SUPERIOR</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;" + jefe_nombre + "</br>&nbsp;&nbsp;&nbsp;&nbsp;" + jefe_cargo + "</br></font></td>" \
              "   </tr>" \
            "   </table>" \
          "   </br>"

        nombre = "Regularizacion-" + str(id) + ".pdf"

        report.html_to_pdf(html, nombre)

        self.respond('/resources/downloads/' + nombre)
