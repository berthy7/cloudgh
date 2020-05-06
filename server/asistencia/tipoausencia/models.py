from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Tipoausencia(Serializable, Base):
    way = {}

    __tablename__ = 'cb_asistencia_tipoausencia'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(200), nullable=True)
    enabled = Column(Boolean, default=True)
