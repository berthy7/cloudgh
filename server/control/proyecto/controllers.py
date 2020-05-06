from .managers import *
from ...control.tarea.managers import *
from ...common.controllers import CrudController
from ...asistencia.asistenciapersonal.managers import *
from ...personal.persona.managers import *

import json


class ProyectoController(CrudController):

    manager = ProyectoManager
    html_index = "control/proyecto/views/index.html"
    html_table = "control/proyecto/views/table.html"
    routes = {
        '/proyecto': {'GET': 'index', 'POST': 'table'},
        '/proyecto_insert': {'POST': 'insert'},
        '/proyecto_update': {'PUT': 'edit', 'POST': 'update'},
        '/proyecto_delete': {'POST': 'delete'},
        '/proyecto_create': {'POST': 'create'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['personas'] = PersonaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        ProyectoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        ProyectoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')


