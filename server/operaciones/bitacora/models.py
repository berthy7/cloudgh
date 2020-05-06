from sqlalchemy import Column, Integer, String, DateTime, BigInteger,Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from server.database.models import Base
from server.database.serializable import Serializable
import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class Bitacora(Serializable, Base):
    way = {'usuario': {}}

    __tablename__ = 'cb_operaciones_bitacora'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(BigInteger, Sequence('id'), primary_key=True)
    fkusuario = Column(Integer, ForeignKey('ASISTENCIA.cb_usuarios_usuario.id'), nullable=True)
    ip = Column(String(100), nullable=True)
    accion = Column(String(200), nullable=True)
    fecha = Column(DateTime, nullable=False, default=fecha_zona)
    tabla = Column(String(200), nullable=True)
    identificador = Column(Integer, nullable=True)

    usuario = relationship('Usuario')
