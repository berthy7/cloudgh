from .managers import *
from ...common.controllers import CrudController
from ..pais.managers import *

import json


class DepartamentoController(CrudController):

    manager = DepartamentoManager
    html_index = "configuraciones/departamento/views/index.html"
    html_table = "configuraciones/departamento/views/table.html"
    routes = {
        '/departamento': {'GET': 'index', 'POST': 'table'},
        '/departamento_insert': {'POST': 'insert'},
        '/departamento_update': {'PUT': 'edit', 'POST': 'update'},
        '/departamento_delete': {'POST': 'delete'},

        '/listar_x_pais': {'POST': 'listar_x_pais'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['pais'] = PaisManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        DepartamentoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        DepartamentoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def listar_x_pais(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = DepartamentoManager(self.db).listar_x_pais(data['idpais'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = DepartamentoManager(self.db).delete(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')
