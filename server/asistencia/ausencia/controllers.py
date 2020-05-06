from .managers import *
from ...common.controllers import CrudController
from ...asistencia.tipoausencia.managers import *
from ...personal.persona.managers import *
from ...vacaciones.historico.managers import *


import json

class AusenciaController(CrudController):

    manager = AusenciaManager
    html_index = "asistencia/ausencia/views/index.html"
    html_table = "asistencia/ausencia/views/table.html"
    routes = {
        '/ausencia': {'GET': 'index', 'POST': 'table'},
        '/ausencia_insert': {'POST': 'insert'},
        '/ausencia_update': {'PUT': 'edit', 'POST': 'update'},
        '/ausencia_delete': {'POST': 'delete'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['ausencias'] = TipoausenciaManager(self.db).listar_todo()
        aux['personal'] = PersonaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip

        objeto = self.manager(self.db).entity(**diccionary)
        respuesta = AusenciaManager(self.db).insert(objeto)


        if respuesta is None:
            # None significa que no tiene padre
            print(respuesta)
            self.respond(success=False, message='No se insertó su ausencia.')
        else:
            if respuesta.estado == "Aceptado":
                AusenciaManager(self.db).actualizar_ausencias(respuesta)
            self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        respuesta = AusenciaManager(self.db).update(objeto)

        if respuesta.estado == "Aceptado":
            if respuesta.fktipoausencia == "1":
                V_historicoManager(self.db).actualizar_vacaciones_ausencia(respuesta,diccionary['user'],diccionary['ip'])
            AusenciaManager(self.db).actualizar_ausencias(respuesta)

        self.respond(success=True, message='Modificado correctamente.')