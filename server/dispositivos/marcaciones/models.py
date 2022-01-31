from sqlalchemy import Column, Integer, String, DateTime, BigInteger,Sequence,Boolean
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



class BitacoraMarcaciones(Serializable, Base):
    way = {}

    __tablename__ = 'cb_dispositivos_bitacora'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(BigInteger, Sequence('id'), primary_key=True)
    fecha = Column(DateTime, nullable=True)
    registro = Column(String(200), nullable=True)

