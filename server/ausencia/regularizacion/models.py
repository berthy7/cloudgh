from sqlalchemy import Column, Integer, String, Boolean, DateTime,  Sequence, Text,DECIMAL
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable

class Regularizacion(Serializable, Base):
    way = {'regularizaciondetalle': {'asistencia': {}}, 'persona': {},'autorizacion': {},'aprobacion': {},}

    __tablename__ = 'cb_ausencia_regularizacion'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)

    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    fkautorizacion = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    fkaprobacion = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    estadoautorizacion = Column(String(25), nullable=True, default="Pendiente")
    estadoaprobacion = Column(String(25), nullable=True, default="Pendiente")
    respuestaautorizacion = Column(String(200), nullable=True, default="")
    respuestaaprobacion = Column(String(200), nullable=True, default="")

    enabled = Column(Boolean, default=True)

    persona= relationship("Persona", foreign_keys=[fkpersona])
    autorizacion = relationship("Persona", foreign_keys=[fkautorizacion])
    aprobacion = relationship("Persona", foreign_keys=[fkaprobacion])

    regularizaciondetalle = relationship('RegularizacionDetalle', cascade="save-update, merge, delete, delete-orphan")

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        return aux


class RegularizacionDetalle(Serializable, Base):
    way = {'regularizacion': {},'asistencia': {}}

    __tablename__ = 'cb_ausencia_regularizacion_det'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkregularizacion = Column(Integer, ForeignKey("ASISTENCIA.cb_ausencia_regularizacion.id"), nullable=True)
    fkasistencia = Column(Integer, ForeignKey("ASISTENCIA.cb_asistencia_personal.id"), nullable=True)

    entrada = Column(Boolean, nullable=True)
    salida = Column(Boolean, nullable=True)
    motivo = Column(String(255), nullable=True, default="")

    estado = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    regularizacion = relationship('Regularizacion')
    asistencia = relationship('Asistencia')
