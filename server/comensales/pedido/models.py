from sqlalchemy import Column, Integer, Boolean, DateTime, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Pedido(Serializable, Base):
    way = {'plato': {},'persona': {},'feriado': {'menuplato': {'plato': {}}}}

    __tablename__ = 'cb_comensal_pedido'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fecha = Column(DateTime, nullable=True)
    sopa = Column(Boolean, nullable=True)
    fkmenu = Column(Integer, ForeignKey("ASISTENCIA.cb_comensal_menu.id"), nullable=True)
    fkplato = Column(Integer, ForeignKey("ASISTENCIA.cb_comensal_plato.id"), nullable=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    enabled = Column(Boolean, default=True)

    menu = relationship("Menu")
    plato = relationship("Plato")
    persona = relationship("Persona")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fecha'] == 'None':
            aux['fecha'] = None
        else:
            aux['fecha'] = self.fecha.strftime('%d/%m/%Y')

        return aux
