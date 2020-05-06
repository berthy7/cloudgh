from .managers import *
from ...common.controllers import CrudController

import json


class V_antiguedadController(CrudController):

    manager = V_antiguedadManager
    html_index = "vacaciones/antiguedad/views/index.html"
    html_table = "vacaciones/antiguedad/views/table.html"
    routes = {
        '/v_antiguedad': {'GET': 'index', 'POST': 'table'},
        '/v_antiguedad_insert': {'POST': 'insert'},
        '/v_antiguedad_update': {'PUT': 'edit', 'POST': 'update'},
        '/v_antiguedad_delete': {'POST': 'delete'},

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
        V_antiguedadManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        V_antiguedadManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip

        result = V_antiguedadManager(self.db).delete(id, estado, user, ip)

        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')