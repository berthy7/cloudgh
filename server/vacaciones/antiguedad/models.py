from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class V_antiguedad(Serializable, Base):
    way = {}

    __tablename__ = 'cb_vacaciones_antiguedad'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    añoi = Column(Integer, nullable=True)
    añof = Column(Integer, nullable=True)
    dias = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True)

