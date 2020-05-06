from .managers import *
from ...common.controllers import CrudController

import json


class AjustesController(CrudController):

    manager = AjustesManager
    html_index = "usuarios/ajustes/views/index.html"
    html_table = "usuarios/ajustes/views/table.html"
    routes = {
        '/ajustes': {'GET': 'index', 'POST': 'table'},
        '/ajustes_insert': {'POST': 'insert'},
        '/ajustes_update': {'PUT': 'edit', 'POST': 'update'},
        '/ajustes_delete': {'POST': 'delete'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['ajuste'] = AjustesManager(self.db).obtener_ajuste()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        AjustesManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        objeto.id = 1
        AjustesManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
