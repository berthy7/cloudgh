from .managers import *
from ...common.controllers import CrudController

import json


class V_historicoController(CrudController):

    manager = V_historicoManager
    html_index = "vacaciones/historico/views/index.html"
    html_table = "vacaciones/historico/views/table.html"
    routes = {
        '/v_historico': {'GET': 'index', 'POST': 'table'},
        '/v_historico_insert': {'POST': 'insert'},
        '/v_historico_update': {'PUT': 'edit', 'POST': 'update'},
        '/v_historico_delete': {'POST': 'delete'},

        '/listar_x_ciudad': {'POST': 'listar_x_ciudad'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        return aux

    def listar_x_ciudad(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        arraT = self.manager(self.db).get_page(1, 10, None, None, True)
        arraT['objeto'] = V_historicoManager(self.db).listar_x_ciudad(data['idciudad'])
        self.respond([item.get_dict() for item in arraT['objeto']])
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        V_historicoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        V_historicoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip

        result = V_historicoManager(self.db).delete(id, estado, user, ip)

        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')