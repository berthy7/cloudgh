from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Lectores(Serializable, Base):
    way = {'sucursal': {}}

    __tablename__ = 'cb_dispositivos_lectores'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    ip = Column(String(100), nullable=False)
    puerto = Column(Integer, nullable=False)
    tipo = Column(String(100), nullable=False)
    descripcion = Column(String(100), nullable=True)
    modelo = Column(String(100), nullable=True)
    fksucursal = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_sucursal.id'), nullable=True)
    estado = Column(Boolean,  default=True)

    enabled = Column(Boolean, default=True)

    sucursal = relationship('Sucursal')
