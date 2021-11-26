from ...personal.persona.managers import *
from ..asistenciapersonal.managers import *
from ..horario.managers import *
from ..asignacion.managers import *
from ...common.controllers import CrudController
from xhtml2pdf import pisa
import os.path
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

class AsistenciaController(CrudController):

    manager = AsistenciaManager
    html_index = "asistencia/asistenciapersonal/views/index.html"
    html_table = "asistencia/asistenciapersonal/views/table.html"
    routes = {
        '/asistenciapersonal': {'GET': 'index', 'POST': 'table'},
        '/asistenciapersonal_insert': {'POST': 'insert'},
        '/asistenciapersonal_insertseg': {'POST': 'insert_seg'},
        '/asistenciapersonal_update': {'PUT': 'edit', 'POST': 'update'},
        '/asistenciapersonal_delete': {'POST': 'delete'},
        '/asistenciapersonal_importar': {'POST': 'importar'},
        '/asistenciapersonal_filtrar': {'POST': 'filtrar'},
        '/asistenciapersonal_actualizar_marcaciones': {'POST': 'actualizar_marcaciones'},
        '/asistenciapersonal_boleta_pdf': {'POST': 'boleta_pdf'},
        '/asistenciapersonal_reporte_total': {'POST': 'reporte_total'},
        '/asistenciapersonal_remove': {'POST': 'remove'},
        '/asistenciapersonal_listar_persona': {'POST': 'listar_x_persona'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['select_semanal'] = SemanalManager(self.db).listar_todo()
        aux['admin'] = PersonaManager(self.db).get_employees_tree()
        aux['horarios'] = AsistenciaManager(self.db).listar_por_dia()
        aux['personal'] = PersonaManager(self.db).listar_todo()
        aux['sucursales'] = SucursalManager(self.db).listar_todo()
        aux['personales'] = PersonaManager(self.db).listar_todo()
        aux['periodos'] = PeriodoManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        fechainicio = diccionary['fechainicio']
        fechafin = diccionary['fechafin']
        fechainicio = datetime.strptime(fechainicio, '%d/%m/%Y')
        fechafin = datetime.strptime(fechafin, '%d/%m/%Y')
        ins_manager = self.manager(self.db)
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip

        if diccionary['fkperiodo'] == "":

            if len(diccionary['personas']) == 0:

                ins_manager.crear_horarios(fechainicio,fechafin,None)

            else:
                for per in diccionary['personas']:
                    ins_manager.crear_horarios(fechainicio, fechafin, per)
        else:
            asignaciones = self.db.query(Asignacion).filter(Asignacion.fkperiodo == diccionary['fkperiodo']).all()

            for per in asignaciones:
                ins_manager.crear_horarios(fechainicio, fechafin, per.fkpersona)

            for per in diccionary['personas']:
                ins_manager.crear_horarios(fechainicio, fechafin, per)

        indicted_object = ins_manager.filtrar(fechainicio, fechafin, None)
        self.respond(indicted_object, message='Operacion exitosa!')
        self.db.close()

    def insert_seg(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        AsistenciaManager(self.db).insert(diccionary['user'], diccionary['ip'])

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PeriodoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def filtrar(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))

        ins_manager = self.manager(self.db)
        fechainicio = datetime.strptime(data['fechainicio'], '%d/%m/%Y')
        fechafin = datetime.strptime(data['fechafin'], '%d/%m/%Y')
        indicted_object = ins_manager.filtrar(fechainicio, fechafin,data['fksucursal'])

        self.respond(indicted_object, message='Operacion exitosa!')

        self.db.close()

    def actualizar_marcaciones(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        fechainicio = datetime.strptime(diccionary['fechainicio'], '%d/%m/%Y')
        fechafin = datetime.strptime(diccionary['fechafin'], '%d/%m/%Y')
        ins_manager = self.manager(self.db)

        if diccionary['fkperiodo'] != "":

            asignaciones = self.db.query(Asignacion).filter(Asignacion.fkperiodo == diccionary['fkperiodo']).all()

            for per in asignaciones:
                ins_manager.asignar_marcaciones(fechainicio, fechafin, per.fkpersona)

        if len(diccionary['personas']) == 0:
            print("todas las personas")
            ins_manager.asignar_marcaciones(fechainicio, fechafin, None)

        else:
            for per in diccionary['personas']:
                ins_manager.asignar_marcaciones(fechainicio, fechafin, per)


        indicted_object = ins_manager.filtrar(fechainicio, fechafin, None)
        self.respond(indicted_object)
        self.db.close()

    def boleta_pdf(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        objetoempresa = EmpresaManager(self.db).obtener_empresa()

        if objetoempresa:
            if objetoempresa.foto1:
                logoempresa = objetoempresa.foto1
            else:
                logoempresa = "/resources/images/sinImagen.jpg"
        else:
            logoempresa = "/resources/images/sinImagen.jpg"

        html = "" \
                "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
                "<style>" \
                    ".border-own { border-left: 0px; border-right: 0px; }" \
                    ".border-own-l { border-right: 0px; }" \
                    ".border-own-r { border-left: 0px; }" \
                    "@page {size: letter portrait; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 772pt; height: 20pt; }}" \
                "</style>" \
                "<div class='container' style='font-size: 12px'>" \
                    "<div class='row'>" \
                        "<div class='col-md-4'>" \
                            "<img src='../server/common" + logoempresa + "' width='auto' height='75'>" \
                        "</div>" \
                    "</div>" \
                "</div>"

        repetidos = set(diccionary['personas_arbol']).intersection(diccionary['personas'])

        for rep in repetidos:
            diccionary['personas'].remove(rep)

        for per in diccionary['personas']:
            diccionary['personas_arbol'].append(per)

        personas_lista = set(diccionary['personas_arbol'])

        for per in personas_lista:
            persona_horario = self.db.query(Asignacion).filter(Asignacion.fkpersona == per).first()

            if persona_horario:
                html = AsistenciaManager(self.db).crear_pdf(per, diccionary, html)

        nombre = "Boleta_Asistencia.pdf"

        report.html_to_pdf(html, nombre)
        self.respond('/resources/downloads/' + nombre)

    def reporte_total(self):
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

        html = "<meta http-equiv='Content-Type' content='text/html'; charset='utf-8' />" \
                "<style>" \
                    ".border-own { border-left: 0px; border-right: 0px; }" \
                    ".border-own-l { border-right: 0px; }" \
                    ".border-own-r { border-left: 0px; }" \
                    "table th { background-color: #1976d2; color: white; }" \
                    "@page {size: letter portrait; margin: 1cm; @frame footer_frame {-pdf-frame-content: footer_content; left: 50pt; width: 512pt; top: 772pt; height: 20pt; }}" \
                "</style>" \
                "<div class='container' style='font-size: 12px'>" \
                    "<div class='row'>" \
                        "<div class='col-md-4'>" \
                            "<img src='../server/common" + logoempresa + "' width='auto' height='75'>" \
                        "</div>" \
                    "</div>" \
                "</div>" \
               "<div class='container' style='font-size: 12px'>" \
                    "<div class='row'>" \
                        "<div class='col-md-4'>" \
                            "<h6 align='center'>REPORTE DÍAS/HORAS ACUMULADAS</h6>" \
                        "</div>" \
                    "</div>" \
                "</div>"

        repetidos = set(diccionary['personas_arbol']).intersection(diccionary['personas'])

        for rep in repetidos:
            diccionary['personas'].remove(rep)

        for per in diccionary['personas']:
            diccionary['personas_arbol'].append(per)

        personas_lista = set(diccionary['personas_arbol'])


        for per in personas_lista:

            persona_horario = self.db.query(Asignacion).filter(Asignacion.fkpersona == per).first()
            if persona_horario:
                detalle += AsistenciaManager(self.db).crear_reporte(per, diccionary)


        html += "<table align='center' style='padding: 4px; border: 1px solid grey' width='100%'>" \
                    "<tr style='font-size: 11px'>" \
                        "<th colspan='2' scope='colgroup'>NOMBRE </th>" \
                        "<th colspan='1' scope='colgroup'>HORAS DE ATRASO </th>" \
                        "<th colspan='1' scope='colgroup'>HORAS TRABAJADAS </th>" \
                        "<th colspan='1' scope='colgroup'>HORAS EXTRAS </th>" \
                        "<th colspan='1' scope='colgroup'>HORAS NOCTURNAS </th>" \
                        "<th colspan='1' scope='colgroup'>FALTAS </th>" \
                        "<th colspan='2' scope='colgroup'>VACACIONES </th>" \
                    "</tr>" \
                    "" + detalle + "" \
               "</table>"

        nombre = "Reporte_Totales.pdf"

        report.html_to_pdf(html, nombre)
        self.respond('/resources/downloads/' + nombre)

    def remove(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip
            self.manager(self.db).remover_marcaciones(diccionary)

            self.respond(success=True, message='Registros eliminados correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()


    def listar_x_persona(self):
        self.set_session()

        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = AsistenciaManager(self.db).listar_x_persona(data['idPersona'],data['fecha'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()