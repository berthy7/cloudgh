from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Semanal(Serializable, Base):
    way = {'semanaldetalle': {'dia': {'hora': {}}}}

    __tablename__ = 'cb_asistencia_semanal'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    codigo = Column(String(80), nullable=True, unique=True)
    nombre = Column(String(80), nullable=False, unique=True)
    enabled = Column(Boolean, default=True)

    semanaldetalle = relationship('Semanaldetalle', cascade="save-update, merge, delete, delete-orphan")


class Semanaldetalle(Serializable, Base):
    way = {'dia': {},'semanal': {}}

    __tablename__ = 'cb_asistencia_semanal_detalle'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    lunes = Column(Boolean, nullable=False, default=False)
    martes = Column(Boolean, nullable=False, default=False)
    miercoles = Column(Boolean, nullable=False, default=False)
    jueves = Column(Boolean, nullable=False, default=False)
    viernes = Column(Boolean, nullable=False, default=False)
    sabado = Column(Boolean, nullable=False, default=False)
    domingo = Column(Boolean, nullable=False, default=False)
    fkdia = Column(Integer, ForeignKey("ASISTENCIA.cb_asistencia_dia.id"), nullable=True)
    fksemanal = Column(Integer, ForeignKey("ASISTENCIA.cb_asistencia_semanal.id"), nullable=True)

    dia = relationship('Dia')
    semanal = relationship('Semanal')
