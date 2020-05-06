from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *


class CiudadManager(SuperManager):

    def __init__(self, db):
        super().__init__(Ciudad, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def listar_x_departamento(self,iddepartamento):
        return self.db.query(self.entity).filter(self.entity.fkdepartamento == iddepartamento).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Ciudad.", fecha=fecha,
                     tabla="rrhh_ciudad", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Ciudad.", fecha=fecha,
                     tabla="rrhh_ciudad", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Ciudad.", fecha=fecha, tabla="rrhh_ciudad",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x
