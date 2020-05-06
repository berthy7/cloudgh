from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *


class OficinaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Oficina, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def listar_x_sucursal(self, idsurcusal):
        return self.db.query(self.entity).filter(self.entity.fksucursal == idsurcusal).filter(
            self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Oficina.", fecha=fecha,tabla="rrhh_oficina", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Oficina.", fecha=fecha,tabla="rrhh_oficina", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id,estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Oficina.", fecha=fecha, tabla="rrhh_oficina", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return x
