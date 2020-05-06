from ...configuraciones.sucursal.models import *
from ...operaciones.bitacora.managers import *
from ...dispositivos.marcaciones.models import *
from .models import *
from sqlalchemy.sql import func


class ProyectoManager(SuperManager):

    def __init__(self, db):
        super().__init__(Proyecto, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)