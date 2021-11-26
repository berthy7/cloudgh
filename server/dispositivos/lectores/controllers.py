from .managers import *
from ...configuraciones.sucursal.managers import *
from ...common.controllers import CrudController

import json


class LectoresController(CrudController):

    manager = LectoresManager
    html_index = "dispositivos/lectores/views/index.html"
    html_table = "dispositivos/lectores/views/table.html"
    routes = {
        '/lectores': {'GET': 'index', 'POST': 'table'},
        '/lectores_insert': {'POST': 'insert'},
        '/lectores_update': {'PUT': 'edit', 'POST': 'update'},
        '/lectores_delete': {'POST': 'delete'},
        '/lectores_extraer_marcaciones': {'POST': 'extraer_marcaciones'},
        '/lectores_obtener_marcaciones': {'POST': 'obtener_marcaciones'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['sucursales'] = SucursalManager(self.db).listar_todo()

        return aux

    def extraer_marcaciones(self):
        self.set_session()
        LectoresManager(self.db).preparar_dispositivos()
        self.respond(success=True, message='Insertado correctamente.')

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip_maquina'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        LectoresManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip_maquina'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        LectoresManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def obtener_marcaciones(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        ins_manager = self.manager(self.db)
        objeto = ins_manager.obtener_dispositivo(diccionary['id'])
        respuesta = ins_manager.extraer_marcaciones(objeto)
        self.respond(success=respuesta['estado'], message=respuesta['mensaje'])
        self.db.close()

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = LectoresManager(self.db).delete(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')