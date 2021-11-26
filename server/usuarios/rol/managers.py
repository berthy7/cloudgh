from ...operaciones.bitacora.managers import *

from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func,and_,or_


class RolManager(SuperManager):
    def __init__(self, db):
        super().__init__(Rol, db)

    def listar_usuario(self,idUsuario):

        if idUsuario.username == "admin":
            x =self.db.query(Rol).filter(Rol.enabled == True).filter(Rol.nombre != "SUPER ADMINISTRADOR")
        else:
            x = self.db.query(Rol).filter(Rol.enabled == True).filter(and_(Rol.nombre != "SUPER ADMINISTRADOR",Rol.nombre != "ADMINISTRADOR"))

        return x



    def get_page(self, page_nr=1, max_entries=10, like_search=None, order_by=None, ascendant=True, query=None):
        query = self.db.query(self.entity).filter(Rol.id > 1)
        return super().get_page(page_nr, max_entries, like_search, order_by, ascendant, query)

    def insert(self, rol):
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=rol.user, ip=rol.ip, accion="Se registró un rol.", fecha=fecha)
        super().insert(b)
        a = super().insert(rol)
        return a

    def update(self, rol):
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=rol.user, ip=rol.ip, accion="Se modificó un rol.", fecha=fecha)
        super().insert(b)
        a = super().update(rol)
        return a

    def list_all(self):
        return dict(objects=self.db.query(Rol).filter(Rol.nombre != "SUPER ADMINISTRADOR").distinct())

    def get_all(self):
        return self.db.query(Rol).filter(Rol.enabled == True).filter(Rol.nombre != "SUPER ADMINISTRADOR")

    def delete_rol(self, id, enable, Usuariocr, ip):
        x = self.db.query(Rol).filter(Rol.id == id).one()
        x.enabled = enable

        if enable == True:
            message = "Se habilitó un rol."
        else:
            users = self.db.query(Usuario).filter(Usuario.enabled == True).filter(Usuario.fkrol == id).all()
            for u in users:
                u.enabled = False

            message = "Se inhabilitó un rol y usuarios relacionados."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuariocr, ip=ip, accion=message, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
