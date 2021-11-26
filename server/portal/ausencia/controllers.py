from .managers import *
from ...common.controllers import CrudController
from ...ausencia.tipoausencia.managers import *
from ...personal.persona.managers import *
from ...asistencia.ausencia.managers import *
from ...vacaciones.historico.managers import *


import json

class PortalAusenciaController(CrudController):

    manager = PortalAusenciaManager
    html_index = "portal/ausencia/views/index.html"
    html_table = "portal/ausencia/views/table.html"
    routes = {
        '/portal_ausencia': {'GET': 'index', 'POST': 'table'},
        '/portal_ausencia_insert': {'POST': 'insert'},
        '/portal_ausencia_update': {'PUT': 'edit', 'POST': 'update'},
        '/portal_ausencia_update_superior': { 'POST': 'update_superior'},
        '/portal_ausencia_delete': {'POST': 'delete'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        idpersona = us.fkpersona

        if idpersona:
            aux['idpersona'] = idpersona
            nombrepersona = PersonaManager(self.db).obtener_persona(idpersona)
            aux['nombrepersona'] = nombrepersona.fullname

            aux['ausencias_personales'] = PortalAusenciaManager(self.db).obtener_x_persona(idpersona)
            aux['ausencias_recibidas'] = PortalAusenciaManager(self.db).obtener_x_supervisor(idpersona)
        else:
            aux['idpersona'] = 0
            aux['nombrepersona'] = "Sin Nombre"

            aux['ausencias_personales'] = PortalAusenciaManager(self.db).listar_todo()
            aux['ausencias_recibidas'] = PortalAusenciaManager(self.db).listar_todo()

        aux['personal'] = PersonaManager(self.db).listar_todo()
        aux['ausencias'] = TipoausenciaManager(self.db).listar_todo()


        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        respuesta = AusenciaManager(self.db).insert(objeto)
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
            AusenciaManager(self.db).actualizar_ausencias(respuesta)

        self.respond(success=True, message='Modificado correctamente.')

    def update_superior(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        respuesta = AusenciaManager(self.db).update_superior(objeto)

        if respuesta.estado == "Aceptado":
            if respuesta.fktipoausencia == 1:
                V_historicoManager(self.db).actualizar_vacaciones_ausencia(respuesta,diccionary['user'],diccionary['ip'])

            AusenciaManager(self.db).actualizar_ausencias(respuesta)

        self.respond(success=True, message='Modificado correctamente.')

