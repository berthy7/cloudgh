from sqlalchemy import Column, Integer, String, Boolean, Sequence,DateTime, Text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Tarea(Serializable, Base):
    way = {'persona': {},'proyecto': {}}

    __tablename__ = 'cb_control_tarea'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    descripcion = Column(Text, nullable=True)
    prioridad = Column(String(50), nullable=True)
    estimacion = Column(Integer, nullable=True)
    fechaInicio = Column(DateTime, nullable=True)
    fechaFin = Column(DateTime, nullable=True)
    fechaCreacion = Column(DateTime, nullable=True)
    fechaConclusion = Column(DateTime, nullable=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    fkproyecto = Column(Integer, ForeignKey("ASISTENCIA.cb_control_proyecto.id"), nullable=True)
    estado = Column(String(50), default=True)

    enabled = Column(Boolean, default=True)

    persona = relationship('Persona')
    proyecto = relationship('Proyecto')

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fechaInicio'] == 'None':
            aux['fechaInicio'] = None
        else:
            aux['fechaInicio'] = self.fechaInicio.strftime('%Y-%m-%d %H:%M')

        if aux['fechaFin'] == 'None':
            aux['fechaFin'] = None
        else:
            aux['fechaFin'] = self.fechaFin.strftime('%Y-%m-%d %H:%M')

        if aux['fechaCreacion'] == 'None':
            aux['fechaCreacion'] = None
        else:
            aux['fechaCreacion'] = self.fechaCreacion.strftime('%Y-%m-%d %H:%M')

        if aux['fechaConclusion'] == 'None':
            aux['fechaConclusion'] = None
        else:
            aux['fechaConclusion'] = self.fechaConclusion.strftime('%Y-%m-%d %H:%M')

        return aux
