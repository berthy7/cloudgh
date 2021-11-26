from .managers import *
from ...common.controllers import CrudController
from ...asistencia.tipoausencia.managers import *
from ...personal.persona.managers import *
from ...asistencia.ausencia.managers import *
from ...vacaciones.historico.managers import *
from ...asistencia.asistenciapersonal.managers import *

# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
# import face_recognition

import json


class PortalAsistenciaController(CrudController):

    manager = PortalAsistenciaManager
    html_index = "portal/asistencia/views/index.html"
    html_table = "portal/asistencia/views/table.html"
    routes = {
        '/portal_asistencia': {'GET': 'index', 'POST': 'table'},
        '/portal_asistencia_insert': {'PUT': 'insert'},
        '/portal_asistencia_update': {'POST': 'update'},
        '/portal_coordenadas_insert': {'POST': 'insert_coordenadas'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        idpersona = us.fkpersona

        if idpersona:
            aux['idpersona'] = idpersona
            nombrepersona = PersonaManager(self.db).obtener_persona(idpersona)
            aux['nombrepersona'] = nombrepersona.fullname
            aux['fotopersona'] = nombrepersona.empleado[0].foto

        else:
            aux['idpersona'] = 0
            aux['nombrepersona'] = "Sin Nombre"
            aux['fotopersona'] = "Sin Foto"


        aux['personal'] = PersonaManager(self.db).listar_todo()
        aux['asistencia_personal'] = PortalAsistenciaManager(self.db).listar_todo_persona(idpersona)


        return aux

    def insert_coordenadas(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        CoordenadasManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = AsistenciaMarcacionesManager(self.db).entity(**diccionary)
        AsistenciaMarcacionesManager(self.db).insert_asistencia_home2(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip


        respuesta = AsistenciaMarcacionesManager(self.db).insert_asistencia_home(diccionary)

        respuesta = dict(respuesta=respuesta)


        self.respond(respuesta)
        self.db.close()

    # def update(self):
    #     self.set_session()
    #     diccionary = json.loads(self.get_argument("object"))
    #     diccionary['user'] = self.get_user_id()
    #     diccionary['ip'] = self.request.remote_ip
    #     objeto = self.manager(self.db).entity(**diccionary)
    #     respuesta = AusenciaManager(self.db).update(objeto)
    #
    #     if respuesta.estado == "Aceptado":
    #         AusenciaManager(self.db).actualizar_ausencias(respuesta)
    #
    #     self.respond(success=True, message='Modificado correctamente.')
