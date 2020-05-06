from ...configuraciones.empresa.models import *
from server.common.managers import SuperManager
from .models import *


class PoliticasManager(SuperManager):
    def __init__(self, db):
        super().__init__(Politicas,db)


    def actualizar_politicas(self):
        empresa = self.db.query(Empresa).all()
        for emp in empresa:
            politica = self.db.query(self.entity).filter(self.entity.fkempresa == emp.id).first()
            if politica is None:
                pol = Politicas(fkempresa=emp.id)
                super().insert(pol)

