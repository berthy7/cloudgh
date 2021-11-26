from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *

from ...operaciones.bitacora.managers import *
from ...configuraciones.empresa.managers import EmpresaManager
from ...asistencia.asistenciapersonal.models import *
from ...asistencia.tipoausencia.models import *
from ...usuarios.ajustes.models import *
from ...personal.organigrama.managers import *
from ...notificaciones.correo.managers import *
from ...calendario.feriado.managers import *

from sqlalchemy.sql import func, and_
from datetime import datetime


class TipoausenciaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Tipoausencia, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def obtener(self,idtipoausencia):
        return self.db.query(self.entity).filter(self.entity.id == idtipoausencia).filter(self.entity.enabled == True).first()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def listar_permisos(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.tipo == "Permiso").order_by(self.entity.nombre.asc()).all()

    def listar_licencias(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.tipo == "Licencia").order_by(self.entity.nombre.asc()).all()

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Tipoausencia.",
                     fecha=fecha, tabla="cb_ausencia_tipoausencia", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Tipoausencia.",
                     fecha=fecha, tabla="cb_ausencia_tipoausencia", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Tipoausencia.", fecha=fecha,
                     tabla="cb_ausencia_tipoausencia", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def get_type_data(self):
        list = dict()
        for t in self.db.query(self.entity).filter(self.entity.enabled == True).all():
            list[t.nombre] = dict(nombre=t.nombre, tipo=t.tipo, duracion=t.duracion, selec_duracion=t.selec_duracion, total=0)

        return list

    def obtener_ausencia(self, fkpersona, fecha):
        respuesta = ""

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            solicitud = self.db.query(Ausencia).filter(Ausencia.fkpersona == fkpersona) \
                .filter(Ausencia.estadoaprobacion == "Aceptado") \
                .filter(and_(func.to_date(Ausencia.fechai) <= fecha, func.to_date(Ausencia.fechaf) >= fecha)).first()

        else:

            # version postgres
            solicitud = self.db.query(Ausencia).filter(Ausencia.fkpersona == fkpersona) \
                .filter(Ausencia.estadoaprobacion == "Aceptado") \
                .filter(and_(func.date(Ausencia.fechai) <= fecha, func.date(Ausencia.fechaf) >= fecha)).first()


        if solicitud:
            respuesta = solicitud.tipoausencia.nombre

        return respuesta
