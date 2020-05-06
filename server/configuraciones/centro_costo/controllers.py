from .managers import *
from ...common.controllers import CrudController

import json


class Centro_costoController(CrudController):

    manager = Centro_costoManager
    html_index = "configuraciones/centro_costo/views/index.html"
    html_table = "configuraciones/centro_costo/views/table.html"
    routes = {
        '/centro_costo': {'GET': 'index', 'POST': 'table'},
        '/centro_costo_insert': {'POST': 'insert'},
        '/centro_costo_update': {'PUT': 'edit', 'POST': 'update'},
        '/centro_costo_delete': {'POST': 'delete'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        Centro_costoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        Centro_costoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = Centro_costoManager(self.db).delete(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')