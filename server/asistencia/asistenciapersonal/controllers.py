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
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['select_semanal'] = SemanalManager(self.db).listar_todo()
        aux['admin'] = PersonaManager(self.db).get_employees_tree()
        aux['horarios'] = AsistenciaManager(self.db).listar_por_dia()
        aux['personal'] = PersonaManager(self.db).listar_todo()

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
        ins_manager.crear_horarios(fechainicio,fechafin)
        arraT = ins_manager.get_page(1, 10, None, None, True)
        arraT['datos'] = ins_manager.listar_por_dia()
        self.respond([objeto_regreso.get_dict() for objeto_regreso in arraT['datos']])
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
        fechainicio = data['fechainicio']
        fechafin = data['fechafin']

        ins_manager = self.manager(self.db)
        indicted_object = ins_manager.filtrar(fechainicio, fechafin)
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object, message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def actualizar_marcaciones(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        fechainicio = diccionary['fechainicio']
        fechafin = diccionary['fechafin']
        ins_manager = self.manager(self.db)
        indicted_object = ins_manager.asignar_marcaciones(fechainicio,fechafin)
        arraT = ins_manager.get_page(1, 10, None, None, True)
        arraT['datos'] = ins_manager.listar_por_dia()
        self.respond([objeto_regreso.get_dict() for objeto_regreso in arraT['datos']])
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
        for per in diccionary['personas']:
           html = AsistenciaManager(self.db).crear_pdf(per,diccionary,html)

        for per in diccionary['personas_arbol']:
           html = AsistenciaManager(self.db).crear_pdf(per,diccionary,html)

        nombre = "Boleta_Asistencia.pdf"

        report.html_to_pdf(html, nombre)
        self.respond('/resources/downloads/' + nombre)



