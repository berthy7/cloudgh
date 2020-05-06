from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Cargo(Serializable, Base):
    way = {'responsable': {}}

    __tablename__ = 'cb_rrhh_cargo'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(200), nullable=False)
    fkresponsable = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_cargo.id'), nullable=True)
    enabled = Column(Boolean, default=True)

    responsable = relationship('Cargo')
