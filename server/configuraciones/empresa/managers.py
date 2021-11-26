from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *
from server.database.connection import transaction
from sqlalchemy.orm.session import make_transient

class EmpresaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Empresa, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def obtener_empresa(self):
        x = self.db.query(self.entity).first()

        return x

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Empresa.",
                     fecha=fecha, tabla="rrhh_empresa", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Empresa.",
                     fecha=fecha, tabla="rrhh_empresa", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Empresa.", fecha=fecha,
                     tabla="rrhh_empresa", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

class EmpresaGlobalManager:
    def get_data_empress(self):
        foto1 = '/resources/default/cloudbit/cb-hor-md.png'
        foto2 = '/resources/default/cloudbit/cb-vert-md-wh.png'
        foto3 = '/resources/default/cloudbit/cloudbit.ico'

        with transaction() as session:
            data = session.query(Empresa).first()
            if not data:
                return None
            session.expunge(data)
            make_transient(data)

            if data.foto1 not in ['S/I', ' ', None, '']:
                foto1 = data.foto1
            if data.foto2 not in ['S/I', ' ', None, '']:
                foto2 = data.foto2
            if data.foto3 not in ['S/I', ' ', None, '']:
                foto3 = data.foto3

        return {'nombre': data.nombre, 'foto1': foto1, 'foto2': foto2, 'foto3': foto3}
