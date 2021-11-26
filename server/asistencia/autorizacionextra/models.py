from sqlalchemy import Column, Integer, String, Boolean, DateTime,  Sequence, Text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Autorizacionextra(Serializable, Base):
    way = {'asistencia': {'persona': {'empleado': {}}}}

    __tablename__ = 'cb_asistencia_autorizacion'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkasistencia = Column(Integer, ForeignKey('ASISTENCIA.cb_asistencia_personal.id'), nullable=True)
    horaextra = Column(DateTime, nullable=True)
    fecha = Column(DateTime, nullable=True)
    enabled = Column(Boolean, default=True)

    asistencia = relationship("Asistencia")

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fecha'] == 'None':
            aux['fecha'] = None
        else:
            aux['fecha'] = self.fecha.strftime('%d/%m/%Y')

        return aux
