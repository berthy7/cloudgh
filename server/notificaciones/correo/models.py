from sqlalchemy import Column, Integer, String, Boolean, Sequence,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from ...database.models import Base
from ...database.serializable import Serializable


class ServidorCorreo(Serializable, Base):
    way = {'correos': {'persona':{'empleado':{}}}}

    __tablename__ = 'cb_notificaciones_servidor'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    servidor = Column(String(200), nullable=False)
    puerto = Column(String(100), nullable=False)
    correo = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    lunes = Column(Boolean, default=True)
    martes = Column(Boolean, default=True)
    miercoles = Column(Boolean, default=True)
    jueves = Column(Boolean, default=True)
    viernes = Column(Boolean, default=True)
    sabado = Column(Boolean, default=False)
    domingo = Column(Boolean, default=False)
    hora = Column(DateTime, nullable=True)
    enabled = Column(Boolean, default=True)

    correos = relationship('Correos', cascade="save-update, merge, delete, delete-orphan")


class Correos(Serializable, Base):
    way = {'persona':{}}

    __tablename__ = 'cb_notificaciones_correos'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    fkservidorcorreo = Column(Integer, ForeignKey("ASISTENCIA.cb_notificaciones_servidor.id"))
    enabled = Column(Boolean, default=True)

    persona = relationship('Persona')

