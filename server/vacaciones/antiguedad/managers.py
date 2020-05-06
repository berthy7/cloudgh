from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *


class V_antiguedadManager(SuperManager):

    def __init__(self, db):
        super().__init__(V_antiguedad, db)


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
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro V_antiguedad.",
                     fecha=fecha, tabla="cb_vacaciones_antiguedad", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico V_antiguedad.",
                     fecha=fecha, tabla="cb_vacaciones_antiguedad", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó V_antiguedad.", fecha=fecha,
                     tabla="cb_vacaciones_antiguedad", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x
