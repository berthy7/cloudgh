from .managers import *
from ...personal.persona.managers import *
from ...common.controllers import CrudController
from ..horario.managers import *

import json


class AsignacionController(CrudController):

    manager = PeriodoManager
    html_index = "asistencia/asignacion/views/index.html"
    html_table = "asistencia/asignacion/views/table.html"
    routes = {
        '/asignacion': {'GET': 'index', 'POST': 'table'},
        '/asignacion_insert': {'POST': 'insert'},
        '/asignacion_update': {'PUT': 'edit', 'POST': 'update'},
        '/asignacion_delete': {'POST': 'delete'},
        '/asignacion_importar': {'POST': 'importar'}

    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['select_semanal'] = SemanalManager(self.db).listar_todo()
        aux['admin'] = PersonaManager(self.db).get_employees_tree()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PeriodoManager(self.db).insert(objeto)

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PeriodoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
