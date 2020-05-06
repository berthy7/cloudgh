from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from ...database.serializable import Serializable


class Asistencia(Serializable, Base):
    way = {'persona': {'empleado': {}},'autorizacion': {}}

    __tablename__ = 'cb_asistencia_personal'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey('ASISTENCIA.cb_rrhh_persona.id'), nullable=True)
    codigo = Column(Integer, default=True)
    nombrecompleto = Column(String(255), nullable=True)
    entradamin = Column(DateTime, nullable=False)
    entrada = Column(DateTime, nullable=False)
    entradamax = Column(DateTime, nullable=False)
    salidamin = Column(DateTime, nullable=False)
    salida = Column(DateTime, nullable=False)
    salidamax = Column(DateTime, nullable=False)
    fecha = Column(DateTime, nullable=True)
    mentrada = Column(DateTime, nullable=True)
    msalida = Column(DateTime, nullable=True)
    retraso = Column(DateTime, nullable=True)
    extra = Column(DateTime, nullable=True)
    observacion = Column(String(150), nullable=True)
    enabled = Column(Boolean, nullable=False, default=False)

    persona = relationship('Persona')
    autorizacion = relationship('Autorizacionextra')

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        lista = list()
        if aux['entrada'] == 'None':
            aux['entrada'] = "----"
        else:
            aux['entrada'] = self.entrada.strftime("%H:%M")

        if aux['mentrada'] == 'None':
            aux['mentrada'] = "----"
        else:
            aux['mentrada'] = self.mentrada.strftime("%H:%M")

        if aux['salida'] == 'None':
            aux['salida'] = "----"
        else:
            aux['salida'] = self.salida.strftime("%H:%M")

        if aux['msalida'] == 'None':
            aux['msalida'] = "----"
        else:
            aux['msalida'] = self.msalida.strftime("%H:%M")

        if aux['fecha'] == 'None':
            aux['fecha'] = "----"
        else:
            aux['fecha'] = self.fecha.strftime("%d/%m/%Y")

        if aux['retraso'] == 'None':
            aux['retraso'] = "----"
        else:
            aux['retraso'] = self.retraso.strftime("%H:%M")

        if aux['extra'] == 'None':
            aux['extra'] = "----"
        else:
            aux['extra'] = self.extra.strftime("%H:%M")

        for a in self.autorizacion:
            if a.enabled:
                lista.append(a.id)
                lista.append(a.horaextra.strftime("%H:%M"))

        aux['autorizacion'] = lista

        return aux
