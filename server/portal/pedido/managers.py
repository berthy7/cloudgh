from ...operaciones.bitacora.managers import *
from .models import *
from ...comensales.pedido.models import *

from sqlalchemy.sql import func
from server.common.managers import SuperManager


class PortalPedidoManager(SuperManager):

    def __init__(self, db):
        super().__init__(Pedido, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def pedido_dia(self,hoy):
        hoy = datetime.strptime(hoy, '%d/%m/%Y')

        return self.db.query(self.entity).filter(func.DATE(self.entity.fecha) == hoy).filter(self.entity.enabled == True)

    def listar_x_persona(self,fkpersona):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkpersona== fkpersona).order_by(self.entity.fecha.desc()).all()

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pedido.", fecha=fecha,
                     tabla="rrhh_pedido", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pedido.", fecha=fecha,
                     tabla="rrhh_pedido", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Pedido.", fecha=fecha, tabla="rrhh_pedido",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
