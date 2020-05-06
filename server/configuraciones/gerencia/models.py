from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Gerencia(Serializable, Base):
    way = {'empresa': {},'empleados': {}}

    __tablename__ = 'cb_rrhh_gerencia'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(100), nullable=False)
    enabled = Column(Boolean, default=True)
    fkempresa = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_empresa.id"))

    empresa = relationship('Empresa')
    empleados = relationship('Empleado')
