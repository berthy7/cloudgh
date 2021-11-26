from sqlalchemy import Column, Integer, Boolean, DateTime, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Marcaciones(Serializable, Base):
    way = {'dispositivo': {}}

    __tablename__ = 'cb_dispositivos_marcaciones'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    codigo = Column(Integer, nullable=False)
    time = Column(DateTime)
    fkdispositivo = Column(Integer, ForeignKey('ASISTENCIA.cb_dispositivos_lectores.id'), nullable=True)
    sucursal = Column(Integer, nullable=True)

    enabled = Column(Boolean, default=True)

    dispositivo = relationship('Lectores')
