from sqlalchemy import Column, Integer, String, Boolean, Date, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Asignacion(Serializable, Base):
    way = {'persona': {}, 'periodo': {}}

    __tablename__ = 'cb_asistencia_asignacion'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_persona.id'), nullable=True)
    fkperiodo = Column(Integer, ForeignKey('ASISTENCIA.cb_asistencia_periodo.id'), nullable=True)

    persona = relationship('Persona')
    periodo = relationship('Periodo')


class Periodo(Serializable, Base):
    way = {'dia': {'hora': {}},'asignacion': {},'semanal': {}}

    __tablename__ = 'cb_asistencia_periodo'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fechai = Column(Date)
    fechaf = Column(Date)
    observacion = Column(String(255), nullable=True)
    fksemanal = Column(Integer, ForeignKey('ASISTENCIA.cb_asistencia_semanal.id'), nullable=True)
    fkdia = Column(Integer, ForeignKey('ASISTENCIA.cb_asistencia_dia.id'), nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)

    asignacion = relationship('Asignacion', cascade="save-update, merge, delete, delete-orphan")
    semanal = relationship('Semanal')
    dia = relationship('Dia')
