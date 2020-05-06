from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Dia(Serializable, Base):
    way = {'hora': {}}

    __tablename__ = 'cb_asistencia_dia'
    __table_args__ = ({"schema": "ASISTENCIA"})
    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(80), nullable=False, unique=True)
    normal = Column(Boolean, nullable=False, default=True)

    hora = relationship('Hora', cascade="save-update, merge, delete, delete-orphan")


class Hora(Serializable, Base):
    way = {'dia': {}}

    __tablename__ = 'cb_asistencia_hora'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkdia = Column(Integer, ForeignKey("ASISTENCIA.cb_asistencia_dia.id"))
    entrada = Column(DateTime, nullable=False)
    salida = Column(DateTime, nullable=False)
    entradamin = Column(DateTime, nullable=False)
    entradamax = Column(DateTime, nullable=False)
    salidamin = Column(DateTime, nullable=False)
    salidamax = Column(DateTime, nullable=False)

    dia = relationship('Dia')

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        aux['entrada'] = self.entrada.strftime('%H:%M')
        aux['salida'] = self.salida.strftime('%H:%M')
        aux['entradamin'] = self.entradamin.strftime('%H:%M')
        aux['entradamax'] = self.entradamax.strftime('%H:%M')
        aux['salidamin'] = self.salidamin.strftime('%H:%M')
        aux['salidamax'] = self.salidamax.strftime('%H:%M')

        return aux
