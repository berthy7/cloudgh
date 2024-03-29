from ...operaciones.bitacora.managers import *
from ...configuraciones.empresa.managers import EmpresaManager
from ...asistencia.asistenciapersonal.models import *
from ...asistencia.tipoausencia.models import *
from ...asistencia.ausencia.models import *
from ...usuarios.ajustes.models import *
from ...personal.organigrama.managers import *
from ...notificaciones.correo.managers import *



from server.common.managers import SuperManager

from .models import *

from sqlalchemy.sql import func, and_
from datetime import datetime


class PortalAsistenciaManager(SuperManager):
    def __init__(self, db):
        super().__init__(AsistenciaMarcaciones, db)


    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def listar_todo_persona(self,idpersona):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkpersona == idpersona).all()

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)

        idsuperior = CorreoManager(self.db).notificar_ausencia(objeto)

        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Ubicacion personal.",
                     fecha=fecha, tabla="cb_asistencia_ausencia", identificador=a.id)
        super().insert(b)


        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fechai = datetime.strptime(objeto.fechai, '%d/%m/%Y')
        objeto.fechaf = datetime.strptime(objeto.fechaf, '%d/%m/%Y')

        if objeto.horai == "":
            objeto.horai = None
        else:
            objeto.horai = datetime.strptime('01/01/2000 ' + objeto.horai, '%d/%m/%Y %H:%M')

        if objeto.horaf == "":
            objeto.horaf = None
        else:
            objeto.horaf = datetime.strptime('01/01/2000 ' + objeto.horaf, '%d/%m/%Y %H:%M')

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Ausencia.",
                     fecha=fecha, tabla="cb_asistencia_ausencia", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Ausencia.", fecha=fecha,
                     tabla="cb_asistencia_ausencia", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()


    def actualizar_ausencias(self, objeto):

        fechas = BitacoraManager(self.db).rango_fechas(objeto.fechai, objeto.fechaf)

        for fech in fechas:
            fecha_hoy = fech.date()

            ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == objeto.fkpersona).filter(func.to_date(Asistencia.fecha).between(fecha_hoy, fecha_hoy)).all()

            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == objeto.fkpersona).filter(
                    func.date(Asistencia.fecha) == fecha_hoy).all()

            for asistencia in asistencia_personal:
                tipoausencia = self.db.query(Tipoausencia).filter(Tipoausencia.id == objeto.fktipoausencia).first()
                asistencia.observacion = tipoausencia.nombre
                super().update(asistencia)

        return objeto