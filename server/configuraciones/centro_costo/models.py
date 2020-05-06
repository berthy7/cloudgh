from sqlalchemy import Column, Integer, String, Boolean, Sequence
from ...database.models import Base
from ...database.serializable import Serializable


class Centro_costo(Serializable, Base):
    __tablename__ = 'cb_rrhh_centro_costo'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    codigo = Column(String(50), nullable=True,)
    nombre = Column(String(50), nullable=False)
    enabled = Column(Boolean, default=True)
