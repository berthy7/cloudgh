from sqlalchemy import Column, Integer, String, Boolean, DateTime,  Sequence, Text,DECIMAL
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable

class Ausencia(Serializable, Base):
    way = {'tipoausencia': {}, 'persona': {},'autorizacion': {},'aprobacion': {},}

    __tablename__ = 'cb_ausencia_solicitud'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fktipoausencia = Column(Integer, ForeignKey('ASISTENCIA.cb_ausencia_tipoausencia.id'), nullable=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    fkautorizacion = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    fkaprobacion = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    descripcion = Column(Text, nullable=True)
    fechai = Column(DateTime, nullable=True)
    fechaf = Column(DateTime, nullable=True)
    horai = Column(DateTime, nullable=True)
    horaf = Column(DateTime, nullable=True)
    estadoautorizacion = Column(String(25), nullable=True, default="Pendiente")
    estadoaprobacion = Column(String(25), nullable=True, default="Pendiente")
    respuestaautorizacion = Column(String(200), nullable=True, default="")
    respuestaaprobacion = Column(String(200), nullable=True, default="")
    tipo = Column(String(100), nullable=True, default="")
    enabled = Column(Boolean, default=True)

    tipoausencia = relationship("Tipoausencia")
    persona= relationship("Persona", foreign_keys=[fkpersona])
    autorizacion = relationship("Persona", foreign_keys=[fkautorizacion])
    aprobacion = relationship("Persona", foreign_keys=[fkaprobacion])

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechai'] == 'None':
            aux['fechai'] = None
        else:
            aux['fechai'] = self.fechai.strftime('%d/%m/%Y')

        if aux['fechaf'] == 'None':
            aux['fechaf'] = None
        else:
            aux['fechaf'] = self.fechaf.strftime('%d/%m/%Y')

        if aux['horai'] == 'None':
            aux['horai'] = "----"
        else:
            aux['horai'] = self.horai.strftime("%H:%M")

        if aux['horaf'] == 'None':
            aux['horaf'] = "----"
        else:
            aux['horaf'] = self.horaf.strftime("%H:%M")

        return aux


class Tipoausencia(Serializable, Base):
    way = {}

    __tablename__ = 'cb_ausencia_tipoausencia'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(200), nullable=True)
    tipo = Column(String(100), nullable=True)
    duracion = Column(String(50), nullable=True)
    selec_duracion = Column(String(50), nullable=True)
    disponibilidad = Column(String(50), nullable=True)
    selec_disponibilidad = Column(String(50), nullable=True)

    enabled = Column(Boolean, default=True)
