from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class V_personal(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_vacaciones_personal'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    dias = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")