from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Oficina(Serializable, Base):
    way = {'sucursal': {}}

    __tablename__ = 'cb_rrhh_oficina'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False)
    fksucursal = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_sucursal.id'), nullable=True)
    enabled = Column(Boolean, default=True)

    sucursal = relationship("Sucursal")
