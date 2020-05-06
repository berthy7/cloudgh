from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Usuario(Serializable, Base):
    way = {'rol': {'modulos': {}},'persona':{}}

    __tablename__ = 'cb_usuarios_usuario'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    token = Column(String(2000), nullable=True, default='Sin Token')
    autenticacion = Column(Boolean, default=True)
    fkrol = Column(Integer, ForeignKey('ASISTENCIA.cb_usuarios_rol.id'), nullable=False)
    fkpersona = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_persona.id'), nullable=True)
    enabled = Column(Boolean, default=True)

    rol = relationship('Rol')
    persona = relationship('Persona')


    def get_dict(self, way=None):
        dictionary = super().get_dict(way)
        del(dictionary['password'])
        return dictionary


Acceso = Table('cb_usuarios_acceso', Base.metadata,
               Column('id', Integer, Sequence('id'), primary_key=True),
               Column('fkrol', Integer, ForeignKey('ASISTENCIA.cb_usuarios_rol.id')),
               Column('fkmodulo', Integer, ForeignKey('ASISTENCIA.cb_usuarios_modulo.id')), schema='ASISTENCIA')


class Modulo(Serializable, Base):
    way = {'roles': {}, 'children': {}}

    __tablename__ = 'cb_usuarios_modulo'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    route = Column(String(100))
    title = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    icon = Column(String(50), nullable=False, default='home.ico')
    menu = Column(Boolean, nullable=False, default=True)
    fkmodulo = Column(Integer, ForeignKey('ASISTENCIA.cb_usuarios_modulo.id'))

    roles = relationship('Rol', secondary=Acceso)
    children = relationship('Modulo')
