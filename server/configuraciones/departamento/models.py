from sqlalchemy import Column, Integer, String, Boolean, Sequence,Text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Departamento(Serializable, Base):
    way = {'pais': {},'ciudades': {}}

    __tablename__ = 'cb_rrhh_departamento'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    fkpais = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_pais.id"))
    latitud = Column(Text, nullable=True)
    longitud = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)

    ciudades = relationship('Ciudad')
    pais = relationship('Pais')
