from .managers import *
from ...dispositivos.lectores.managers import *
from ...configuraciones.sucursal.managers import *
from ...common.controllers import CrudController

import json


class PortalMarcacionesController(CrudController):

    manager = PortalMarcacionesManager
    html_index = "portal/marcaciones/views/index.html"
    html_table = "portal/marcaciones/views/table.html"
    routes = {
        '/portal_marcaciones': {'GET': 'index', 'POST': 'table'},
        '/portal_marcaciones_insert': {'POST': 'insert'},
        '/portal_marcaciones_update': {'PUT': 'edit', 'POST': 'update'},
        '/portal_marcaciones_delete': {'POST': 'delete'},
        '/portal_marcaciones_filtrar': {'POST': 'filtrar'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        user = self.get_user()
        fkpersona = user.fkpersona

        aux['sucursales'] = SucursalManager(self.db).listar_todo()
        aux['horarios'] = PortalMarcacionesManager(self.db).listar_dia_persona(fkpersona)

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip_maquina'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PortalMarcacionesManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PortalMarcacionesManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def filtrar(self):
        self.set_session()
        user = self.get_user()
        fkpersona = user.fkpersona
        data = json.loads(self.get_argument("object"))
        fechainicio = data['fechainicio']
        fechafin = data['fechafin']

        ins_manager = self.manager(self.db)
        indicted_object = ins_manager.filtrar(fechainicio, fechafin,fkpersona)
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object, message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()
