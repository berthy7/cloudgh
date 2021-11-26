from .managers import *
from ...common.controllers import CrudController
from ...personal.persona.managers import *
from ..correo.managers import *

import json


class CorreorrhhController(CrudController):

    manager = CorreorrhhManager
    html_index = "notificaciones/correo_rrhh/views/index.html"
    html_table = "notificaciones/correo_rrhh/views/table.html"
    routes = {
        '/correo_rrhh': {'GET': 'index', 'POST': 'table'},
        '/correo_rrhh_insert': {'PUT': 'correos', 'POST': 'insert'},
        '/correo_rrhh_update': {'PUT': 'edit', 'POST': 'update'},
        '/correo_rrhh_delete': {'POST': 'delete'},

    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['personal'] = PersonaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip

        for correo in diccionary['correos']:

            persona_correo = self.db.query(Correorrhh).filter(Correorrhh.fkpersona == correo['fkpersona']).first()
            if persona_correo is None:

                diccionary['fkpersona'] = correo['fkpersona']
                objeto = self.manager(self.db).entity(**diccionary)
                CorreorrhhManager(self.db).insert(objeto)

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        CorreorrhhManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        self.verif_privileges()
        id = json.loads(self.get_argument("id"))
        state = json.loads(self.get_argument("enabled"))
        updated_object = self.manager(self.db).delete(id, state)
        if state:
            message = "Correo dado de Alta!"
        else:
            message = "Correo dado de Baja!"
        self.respond(updated_object.get_dict(), message=message)
        self.db.close()
