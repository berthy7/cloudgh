from .managers import *
from ...common.controllers import CrudController

import json


class TurnoController(CrudController):

    manager = DiaManager
    html_index = "asistencia/turno/views/index.html"
    html_table = "asistencia/turno/views/table.html"
    routes = {
        '/turno': {'GET': 'index', 'POST': 'table'},
        '/turno_insert': {'POST': 'insert'},
        '/turno_update': {'PUT': 'edit', 'POST': 'update'},
        '/turno_delete': {'POST': 'delete'},
        '/turno_importar': {'POST': 'importar'},
        '/turno_sms': {'POST': 'sms'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        diccionary['id'] = None
        objeto = self.manager(self.db).entity(**diccionary)
        DiaManager(self.db).insert(objeto)

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        DiaManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def sms(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        DiaManager(self.db).sms(diccionary['telefono'],diccionary['texto'])
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = DiaManager(self.db).delete(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')
