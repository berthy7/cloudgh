from sqlalchemy import Column, Integer, Boolean, Sequence, Date, String, Text, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Feriado(Serializable, Base):
    way = {'pais': {},'departamento': {},'ciudad': {},'sucursal': {}}

    __tablename__ = 'cb_calendario_feriado'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(255), nullable=False)
    fecha = Column(Date, nullable=True)

    ciclico = Column(Boolean, nullable=True, default=False)
    fijo = Column(Boolean, nullable=True, default=False)
    relativo = Column(Boolean, nullable=True, default=False)

    fkpais = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_pais.id'), nullable=True)
    fkdepartamento = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_departamento.id'), nullable=True)
    fkciudad = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_ciudad.id'), nullable=True)
    fksucursal = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_sucursal.id'), nullable=True)
    enabled = Column(Boolean, default=True)

    pais = relationship("Pais")
    departamento = relationship("Departamento")
    ciudad = relationship("Ciudad")
    sucursal = relationship("Sucursal")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fecha'] == 'None':
            aux['fecha'] = None
        else:
            aux['fecha'] = self.fecha.strftime('%d/%m/%Y')

        return aux


