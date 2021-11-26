from ...operaciones.bitacora.managers import *
from ...asistencia.asistenciapersonal.models import *
from ...personal.persona.models import *
from ...usuarios.ajustes.models import *

from sqlalchemy.sql import func
from server.common.managers import SuperManager
from .models import *



class FeriadoManager(SuperManager):

    def __init__(self, db):
        super().__init__(Feriado, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.fecha.desc()).all()

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fecha = datetime.strptime(objeto.fecha, '%d/%m/%Y')

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Feriado.", fecha=fecha,
                     tabla="cb_calendario_ferido", identificador=a.id)
        super().insert(b)

        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fecha = datetime.strptime(objeto.fecha, '%d/%m/%Y')

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Feriado.", fecha=fecha,
                     tabla="rrhh_menu", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Feriado.", fecha=fecha, tabla="cb_calendario_feriado",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def actualizar_feriado(self, objeto):

        asistencia_personal = FeriadoManager(self.db).obtener_localizacion(objeto)

        for asistencia in asistencia_personal:
            asistencia.observacion = objeto.nombre
            super().update(asistencia)

        return objeto


    def obtener_x_fecha(self,fecha):
        return self.db.query(self.entity).filter(self.entity.fecha == fecha).filter(self.entity.enabled == True).first()

    def obtener_localizacion(self, feriado):
        list = {}
        asistencia_personal = 0

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if feriado.fkpais:

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(
                    Empleado.fkpais == feriado.fkpais).filter(
                    func.to_date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(
                    Empleado.fkpais == feriado.fkpais).filter(
                    func.date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()

        if feriado.fkdepartamento:

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(
                    Empleado.fkdepartamento == feriado.fkdepartamento).filter(
                    func.to_date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(
                    Empleado.fkdepartamento == feriado.fkdepartamento).filter(
                    func.date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()

        if feriado.fkciudad:

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(
                    Empleado.fkciudad == feriado.fkciudad).filter(
                    func.to_date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(
                    Empleado.fkciudad == feriado.fkciudad).filter(
                    func.date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()

        if feriado.fksucursal:

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(
                    Empleado.fksucursal == feriado.fksucursal).filter(
                    func.to_date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(
                    Empleado.fksucursal == feriado.fksucursal).filter(
                    func.date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()

        return asistencia_personal





