from sqlalchemy import Column, Integer, String, Boolean, Sequence,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from ...database.models import Base
from ...database.serializable import Serializable


class Correorrhh(Serializable, Base):
    way = {'persona':{}}

    __tablename__ = 'cb_notificaciones_correo_rrhh'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    enabled = Column(Boolean, default=True)

    persona = relationship('Persona')
