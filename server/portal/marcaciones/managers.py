from server.common.managers import SuperManager
from ...operaciones.bitacora.managers import BitacoraManager
from ...operaciones.bitacora.models import *
from ...personal.persona.models import *
from ...asistencia.asistenciapersonal.models import *
from ...usuarios.ajustes.models import *
from .models import *
from sqlalchemy.sql import func

from datetime import datetime, timedelta, time, date

import pytz


class PortalMarcacionesManager(SuperManager):

    def __init__(self, db):
        super().__init__(Asistencia, db)

    def listar_dia_persona(self,fkpersona):
        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha = fecha_zona
        fechahoy = str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)
        fechahoy = datetime.strptime(fechahoy, '%d/%m/%Y')

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            if fkpersona:

                objeto = self.db.query(self.entity).filter(self.entity.fkpersona == fkpersona).filter(func.to_date(self.entity.fecha).between(fechahoy, fechahoy)).order_by(
                self.entity.mentrada.asc()).all()
            else:
                objeto = self.db.query(self.entity).filter(func.to_date(self.entity.fecha).between(fechahoy, fechahoy)).order_by(
                    self.entity.mentrada.asc()).all()
        else:
            # version postgres
            if fkpersona:

                objeto = self.db.query(self.entity).filter(self.entity.fkpersona == fkpersona).filter(
                    func.date(self.entity.fecha) == fechahoy).order_by(
                    self.entity.mentrada.asc()).all()
            else:
                objeto = self.db.query(self.entity).filter(func.date(self.entity.fecha) == fechahoy).order_by(
                    self.entity.mentrada.asc()).all()

        return objeto

    def filtrar(self, fechainicio, fechafin,fkpersona):
        list = {}
        c = 0

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            if fkpersona:
                objeto = self.db.query(self.entity).filter(self.entity.fkpersona == fkpersona).filter(
                    func.to_date(self.entity.fecha).between(fechainicio, fechafin)).order_by(
                    self.entity.nombrecompleto.asc()).all()

            else:
                objeto = self.db.query(self.entity).filter(
                    func.to_date(self.entity.fecha).between(fechainicio, fechafin)).order_by(
                    self.entity.nombrecompleto.asc()).all()
        else:
            # version postgres
            if fkpersona:
                objeto = self.db.query(self.entity).filter(self.entity.fkpersona == fkpersona).filter(
                    func.date(self.entity.fecha).between(fechainicio, fechafin)).order_by(
                    self.entity.nombrecompleto.asc()).all()

            else:
                objeto = self.db.query(self.entity).filter(
                    func.date(self.entity.fecha).between(fechainicio, fechafin)).order_by(
                    self.entity.nombrecompleto.asc()).all()

        for x in objeto:
            if x.mentrada:
                mentrada = x.mentrada.strftime("%H:%M:%S")
            else:
                mentrada = "------"

            if x.msalida:
                msalida = x.msalida.strftime("%H:%M:%S")
            else:
                msalida = "------"

            if x.retraso:
                retraso = x.retraso.strftime("%H:%M:%S")
            else:
                retraso = "------"

            if x.extra:
                extra = x.extra.strftime("%H:%M:%S")
            else:
                extra = "------"

            list[c] = dict(id=x.id, codigo=x.codigo, nombre=x.nombrecompleto, fecha=x.fecha.strftime("%d/%m/%Y"),
                           entrada=x.entrada.strftime("%H:%M"),salida=x.salida.strftime("%H:%M"),
                           mentrada=mentrada, msalida=msalida, observacion=x.observacion, retraso=retraso, extra=extra)
            c = c + 1

        return list
