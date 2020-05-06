from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *


class AjustesManager(SuperManager):

    def __init__(self, db):
        super().__init__(Ajustes, db)

    def obtener_ajuste(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pais.", fecha=fecha,tabla="rrhh_pais", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pais.", fecha=fecha,tabla="rrhh_pais", identificador=a.id)
        super().insert(b)
        return a

