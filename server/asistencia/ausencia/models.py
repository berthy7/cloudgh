from sqlalchemy import Column, Integer, String, Boolean, DateTime,  Sequence, Text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Ausencia(Serializable, Base):
    way = {'tipoausencia': {}, 'persona': {}, 'superior': {}}

    __tablename__ = 'cb_asistencia_ausencia'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fktipoausencia = Column(Integer, ForeignKey('ASISTENCIA.cb_asistencia_tipoausencia.id'), nullable=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    fksuperior = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    descripcion = Column(Text, nullable=True)
    fechai = Column(DateTime, nullable=True)
    fechaf = Column(DateTime, nullable=True)
    horai = Column(DateTime, nullable=True)
    horaf = Column(DateTime, nullable=True)
    estado = Column(String(25), nullable=True, default="Pendiente")
    respuesta = Column(String(200), nullable=True, default="")
    enabled = Column(Boolean, default=True)

    tipoausencia = relationship("Tipoausencia")
    persona= relationship("Persona", foreign_keys=[fkpersona])
    superior = relationship("Persona", foreign_keys=[fksuperior])

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
