from sqlalchemy import Column, Integer, String, Boolean, Sequence,Text
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable
from ...asistencia.politicas.models import *


class Empresa(Serializable, Base):
    way = {'gerencias': {'empleados': {}},'sucursales': {},'politicas': {}}

    __tablename__ = 'cb_rrhh_empresa'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False)
    foto1 = Column(Text, nullable=True)
    foto2 = Column(Text, nullable=True)
    foto3 = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)

    gerencias = relationship('Gerencia')
    sucursales = relationship('Sucursal')
    politicas = relationship('Politicas')
