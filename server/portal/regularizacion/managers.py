from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from ...asistencia.tipoausencia.managers import *
from ...notificaciones.correo_rrhh.managers import *
from ...personal.persona.managers import *
from datetime import datetime, timedelta, time, date
from .models import *
from ...ausencia.tipoausencia.models import *
from ...usuarios.ajustes.models import *
from ...asistencia.asistenciapersonal.models import *
from sqlalchemy.sql import func, and_,or_
from sqlalchemy import extract

from server.ausencia.regularizacion.models import *


class PortalRegularizacionManager(SuperManager):

    def __init__(self, db):
        super().__init__(Regularizacion, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.id.desc())



    def obtener_x_persona(self, fkpersona):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkpersona == fkpersona).order_by(self.entity.id.desc()).all()


    def obtener_x_supervisor(self, fkpersona):
        solicitudes = self.db.query(self.entity).filter(self.entity.enabled == True).filter(or_(self.entity.fkautorizacion == fkpersona,self.entity.fkaprobacion == fkpersona)).order_by(self.entity.id.desc()).all()


        # organi_super = self.db.query(Organigrama).filter(Organigrama.enabled == True).filter(
        #     Organigrama.fkpersona == fkpersona).first()
        #
        # if organi_super:
        #     solicitudes_superior = self.db.query(self.entity).filter(self.entity.fksuperior == organi_super.fkpersona).all()
        #
        #     for soli in solicitudes_superior:
        #         solicitudes.append(soli)

        return solicitudes






