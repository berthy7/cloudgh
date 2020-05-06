from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Sucursal(Serializable, Base):
    way = {'ciudad': {'departamento': {'pais': {}}},'empresa': {},'empleados': {}}

    __tablename__ = 'cb_rrhh_sucursal'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    fkciudad = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_ciudad.id"))
    fkempresa = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_empresa.id"), nullable=True)
    enabled = Column(Boolean, default=True)

    ciudad = relationship("Ciudad")
    empresa = relationship("Empresa")
    empleados = relationship("Empleado")
