from ..usuario.models import *
from ...database.models import Base
from ...database.serializable import Serializable


class Rol(Serializable, Base):
    way = {'usuario': {}, 'modulos': {}}

    __tablename__ = 'cb_usuarios_rol'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column( Integer, Sequence('id'), primary_key=True)
    nombre = Column( String(50), nullable=False)
    descripcion = Column( String(200), nullable=False)
    enabled = Column(Boolean, default=True)

    usuario = relationship('Usuario')
    modulos = relationship('Modulo', secondary=Acceso)
