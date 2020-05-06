from .managers import *
from ...common.controllers import CrudController

import json


class TipoausenciaController(CrudController):

    manager = TipoausenciaManager
    html_index = "asistencia/tipoausencia/views/index.html"
    html_table = "asistencia/tipoausencia/views/table.html"
    routes = {
        '/tipoausencia': {'GET': 'index', 'POST': 'table'},
        '/tipoausencia_insert': {'POST': 'insert'},
        '/tipoausencia_update': {'PUT': 'edit', 'POST': 'update'},
        '/tipoausencia_delete': {'POST': 'delete'},
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
        TipoausenciaManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        TipoausenciaManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        estado = diccionary['enabled']
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = TipoausenciaManager(self.db).delete(id, estado, user, ip)
        if result.enabled:
            self.respond(success=True, message='Alta Realizada Correctamente.')
        elif not result.enabled:    
            self.respond(success=False, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')
