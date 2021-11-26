from sqlalchemy import Column, Integer,DateTime, String, Boolean, Sequence
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Ajustes(Serializable, Base):
    way = {}

    __tablename__ = 'cb_usuarios_ajustes'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    dominio = Column(String(100), nullable=True)
    mysql = Column(Boolean, nullable=True)
    postgres = Column(Boolean, nullable=True)
    oracle = Column(Boolean, nullable=True)
    sqlserver = Column(Boolean, nullable=True)
    iniciohoranocturno = Column(DateTime, nullable=True)
    finhoranocturno = Column(DateTime, nullable=True)
    porcentajehoranocturno = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True)

