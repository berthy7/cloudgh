from sqlalchemy import Column, Integer, Boolean, Sequence, Date, String, Text, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Menu(Serializable, Base):
    way = {'menuplato': {'plato': {}}}

    __tablename__ = 'cb_comensal_menu'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=True)
    fecha = Column(Date, nullable=True)
    enabled = Column(Boolean, default=True)
    foto = Column(Text, nullable=True)

    menuplato = relationship("Menuplato", cascade="save-update, merge, delete, delete-orphan")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fecha'] == 'None':
            aux['fecha'] = None
        else:
            aux['fecha'] = self.fecha.strftime('%d/%m/%Y')

        return aux


class Menuplato(Serializable, Base):
    way = {'feriado': {},'plato': {}}

    __tablename__ = 'cb_comensal_Menuplato'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkmenu= Column(Integer, ForeignKey("ASISTENCIA.cb_comensal_menu.id"), nullable=True)
    fkplato = Column(Integer, ForeignKey("ASISTENCIA.cb_comensal_plato.id"), nullable=True)
    enabled = Column(Boolean, default=True)

    menu = relationship("Menu")
    plato = relationship("Plato")


class Plato(Serializable, Base):
    __tablename__ = 'cb_comensal_plato'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=True)
    tipo = Column(String(50), nullable=True)
    estado = Column(Boolean, nullable=True, default=True)
    enabled = Column(Boolean, default=True)


class HorarioComensal(Serializable, Base):
    __tablename__ = 'cb_comensal_horario'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    horaLimite = Column(DateTime, nullable=True)
    horaInicio = Column(DateTime, nullable=True)
    horaFin = Column(DateTime, nullable=True)
    enabled = Column(Boolean, default=True)


