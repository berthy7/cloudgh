from .managers import *
from ...common.controllers import CrudController
from ...personal.persona.managers import *

import json


class CorreoController(CrudController):

    manager = CorreoManager
    html_index = "notificaciones/correo/views/index.html"
    html_table = "notificaciones/correo/views/table.html"
    routes = {
        '/correo': {'GET': 'index', 'POST': 'table'},
        '/correo_insert': {'PUT': 'correos', 'POST': 'insert'},
        '/correo_update': {'PUT': 'edit', 'POST': 'update'},
        '/correo_delete': {'POST': 'delete_correo'},
        '/correo_dias': {'POST': 'actualizar_dias'},
        '/correo_hora': {'PUT': 'edit', 'POST': 'update_hora'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['personal'] = PersonaManager(self.db).listar_todo()
        aux['hora_notificacion'] = CorreoManager(self.db).obtener_servidor()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        CorreoManager(self.db).update(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        CorreoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtener_servidor()
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def correos(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        indicted_object = ins_manager.obtener_servidor()
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def actualizar_dias(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        state = json.loads(self.get_argument("enabled"))
        updated_object = self.manager(self.db).actualizacion_dias(id, state)
        if state:
            message = "Dia dado de Alta!"
        else:
            message = "Dia dado de Baja!"
        self.respond(updated_object.get_dict(), message=message)
        self.db.close()

    def delete_correo(self):
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

    def update_hora(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).obtener_servidor()
        objeto.hora = datetime.strptime('01/01/2000 '+diccionary['hora'], '%d/%m/%Y %H:%M')
        CorreoManager(self.db).update_hora(objeto,diccionary['user'],diccionary['ip'])
        self.respond(success=True, message='Modificado correctamente.')
