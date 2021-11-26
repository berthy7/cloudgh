from .managers import *
from ...common.controllers import CrudController
from ...asistencia.tipoausencia.managers import *
from ...personal.persona.managers import *
from ...vacaciones.historico.managers import *
from ...vacaciones.solicitud.managers import *


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

class PortalVacacionController(CrudController):

    manager = V_solicitudManager
    html_index = "portal/vacacion/views/index.html"
    html_table = "portal/vacacion/views/table.html"
    routes = {
        '/portal_vacacion': {'GET': 'index', 'POST': 'table'},
        '/portal_vacacion_insert': {'POST': 'insert'},
        '/portal_vacacion_update': {'PUT': 'edit', 'POST': 'update'},
        '/portal_vacacion_delete': {'POST': 'delete'},
        '/portal_vacacion_autorizacion': {'PUT': 'edit', 'POST': 'autorizacion'},
        '/portal_vacacion_aprobacion': {'PUT': 'edit', 'POST': 'aprobacion'},
        '/portal_vacacion_imprimir': {'POST': 'imprimir'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        idpersona = us.fkpersona

        if idpersona:
            aux['idpersona'] = idpersona
            nombrepersona = PersonaManager(self.db).obtener_persona(idpersona)
            aux['nombrepersona'] = nombrepersona.fullname

            v_persona = V_personalManager(self.db).obtener_x_personal(idpersona)
            if v_persona:
                aux['dias_vacacion'] = v_persona
                aux['dias_vacacion_index'] = v_persona['objeto']
                aux['dias_vacacion_gestion'] = v_persona['gestion']
            else:
                aux['dias_vacacion_index'] = "---"
                aux['dias_vacacion_gestion'] = v_persona['gestion']

            aux['rol'] = us.rol.nombre

            aux['vacaciones_personales'] = PortalVacacionManager(self.db).obtener_x_persona(idpersona)
            aux['vacaciones_recibidas'] = PortalVacacionManager(self.db).obtener_x_supervisor(idpersona)
            aux['total_vacacion'] = V_personalManager(self.db).obtener_x_fkpersona(idpersona)
        else:
            aux['idpersona'] = 0
            aux['nombrepersona'] = "Sin Nombre"
            aux['dias_vacacion'] = 0
            aux['dias_vacacion_index'] = "---"
            aux['dias_vacacion_gestion'] = "---"
            aux['rol'] = us.rol.nombre

            aux['vacaciones_personales'] = PortalVacacionManager(self.db).listar_todo()
            aux['vacaciones_recibidas'] = PortalVacacionManager(self.db).listar_todo()
            aux['total_vacacion'] = []

        aux['tipovacacion'] = V_tipovacacionManager(self.db).listar_para_personal()
        aux['personal'] = PersonaManager(self.db).listar_todo()
        # aux['select_semanal'] = SemanalManager(self.db).listar_todo()
        aux['admin'] = PersonaManager(self.db).get_employees_tree()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        solicitud = V_solicitudManager(self.db).insert(diccionary)

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        solicitud = V_solicitudManager(self.db).update(objeto)

        self.respond(success=True, message='Modificado correctamente.')

    def autorizacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        solicitud = V_solicitudManager(self.db).autorizacion(diccionary)
        self.respond(success=True, message='Autorizado correctamente.')

    def aprobacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        solicitud = V_solicitudManager(self.db).aprobacion(diccionary)

        self.respond(success=True, message='Aprobado correctamente.')

    def imprimir(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']

        solicitud = V_solicitudManager(self.db).obtener_x_id(id)

        detalleVacacion = ""
        detalleGestion = ""

        autorizacion = ""
        aprobacion = ""
        persona = ""
        legajo = ""
        fechaIngreso = ""
        cargo = ""
        ListadetalleVacacion = ""

        if solicitud.fkautorizacion:
            autorizacion = solicitud.autorizacion.fullname
            autorizacion_cargo = solicitud.autorizacion.empleado[0].cargo.nombre
        else:
            autorizacion = "------"
            autorizacion_cargo = "------"

        if solicitud.fkaprobacion:
            aprobacion = solicitud.aprobacion.fullname
            aprobacion_cargo = solicitud.aprobacion.empleado[0].cargo.nombre
        else:
            aprobacion = "------"
            aprobacion_cargo = "------"

        if solicitud.fkpersona:
            persona = solicitud.persona.fullname
            legajo = solicitud.persona.empleado[0].codigo
            # desarrollo
            # crear funcion para obtener el contrato actuaal
            fechaIngreso = solicitud.persona.contrato[0].fechaIngreso.strftime("%d/%m/%Y")
            cargo = solicitud.persona.empleado[0].cargo.nombre
            ListadetalleVacacion = V_personalManager(self.db).obtener_x_fkpersona(solicitud.fkpersona)
        else:
            persona = "Varias Personas"
            legajo = ""
            fechaIngreso = ""
            cargo = ""
            ListadetalleVacacion = []

        for det in ListadetalleVacacion:

            espaciosBlancos = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

            if len(str(det.dias)) == 1:
                espaciosBlancos = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

            elif len(str(det.dias)) == 2:
                espaciosBlancos = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

            elif len(str(det.dias)) == 4:
                espaciosBlancos = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

            detalleVacacion += "<p>&nbsp;&nbsp;&nbsp;&nbsp;" + str(
                det.gestion) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(det.dias) + str(
                espaciosBlancos) + str(det.estado) + "</p>"

        # empresa = EmpresaManager(self.db).obtener_empresa()
        #
        # if empresa.foto3:
        #
        #     logoempresa = empresa.foto3
        #
        # else:
        #     logoempresa = "/resources/images/sinImagen.jpg"

        logoempresa = "/resources/images/elfec.png"

        dias_vacacion = BitacoraManager(self.db).obtener_cant_dias(solicitud.fktipovacacion, solicitud.fechai,
                                                                   solicitud.fechaf)

        objetoListaGestion = V_solicitudGestionManager(self.db).obtener_x_solicitud(id)

        for x in objetoListaGestion:
            detalleGestion = detalleGestion + "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                                              "       <td colspan='3' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>" + str(x.fksolicitud) + "</td>" \
                                            "       <td colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>" + str(x.gestion) + "</td>" \
                                            "       <td colspan='1' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>D</td>" \
                                            "       <td colspan='3' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>" + str(x.estado) + "</td>" \
                                            "       <td colspan='1' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>" + str(x.dias) + "</td>" \
                                            "   </tr>" \

        html = "" \
               "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
               "<style>" \
               "   @page {size: a4 portrait; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 772pt; height: 20pt; }}" \
               "</style>" \
               "<div align='left' width='100%'>" \
               "   <center>" \
               "       <img align='left' src='../server/common" + logoempresa + "' width='134' height='75'>" \
                "   </center>" \
                "</div>" \
                "<div class ='row clearfix'>" \
                "   <center>" \
                "       <div class ='col-sm-6'>" \
                "           <div class ='form-line'>" \
                "               <label class ='form-label'><font size=7 color='black'>PAPELETA DE VACACION</font></label>" \
                "           </div>" \
                "       </div>" \
                "   </center>" \
                "</div>" \
                "</br>"

        html += "" \
                "<table align='center' style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px'>VACACION Nro: </th>" \
                "       <td colspan='3' class='text-normal' align='left'>" + str(id) + "</td>" \
               "       <th colspan='3' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px'>Fecha de Proceso: </th>" \
               "       <td colspan='3' class='text-normal' align='left'>" + solicitud.fechar.strftime("%d/%m/%Y") + "</td>" \
              "   </tr>" \
              "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
              "   </tr>" \
              "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
              "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px'>Legajo: </th>" \
              "       <td colspan='8' class='text-normal' align='left'>" + str(legajo) + "</td>" \
             "   </tr>" \
             "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
             "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px'>Fecha de Ingreso: </th>" \
             "       <td colspan='8' class='text-normal' align='left'>" + fechaIngreso + "</td>" \
             "   </tr>" \
             "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
             "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px'>Nombre Completo: </th>" \
             "       <td colspan='3' class='text-normal' align='left'>" + persona + "</td>" \
            "       <th colspan='3' scope='colgroup' align='left' style='padding-left: 25px; padding-top: 3px'>Saldo de Vacaciones </th>" \
            "       <td colspan='3' class='text-normal' align='left'></td>" \
            "   </tr>" \
            "</table>"

        html += "" \
                "<table align='center' style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <th colspan='1' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 15px; padding-bottom: 15px'>Cargo: </th>" \
                "       <td colspan='3' class='text-normal' align='left' style='padding-left: 4px; padding-top: 15px; padding-bottom: 15px'>" + cargo + "</td>" \
                                                                                                                                                        "       <td colspan='4' class='text-normal' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 1px'>" + detalleVacacion + "</td>" \
                                                                                                                                                                                                                                                                                                        "   </tr>" \
                                                                                                                                                                                                                                                                                                        "</table>"

        html += "" \
                "<table align='center' style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 5px; padding-bottom: 5px'>Tiempo solicitado: </th>" \
                "       <td colspan='8' class='text-normal' align='left' >" + str(dias_vacacion) + " Dias</td>" \
                                                                                                   "   </tr>" \
                                                                                                   "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                                                                                                   "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 5px; padding-bottom: 5px'>Fecha de Inicio: </th>" \
                                                                                                   "       <td colspan='3' class='text-normal' align='left' >" + solicitud.fechai.strftime(
            "%d/%m/%Y") + "</td>" \
                          "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 5px; padding-bottom: 5px'>Fecha de Conclusion: </th>" \
                          "       <td colspan='3' class='text-normal' align='left' >" + solicitud.fechaf.strftime(
            "%d/%m/%Y") + "</td>" \
                          "   </tr>" \
                          "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                          "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>Hora Inicio: </th>" \
                          "       <td colspan='3' class='text-normal' align='left' >" + solicitud.fechai.strftime(
            "%H:%M") + "</td>" \
                       "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>Hora Conclusion: </th>" \
                       "       <td colspan='3' class='text-normal' align='left' >" + solicitud.fechaf.strftime(
            "%H:%M") + "</td>" \
                       "   </tr>" \
                       "</table>"

        html += "" \
                "<table align='center' style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <th colspan='12' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>Detalle de Vacacion</th>" \
                "   </tr>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <th colspan='3' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>Vacacion Nro</th>" \
                "       <th colspan='2' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>Gestion</th>" \
                "       <th colspan='1' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>Tipo</th>" \
                "       <th colspan='3' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>Descripcion</th>" \
                "       <th colspan='1' scope='colgroup' align='left' style='padding-left: 4px; padding-top: 3px; padding-bottom: 3px'>Dias</th>" \
                "   </tr>" \
                "" + detalleGestion + "" \
                                      "</table>"

        html += "" \
                "<table align='center' style='padding: 4px; border: 0px solid grey' width='100%'>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <td width='30%' colspan='4' align='left' style='padding-left: 4px; padding-top: 5px'><font size=3><i class='format' ></i>VºBº </font></td>" \
                "       <td width='30%' colspan='4' align='left' style='padding-left: 4px; padding-top: 5px'><font size=3><i class='format'></i>Autorizado por:</font></td>" \
                "   </tr>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <td width='30%' colspan='4' align='left' ><font size=3><i class='format'></i></br> </br> &nbsp;&nbsp;_________________________</br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GERENTE/JEFE UNIDAD STAFF</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;" + aprobacion + "</br>&nbsp;&nbsp;&nbsp;&nbsp;</br></font></td>" \
                                                                                                                                                                                                                                                                                               "       <td width='30%' colspan='4' align='left' ><font size=3><i class='format'></i></br> </br> &nbsp;&nbsp;_________________________</br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; JEFE INMEDIATO SUPERIOR</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;" + autorizacion + "</br>&nbsp;&nbsp;&nbsp;&nbsp;</br></font></td>" \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              "       <td width='30%' colspan='4' align='left' ><font size=3><i class='format'></i></br> </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_________________________ </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TRABAJADOR</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;</br>&nbsp;&nbsp;&nbsp;&nbsp;</br></font></td>" \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              "   </tr>" \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              "</table>"

        html += "" \
                "<table align='center' style='padding: 4px; border: 0px solid grey' width='100%'>" \
                "   <tr style='font-size: 12px; border: 0px; padding: 0px'>" \
                "       <td width='30%' colspan='2' align='left' style='padding-left: 4px; padding-top: 5px'><font size=3><i class='format' ></i>c.c: 0. File Personal</br>&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp;&nbsp1. Personal</br>&nbsp;&nbsp&nbsp;&nbsp;&nbsp&nbsp;&nbsp2. Trabajador</font></td>" \
                "       <td width='30%' colspan='8' align='left' style='padding-left: 4px; padding-top: 5px; border: 1px'><font size=4><i class='format'></i>IMPORTANTE: En Caso de ser rechazado el uso de la papeleta de vacación, sirvase informar</br>en el dia a la Oficina de Personal, para no perder los dias solicitados </font></td>" \
                "       <td width='30%' colspan='2' align='left' style='padding-left: 15px; padding-top: 5px'><font size=3><i class='format'></i>G- 09 - 01/05</font></td>" \
                "   </tr>" \
                "</table>"

        nombre = "Papeleta-Vacacion.pdf"

        report.html_to_pdf(html, nombre)

        self.respond('/resources/downloads/' + nombre)
