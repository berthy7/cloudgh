from .managers import *
from ...common.controllers import CrudController
from ...ausencia.tipoausencia.managers import *
from ...personal.persona.managers import *
from ...vacaciones.historico.managers import *
from ...ausencia.licencia.managers import *


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

class PortalLicenciaController(CrudController):

    manager = PortalLicenciaManager
    html_index = "portal/licencia/views/index.html"
    html_table = "portal/licencia/views/table.html"
    routes = {
        '/portal_licencia': {'GET': 'index', 'POST': 'table'},
        '/portal_licencia_insert': {'POST': 'insert'},
        '/portal_licencia_update': {'PUT': 'edit', 'POST': 'update'},
        '/portal_licencia_delete': {'POST': 'delete'},
        '/portal_licencia_autorizacion': {'PUT': 'edit', 'POST': 'autorizacion'},
        '/portal_licencia_aprobacion': {'PUT': 'edit', 'POST': 'aprobacion'},
        '/portal_licencia_imprimir': {'POST': 'imprimir'}
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

            aux['licencias_personales'] = PortalLicenciaManager(self.db).obtener_x_persona(idpersona)
            aux['licencias_recibidas'] = PortalLicenciaManager(self.db).obtener_x_supervisor(idpersona)
        else:
            aux['idpersona'] = 0
            aux['nombrepersona'] = "Sin Nombre"
            aux['rol'] = us.rol.nombre

            aux['licencias_personales'] = PortalLicenciaManager(self.db).listar_todo()
            aux['licencias_recibidas'] = PortalLicenciaManager(self.db).listar_todo()

        aux['tipoausencia'] = TipoausenciaManager(self.db).listar_licencias()
        aux['personal'] = PersonaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        portal_licencia = LicenciaManager(self.db).insert(diccionary)


        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        LicenciaManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        estado = diccionary['enabled']
        user = self.get_user_id()
        ip = self.request.remote_ip
        result =LicenciaManager(self.db).delete(id, estado, user, ip)
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
        solicitud = LicenciaManager(self.db).autorizacion(diccionary)
        self.respond(success=True, message='Autorizado correctamente.')

    def aprobacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        solicitud = LicenciaManager(self.db).aprobacion(diccionary)

        self.respond(success=True, message='Aprobado correctamente.')

    def imprimir(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']

        solicitud = LicenciaManager(self.db).obtener_x_id(id)

        autorizacion = ""
        aprobacion = ""
        if solicitud.fkautorizacion:
            autorizacion = solicitud.autorizacion.fullname
        else:
            autorizacion = "------"

        if solicitud.fkaprobacion:
            aprobacion = solicitud.aprobacion.fullname
        else:
            aprobacion = "------"

        html = "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
               "<style>" \
               "@page {size: a4 portrait; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 772pt; height: 20pt; }}" \
               "</style>" \
               "<div class='container' style='font-size: 12px'>" \
               "<div class='row'>" \
               "<div class='col-md-4'>" \
               "<img src='" + image_report + "' width='134' height='75' alt=''>" \
             "</div>" \
             " </div>" \
             "<div class='row'>" \
             "<div class='col-md-8'>" \
             "<h6 class='font-weight-bold' align='right'># " + str(solicitud.id) + "</h6>" \
             "</div>" \
             "</div>" \
             "<div class='row'>" \
             "<div class='col-md-4'>" \
             "<h6 align='center'>INFORME LICENCIAS CON GOCE DE HABER</h6>" \
                           "</div>" \
                           "</div>" \
                           "</div>"

        html += "<table>" \
                "<colgroup span='2'></colgroup>" \
                "<colgroup span='2'></colgroup>" \
                "<tr class='spacer'> <td> </td></tr>" \
                "<tr class='spacer'> <td> </td></tr>" \
                "<tr style='font-size: 12px'>" \
                "<th colspan='2' scope='colgroup'></th>" \
                "<th colspan='2' scope='colgroup' align='left'>Personal: </th>" \
                "<td colspan='4' class='text-normal' align='left'>"+ solicitud.persona.fullname+"</td>" \
                "</tr>" \
                "<tr style='font-size: 12px'>" \
                "<th colspan='2' scope='colgroup'></th>" \
                "<th colspan='2' scope='colgroup' align='left'>Tipo de Ausencia: </th>" \
                "<td colspan='4' class='text-normal' align='left'>"+ solicitud.tipoausencia.nombre +"</td>" \
               "</tr>" \
               "<tr style='font-size: 12px'>" \
               "<th colspan='2' scope='colgroup'></th>" \
               "<th colspan='2' scope='colgroup' align='left'>Descripcion: </th>" \
               "<td colspan='4' class='text-normal' align='left'>"+ solicitud.descripcion +"</td>" \
               "</tr>" \
               "<tr style='font-size: 12px'>" \
               "<th colspan='2' scope='colgroup'></th>" \
               "<th colspan='2' scope='colgroup' align='left'>Fecha Inicio: </th>" \
               "<td colspan='4' class='text-normal' align='left'>"+solicitud.fechai.strftime("%d/%m/%Y")+"</td>" \
             "</tr>" \
             "<tr style='font-size: 12px'>" \
             "<th colspan='2' scope='colgroup'></th>" \
             "<th colspan='2' scope='colgroup' align='left'>Fecha Fin: </th>" \
             "<td colspan='4' class='text-normal' align='left'>"+solicitud.fechaf.strftime("%d/%m/%Y")+"</td>" \
              "</tr>" \
              "<tr class='spacer'> <td> </td></tr>" \
              "<tr class='spacer'> <td> </td></tr>" \
              "<tr style='font-size: 12px'>" \
              "<th colspan='2' scope='colgroup'></th>" \
              "<th colspan='2' scope='colgroup'> AUTORIZACION </th>" \
              "<th colspan='2' scope='colgroup'></th>" \
              "</tr>" \
              "<tr class='spacer'> <td> </td></tr>" \
               "<tr style='font-size: 12px'>" \
               "<th colspan='2' scope='colgroup'></th>" \
               "<th colspan='2' scope='colgroup' align='left'>Autorizado por: </th>" \
               "<td colspan='4' class='text-normal' align='left'>" + autorizacion + "</td>" \
             "</tr>" \
             "<tr style='font-size: 12px'>" \
             "<th colspan='2' scope='colgroup'></th>" \
             "<th colspan='2' scope='colgroup' align='left'>Estado: </th>" \
             "<td colspan='4' class='text-normal' align='left'>" + solicitud.estadoautorizacion + "</td>" \
              "</tr>" \
              "<tr style='font-size: 12px'>" \
              "<th colspan='2' scope='colgroup'></th>" \
              "<th colspan='2' scope='colgroup' align='left'>Respuesta: </th>" \
              "<td colspan='4' class='text-normal' align='left'>" + solicitud.respuestaautorizacion+ "</td>" \
              "</tr>" \
             "<tr class='spacer'> <td> </td></tr>" \
             "<tr class='spacer'> <td> </td></tr>" \
             "<tr style='font-size: 12px'>" \
             "<th colspan='2' scope='colgroup'></th>" \
             "<th colspan='2' scope='colgroup'> APROBACION </th>" \
             "<th colspan='2' scope='colgroup'></th>" \
             "</tr>" \
             "<tr class='spacer'> <td> </td></tr>" \
             "<tr style='font-size: 12px'>" \
             "<th colspan='2' scope='colgroup'></th>" \
             "<th colspan='2' scope='colgroup' align='left'>Aprobado por: </th>" \
             "<td colspan='4' class='text-normal' align='left'>" + aprobacion + "</td>" \
             "</tr>" \
             "<tr style='font-size: 12px'>" \
             "<th colspan='2' scope='colgroup'></th>" \
             "<th colspan='2' scope='colgroup' align='left'>Estado: </th>" \
             "<td colspan='4' class='text-normal' align='left'>" + solicitud.estadoaprobacion + "</td>" \
              "</tr>" \
              "<tr style='font-size: 12px'>" \
              "<th colspan='2' scope='colgroup'></th>" \
              "<th colspan='2' scope='colgroup' align='left'>Respuesta: </th>" \
              "<td colspan='4' class='text-normal' align='left'>" + solicitud.respuestaaprobacion + "</td>" \
              "</tr>" \
              "</table>"


        nombre = "Informe-Licencia-" + str(id) + ".pdf"

        report.html_to_pdf(html, nombre)

        self.respond('/resources/downloads/' + nombre)
