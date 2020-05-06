from .managers import *
from ...common.controllers import CrudController
from ..turno.managers import *

import json


class HorarioController(CrudController):

    manager = SemanalManager
    html_index = "asistencia/horario/views/index.html"
    html_table = "asistencia/horario/views/table.html"
    routes = {
        '/horario': {'GET': 'index', 'POST': 'table'},
        '/horario_insert': {'POST': 'insert'},
        '/horario_update': {'PUT': 'edit', 'POST': 'update'},
        '/horario_delete': {'POST': 'delete'},
        '/horario_importar': {'POST': 'importar'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['dias'] = DiaManager(self.db).litar_todo()
        aux['tabla_semanal'] = SemanalManager(self.db).tabla_semanal()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        diccionary['id'] = None
        objeto = self.manager(self.db).entity(**diccionary)
        SemanalManager(self.db).insert(objeto)

        self.respond(success=True, message='Insertado correctamente.')
