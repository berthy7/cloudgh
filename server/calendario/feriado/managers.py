from ...operaciones.bitacora.managers import *
from sqlalchemy.sql import func
from server.common.managers import SuperManager
from .models import *
from ...usuarios.ajustes.models import *
from ...personal.persona.models import Persona
from ...asistencia.asistenciapersonal.managers import *


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

        asistencia_personal = AsistenciaManager(self.db).obtener_localizacion(objeto)

        for asistencia in asistencia_personal:
            asistencia.observacion = objeto.nombre
            super().update(asistencia)

        return objeto





