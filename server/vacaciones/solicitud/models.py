from sqlalchemy import Column, Integer, String, Boolean, DateTime,  Sequence, Text,DECIMAL
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class V_solicitud(Serializable, Base):
    way = {'tipovacacion': {},'solicitudGestiones': {}, 'persona': {'empleado': {}}, 'autorizacion': {},'aprobacion': {}, 'colectiva': {}}

    __tablename__ = 'cb_vacaciones_solicitud'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fktipovacacion = Column(Integer, ForeignKey('ASISTENCIA.cb_vacaciones_tipovacacion.id'), nullable=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    fkautorizacion = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    fkaprobacion = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)
    descripcion = Column(Text, nullable=True)
    jornada = Column(String(50), nullable=True, default="") #mañana , tarde
    fechar = Column(DateTime, nullable=True)
    fechai = Column(DateTime, nullable=True)
    fechaf = Column(DateTime, nullable=True)
    estadoautorizacion = Column(String(25), nullable=True, default="Pendiente")
    estadoaprobacion = Column(String(25), nullable=True, default="Pendiente")
    respuestaautorizacion = Column(String(200), nullable=True, default="")
    respuestaaprobacion = Column(String(200), nullable=True, default="")
    dias = Column(DECIMAL, nullable=True)
    enabled = Column(Boolean, default=True)
    adjunto = Column(Text, nullable=True)

    tipovacacion = relationship("V_tipovacacion")
    persona= relationship("Persona", foreign_keys=[fkpersona])
    autorizacion = relationship("Persona", foreign_keys=[fkautorizacion])
    aprobacion = relationship("Persona", foreign_keys=[fkaprobacion])
    colectiva = relationship("V_colectiva", cascade="save-update, merge, delete, delete-orphan")
    solicitudGestiones = relationship("V_solicitudGestion")


    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechai'] == 'None':
            aux['fechai'] = None
            aux['horai'] = None
        else:
            aux['fechai'] = self.fechai.strftime('%d/%m/%Y')
            aux['horai'] = self.fechai.strftime('%H:%M')

        if aux['fechaf'] == 'None':
            aux['fechaf'] = None
            aux['horaf'] = None
        else:
            aux['fechaf'] = self.fechaf.strftime('%d/%m/%Y')
            aux['horaf'] = self.fechaf.strftime('%H:%M')




        return aux


class V_tipovacacion(Serializable, Base):
    way = {}

    __tablename__ = 'cb_vacaciones_tipovacacion'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    nombre = Column(String(50), nullable=False)
    enabled = Column(Boolean, default=True)


class V_colectiva(Serializable, Base):
    way = {'solicitud': {},'persona': {}}

    __tablename__ = 'cb_vacaciones_colectiva'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fksolicitud = Column(Integer, ForeignKey("ASISTENCIA.cb_vacaciones_solicitud.id"), nullable=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"), nullable=True)

    enabled = Column(Boolean, default=True)

    solicitud = relationship("V_solicitud")
    persona = relationship("Persona")


class V_solicitudGestion(Serializable, Base):
    way = {'solicitud': {}}

    __tablename__ = 'cb_vacaciones_solicitud_ges'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    dias = Column(DECIMAL, nullable=True)
    gestion = Column(Integer, nullable=True)
    estado = Column(String(80), nullable=True)
    fksolicitud = Column(Integer, ForeignKey("ASISTENCIA.cb_vacaciones_solicitud.id"), nullable=True)


    enabled = Column(Boolean, default=True)

    solicitud = relationship("V_solicitud")

