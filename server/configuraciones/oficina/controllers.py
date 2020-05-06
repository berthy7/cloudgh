from .managers import *
from ..sucursal.managers import *
from ...common.controllers import CrudController

import json


class OficinaController(CrudController):

    manager = OficinaManager
    html_index = "configuraciones/oficina/views/index.html"
    html_table = "configuraciones/oficina/views/table.html"
    routes = {
        '/oficina': {'GET': 'index', 'POST': 'table'},
        '/oficina_insert': {'POST': 'insert'},
        '/oficina_update': {'PUT': 'edit', 'POST': 'update'},
        '/oficina_delete': {'POST': 'delete'},

        '/listar_x_sucursal': {'POST': 'listar_x_sucursal'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['sucursal'] = SucursalManager(self.db).listar_todo()

        return aux

    def listar_x_sucursal(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = OficinaManager(self.db).listar_x_sucursal(data['idsucursal'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        OficinaManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        OficinaManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip

        result = OficinaManager(self.db).delete(id,estado, user, ip)

        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')

