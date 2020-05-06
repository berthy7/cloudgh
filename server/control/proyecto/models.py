from sqlalchemy import Column, Integer, String, Boolean, Sequence,DateTime, Text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Proyecto(Serializable, Base):
    way = {'tareas': {}}

    __tablename__ = 'cb_control_proyecto'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)

    tareas = relationship("Tarea", cascade="save-update, merge, delete, delete-orphan")


class Requisitos(Serializable, Base):
    way = {'proyecto': {}}

    __tablename__ = 'cb_control_requisitos'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fkproyecto = Column(Integer, ForeignKey("ASISTENCIA.cb_control_proyecto.id"))
    enabled = Column(Boolean, default=True)

    proyecto = relationship("Proyecto")
