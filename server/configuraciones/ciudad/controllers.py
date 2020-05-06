from .managers import *
from ...common.controllers import CrudController
from ..departamento.managers import *

import json


class CiudadController(CrudController):

    manager = CiudadManager
    html_index = "configuraciones/ciudad/views/index.html"
    html_table = "configuraciones/ciudad/views/table.html"
    routes = {
        '/ciudad': {'GET': 'index', 'POST': 'table'},
        '/ciudad_insert': {'POST': 'insert'},
        '/ciudad_update': {'PUT': 'edit', 'POST': 'update'},
        '/ciudad_delete': {'POST': 'delete'},

        '/listar_x_departamento': {'POST': 'listar_x_departamento'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['departamento'] = DepartamentoManager(self.db).listar_todo()

        return aux

    def listar_x_departamento(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = CiudadManager(self.db).listar_x_departamento(data['iddepartamento'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        CiudadManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        CiudadManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = CiudadManager(self.db).delete(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')