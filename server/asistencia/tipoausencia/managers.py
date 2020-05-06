from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *


class TipoausenciaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Tipoausencia, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Tipoausencia.",
                     fecha=fecha, tabla="rrhh_Tipoausencia", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Tipoausencia.",
                     fecha=fecha, tabla="rrhh_Tipoausencia", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Tipoausencia.", fecha=fecha,
                     tabla="rrhh_Tipoausencia", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x
