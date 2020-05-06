from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable
from sqlalchemy.ext.hybrid import hybrid_property


class Organigrama(Serializable, Base):
    way = {'hijos': {},'padre': {},'cargo': {},'persona': {}}

    __tablename__ = 'cb_rrhh_organigrama'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkcargo = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_cargo.id'), nullable=True)
    fkpersona = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_persona.id'), nullable=True)
    fkpadre = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_organigrama.id'), nullable=True)
    siguiente = Column(Integer, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)

    cargo = relationship('Cargo')
    persona = relationship('Persona')

    padre = relationship('Organigrama')
    hijos = relationship('Organigrama')
