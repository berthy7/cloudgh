from .managers import *
from ..empresa.managers import *
from ...common.controllers import CrudController

import json


class GerenciaController(CrudController):

    manager = GerenciaManager
    html_index = "configuraciones/gerencia/views/index.html"
    html_table = "configuraciones/gerencia/views/table.html"
    routes = {
        '/gerencia': {'GET': 'index', 'POST': 'table'},
        '/gerencia_insert': {'POST': 'insert'},
        '/gerencia_update': {'PUT': 'edit', 'POST': 'update'},
        '/gerencia_delete': {'POST': 'delete'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['empresa'] = EmpresaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        GerenciaManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        GerenciaManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
        
    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = GerenciaManager(self.db).delete(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')
