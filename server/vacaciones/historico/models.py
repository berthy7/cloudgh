from sqlalchemy import Column, Integer, String, DateTime, Boolean,Sequence,DECIMAL
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ...database.models import Base
from ...database.serializable import Serializable

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))

class V_historico(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_vacaciones_historico'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    dias = Column(DECIMAL, nullable=True)
    descripcion = Column(String(255), nullable=True,default="")
    operacion = Column(String(10), nullable=True)
    fecha = Column(DateTime, nullable=False, default=fecha_zona)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")

