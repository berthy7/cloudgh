from .managers import *
from ...common.controllers import CrudController
from ...ausencia.tipoausencia.managers import *
from ...personal.persona.managers import *
from ...vacaciones.historico.managers import *
from ...ausencia.permiso.managers import *

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
global image_report

image_report = "../server/common/resources/images/logos/elfec.jpg"

class PortalPermisoController(CrudController):

    manager = PermisoManager
    html_index = "portal/permiso/views/index.html"
    html_table = "portal/permiso/views/table.html"
    routes = {
        '/portal_permiso': {'GET': 'index', 'POST': 'table'},
        '/portal_permiso_insert': {'POST': 'insert'},
        '/portal_permiso_update': {'PUT': 'edit', 'POST': 'update'},
        '/portal_permiso_delete': {'POST': 'delete'},
        '/portal_permiso_disponible': {'POST': 'disponible'},
        '/portal_permiso_autorizacion': {'PUT': 'edit', 'POST': 'autorizacion'},
        '/portal_permiso_aprobacion': {'PUT': 'edit', 'POST': 'aprobacion'},
        '/portal_permiso_imprimir': {'POST': 'imprimir'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        idpersona = us.fkpersona

        if idpersona:
            aux['idpersona'] = idpersona
            nombrepersona = PersonaManager(self.db).obtener_persona(idpersona)
            aux['nombrepersona'] = nombrepersona.fullname
            aux['rol'] = us.rol.nombre

            aux['permisos_personales'] = PortalPermisoManager(self.db).obtener_x_persona(idpersona)
            aux['permisos_recibidas'] = PortalPermisoManager(self.db).obtener_x_supervisor(idpersona)
        else:
            aux['idpersona'] = 0
            aux['nombrepersona'] = "Sin Nombre"
            aux['rol'] = us.rol.nombre

            aux['permisos_personales'] = PortalPermisoManager(self.db).listar_todo()
            aux['permisos_recibidas'] = PortalPermisoManager(self.db).listar_todo()

        aux['tipoausencia'] = TipoausenciaManager(self.db).listar_permisos()
        aux['personal'] = PersonaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip

        permiso = PermisoManager(self.db).insert(diccionary)

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PermisoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        estado = diccionary['enabled']
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = PermisoManager(self.db).delete(id, estado, user, ip)
        if result.enabled:
            self.respond(success=True, message='Alta Realizada Correctamente.')
        elif not result.enabled:    
            self.respond(success=False, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')

    def disponible(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        respuesta = PermisoManager(self.db).disponibilidad(diccionary['fkpersona'],diccionary['fktipoausencia'],diccionary['dia'],diccionary['fechai'])
        if respuesta['respuesta']:
            self.respond(message=respuesta['mensaje'], success=respuesta['respuesta'], tipo=respuesta['tipo'])
        else:
            self.respond(message=respuesta['mensaje'], success=respuesta['respuesta'], tipo=respuesta['tipo'])

    def autorizacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        solicitud = PermisoManager(self.db).autorizacion(diccionary)
        self.respond(success=True, message='Autorizado correctamente.')

    def aprobacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        solicitud = PermisoManager(self.db).aprobacion(diccionary)

        self.respond(success=True, message='Aprobado correctamente.')

    def imprimir(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']

        solicitud = PermisoManager(self.db).obtener_x_id(id)

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
                                                                                                                                                               "       <td colspan='10' align='center' style='font-weight:bold;font-size: 18px; padding-right: 55px; padding-top: 0px'>AUTORIZACIÓN DE SALIDA</td>" \
                                                                                                                                                               "   </tr>" \
                                                                                                                                                               "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                                                                                                                                                               "       <td colspan='9' class='text-normal' align='right' style='font-weight:bold; padding-right: 4px; padding-top: 0px'>ITEM:</td>" \
                                                                                                                                                               "       <td colspan='3' class='text-normal' align='right' style='padding-top: 2px'>" + str(
            solicitud.id) + " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>" \
                            "   </tr>" \
                            "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                            "       <td colspan='9' class='text-normal' align='right' style='font-weight:bold;padding-right: 4px; padding-top: 0px'>FECHA:</td>" \
                            "       <td colspan='3' class='text-normal' align='right' style='padding-top: 2px'> " + str(
            solicitud.fechai.strftime(
                "%d/%m/%Y")) + " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>" \
                               "   </tr>" \
                               "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                               "       <th colspan='4' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 2px'>Nombre de Trabajador:</th>" \
                               "       <td colspan='8' class='text-normal' align='left' style='padding-top: 2px'>" + str(
            solicitud.persona.fullname) + "</td>" \
                                          "   </tr>" \
                                          "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                                          "       <th colspan='4' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px'>Unidad:</th>" \
                                          "       <td colspan='8' class='text-normal' align='left' style='padding-top: 5px'>" + str(
            solicitud.persona.empleado[0].gerencia.nombre) + "</td>" \
                                                             "   </tr>" \
                                                             "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                                                             "       <th colspan='4' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px'>Motivo de Salida:</th>" \
                                                             "       <td colspan='8' class='text-normal' align='left' style='padding-top: 5px'>" + str(
            solicitud.descripcion) + "</td>" \
                                     "   </tr>" \
                                     "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                                     "       <th colspan='4' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px'></th>" \
                                     "       <td colspan='8' class='text-normal' align='left' style='padding-top: 5px'></td>" \
                                     "   </tr>" \
                                     "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                                     "       <th colspan='3' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px'>Hora Salida:</th>" \
                                     "       <td colspan='3' class='text-normal' align='left' style='padding-top: 5px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(
            solicitud.horai.strftime("%H:%M")) + "</td>" \
                                                 "       <th colspan='3' scope='colgroup' align='left' style='padding-left: 20px; font-size: 5; padding-top: 5px' >Hora Retorno:</th>" \
                                                 "       <td colspan='3' class='text-normal' align='left' style='padding-top: 5px'>" + str(
            solicitud.horaf.strftime("%H:%M")) + "</td>" \
                                                 "   </tr>" \
                                                 "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                                                 "       <td width='30%' colspan='4' align='left' ><font size=4><i class='format'></i></br> </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______________________</br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Vo.Bo &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RESPONSABLE</br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RECURSOS HUMANOS</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;</br></font></td>" \
                                                 "       <td width='30%' colspan='4' align='left' ><font size=4><i class='format'></i></br> </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______________________ </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TRABAJADOR</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;</br></font></td>" \
                                                 "       <td width='30%' colspan='4' align='left' ><font size=4><i class='format'></i></br> </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______________________ </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; JEFE INMEDIATO SUPERIOR</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;" + jefe_nombre + "</br>&nbsp;&nbsp;&nbsp;&nbsp;" + jefe_cargo + "</br></font></td>" \
                                                                                                                                                                                                                                                                                                                                                                                              "   </tr>" \
                                                                                                                                                                                                                                                                                                                                                                                              "   </table>" \
                                                                                                                                                                                                                                                                                                                                                                                              "   </br>"

        nombre = "Autorizacion-salida-" + str(id) + ".pdf"

        report.html_to_pdf(html, nombre)

        self.respond('/resources/downloads/' + nombre)
