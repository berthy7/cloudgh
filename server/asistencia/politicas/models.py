from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


from ...database.models import Base
from ...database.serializable import Serializable


class Politicas(Serializable, Base):
    way = {'empresa': {}}

    __tablename__ = 'cb_asistencia_politicas'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkempresa = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_empresa.id'), nullable=True)
    toleranciadia = Column(Integer, nullable=False, default=0)
    toleranciames = Column(Integer, nullable=False, default=0)
    enabled = Column(Boolean, nullable=False, default=True)

    empresa = relationship('Empresa')

