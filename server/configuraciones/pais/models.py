from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Pais(Serializable, Base):
    way = {'departamentos': {}}

    __tablename__ = 'cb_rrhh_pais'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    enabled = Column(Boolean, default=True)

    departamentos = relationship('Departamento', cascade="save-update, merge, delete, delete-orphan")
