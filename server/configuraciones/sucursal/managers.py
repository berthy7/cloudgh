from ...operaciones.bitacora.managers import *
from ..gerencia.models import *
from server.common.managers import SuperManager
from .models import *


class SucursalManager(SuperManager):

    def __init__(self, db):
        super().__init__(Sucursal, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def obtener_gerencias(self,idempresa,idsucursal):
        list = {}
        vector = []
        c = 0

        objeto= self.db.query(self.entity).filter(self.entity.id == idsucursal).one()

        for x in objeto.empleados:
            if x.gerencia.nombre not in vector:
                vector.append(x.gerencia.nombre)

        vector.sort()
        for i in vector:
            ger = self.db.query(Gerencia).filter(Gerencia.enabled == True).filter(Gerencia.nombre == i).filter(Gerencia.fkempresa == idempresa).first()
            if ger:
                list[c] = dict(idgerencia=ger.id ,gerencia=i)
                c = c + 1

        return list

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def listar_x_ciudad(self, idciudad):
        return self.db.query(self.entity).filter(self.entity.fkciudad == idciudad).filter(
            self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Sucursal.",
                     fecha=fecha, tabla="rrhh_sucursal", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Sucursal.",
                     fecha=fecha, tabla="rrhh_sucursal", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Sucursal.", fecha=fecha,
                     tabla="rrhh_sucursal", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x
