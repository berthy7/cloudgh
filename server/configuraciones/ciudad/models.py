from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Ciudad(Serializable, Base):
    way = {'departamento': {'pais': {}},'sucursales': {}}

    __tablename__ = 'cb_rrhh_ciudad'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    enabled = Column(Boolean, default=True)
    fkdepartamento = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_departamento.id"))

    departamento = relationship('Departamento')
    sucursales = relationship('Sucursal')
