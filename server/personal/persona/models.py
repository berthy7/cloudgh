from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...database.models import Base
from server.database.serializable import Serializable
from sqlalchemy.ext.hybrid import hybrid_property


class Persona(Serializable, Base):
    way = {'coordenadas': {},'contrato': {}, 'empleado': {'sucursal': {'ciudad': {'departamento': {'pais': {}} } }, 'gerencia': {} }, 'administrativo': {}, 'educacion': {},
           'capacitacion': {}, 'estudios': {}, 'memo': {}, 'idioma': {}, 'experiencia': {}, 'padres': {}, 'conyuge': {}, 'hijos': {}}

    __tablename__ = 'cb_rrhh_persona'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    apellidopaterno = Column(String(50), nullable=False)
    apellidomaterno = Column(String(50), nullable=True, default="")
    nombres = Column(String(50), nullable=False)
    sexo = Column(String(10), nullable=False)
    ci = Column(String(50), nullable=False)
    fechanacimiento = Column(Date, nullable=True)
    domicilio = Column(String(100), nullable=True)
    telefono = Column(String(50), nullable=True)
    enabled = Column(Boolean, default=True)

    empleado = relationship("Empleado", cascade="save-update, merge, delete, delete-orphan")
    contrato = relationship("Contrato", cascade="save-update, merge, delete, delete-orphan")
    administrativo = relationship("Administrativo", cascade="save-update, merge, delete, delete-orphan")
    educacion = relationship("Educacion", cascade="save-update, merge, delete, delete-orphan")
    capacitacion = relationship("Capacitacion", cascade="save-update, merge, delete, delete-orphan")
    estudios = relationship("Estudios", cascade="save-update, merge, delete, delete-orphan")
    memo = relationship("Memo", cascade="save-update, merge, delete, delete-orphan")
    idioma = relationship("Idioma", cascade="save-update, merge, delete, delete-orphan")
    experiencia = relationship("Experiencia", cascade="save-update, merge, delete, delete-orphan")
    padres = relationship("Padres", cascade="save-update, merge, delete, delete-orphan")
    conyuge = relationship("Conyuge", cascade="save-update, merge, delete, delete-orphan")
    hijos = relationship("Hijos", cascade="save-update, merge, delete, delete-orphan")
    coordenadas = relationship("Coordenadas", cascade="save-update, merge, delete, delete-orphan")

    @hybrid_property
    def fullname(self):
        aux = ""
        if self.apellidopaterno is not None:
            aux = self.apellidopaterno + " "
        else:
            aux = " "
        if self.apellidomaterno is not None:
            aux = aux + self.apellidomaterno + " "
        else:
            aux = " "

        if self.nombres is not None:
            aux += self.nombres
        else:
            aux = " "

        return aux

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechanacimiento'] == 'None':
            aux['fechanacimiento'] = None
        else:
            aux['fechanacimiento'] = self.fechanacimiento.strftime('%d/%m/%Y')

        aux['fullname'] = self.apellidopaterno + " " + self.apellidomaterno + " " + self.nombres

        return aux


class Empleado(Serializable, Base):
    way = {'persona': {},
           'pais': {},
           'departamentos': {},
           'ciudad': {},
           'sucursal': {'empresa': {}},
           'gerencia': {},
           'cargo': {},
           'centro': {},
           'oficina': {}}

    __tablename__ = 'cb_rrhh_empleado'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    codigo = Column(Integer, nullable=False, unique=True)
    foto = Column(String(200), nullable=True)
    fkgerencia = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_gerencia.id"), nullable=True)
    fkcargo = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_cargo.id"))
    fkpais = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_pais.id"), nullable=True)
    fkdepartamento = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_departamento.id"), nullable=True)
    fkciudad = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_ciudad.id"), nullable=True)
    fksucursal = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_sucursal.id"), nullable=True)
    fkcentro = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_centro_costo.id"), nullable=True)
    fkoficina = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_oficina.id"), nullable=True)
    email = Column(String(50), nullable=True)
    autorizacion = Column(Boolean, default=True)
    aprobacion = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")
    pais = relationship("Pais")
    departamentos = relationship("Departamento")
    ciudad = relationship("Ciudad")
    sucursal = relationship("Sucursal")
    gerencia = relationship("Gerencia")
    cargo = relationship("Cargo")
    centro = relationship("Centro_costo")
    oficina = relationship("Oficina")


class Contrato(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_contrato'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    nroContrato = Column(Integer, nullable=True)
    sueldo = Column(Float, nullable=True)
    fechaIngreso = Column(DateTime, nullable=True)
    fechaFin = Column(DateTime, nullable=True)
    fechaForzado = Column(DateTime, nullable=True)
    tipo = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechaIngreso'] == 'None':
            aux['fechaIngreso'] = None
        else:
            aux['fechaIngreso'] = self.fechaIngreso.strftime('%d/%m/%Y')

        if aux['fechaFin'] == 'None':
            aux['fechaFin'] = None
        else:
            aux['fechaFin'] = self.fechaFin.strftime('%d/%m/%Y')

        if aux['fechaForzado'] == 'None':
            aux['fechaForzado'] = None
        else:
            aux['fechaForzado'] = self.fechaForzado.strftime('%d/%m/%Y')

        return aux


class Administrativo(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_administrativo'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    nroAsegurado = Column(String(50), nullable=True)
    cajaSalud = Column(String(50), nullable=True)
    afp = Column(String(50), nullable=True)
    tipoTrabajador = Column(String(50), nullable=True)
    banco = Column(String(50), nullable=True)
    nroCuenta= Column(String(50), nullable=True)
    libretaMilitar = Column(String(50), nullable=True)
    hijos = Column(String(50), nullable=True)
    brevete = Column(String(50), nullable=True)
    grupoSanguineo = Column(String(50), nullable=True)
    telefonoFijo = Column(String(50), nullable=True)
    telefonoCelular = Column(String(50), nullable=True)
    estadoCivil = Column(String(50), nullable=True)
    nacimientoPais = Column(String(50), nullable=True)
    nacimientoDepartamento = Column(String(50), nullable=True)
    nacimientoProvincia = Column(String(50), nullable=True)
    nacimientoDistrito = Column(String(50), nullable=True)
    nacimientoDomicilio = Column(String(50), nullable=True)
    domicilioPais = Column(String(50), nullable=True)
    domicilioDepartamento = Column(String(50), nullable=True)
    domicilioProvincia = Column(String(50), nullable=True)
    domicilioDistrito = Column(String(50), nullable=True)
    domiciliodireccion = Column(String(50), nullable=True)
    domicilioCasa = Column(String(50), nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")


class Educacion(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_educacion'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    nivelEducativo = Column(String(50), nullable=True)
    tipoCentroEstudio= Column(String(50), nullable=True)
    nombreCentroEstudio = Column(String(255), nullable=True)
    condicionActual = Column(String(50), nullable=True)
    profesion = Column(String(50), nullable=True)
    fechaTitulo = Column(Date, nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechaTitulo'] == 'None':
            aux['fechaTitulo'] = None
        else:
            aux['fechaTitulo'] = self.fechaTitulo.strftime('%d/%m/%Y')

        return aux


class Estudios(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_estudios'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    detalle = Column(String(50), nullable=True)
    gestion = Column(Integer, nullable=True)
    tipo = Column(String(50), nullable=True) #Postgrado u Otros Estudios
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")


class Conyuge(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_conyuge'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    nombreCompleto = Column(String(50), nullable=False)
    fechanacimiento = Column(Date, nullable=True)
    sexo = Column(String(10), nullable=False)
    ci = Column(String(50), nullable=False)
    pais = Column(String(50), nullable=True)
    departamento = Column(String(50), nullable=True)
    provincia = Column(String(50), nullable=True)
    distrito = Column(String(50), nullable=True)
    domicilio = Column(String(50), nullable=True)
    telefono = Column(String(50), nullable=True)
    instruccion = Column(String(50), nullable=True)
    ocupacion = Column(String(50), nullable=True)
    centroTabajo = Column(String(50), nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechanacimiento'] == 'None':
            aux['fechanacimiento'] = None
        else:
            aux['fechanacimiento'] = self.fechanacimiento.strftime('%d/%m/%Y')

        return aux


class Hijos(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_hijos'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    nombrecompleto = Column(String(50), nullable=True)
    direccion= Column(String(50), nullable=True)
    telefono = Column(String(50), nullable=True)
    fechanacimiento = Column(Date, nullable=True)
    enabled = Column(Boolean, default=True)

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechanacimiento'] == 'None':
            aux['fechanacimiento'] = None
        else:
            aux['fechanacimiento'] = self.fechanacimiento.strftime('%d/%m/%Y')

        return aux

    persona = relationship("Persona")


class Capacitacion(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_capacitacion'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    documento = Column(String(50), nullable=True)
    detalle = Column(String(50), nullable=True)
    fechaInicio = Column(Date, nullable=True)
    fechaFin = Column(Date, nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechaInicio'] == 'None':
            aux['fechaInicio'] = None
        else:
            aux['fechaInicio'] = self.fechaInicio.strftime('%d/%m/%Y')

        if aux['fechaFin'] == 'None':
            aux['fechaFin'] = None
        else:
            aux['fechaFin'] = self.fechaFin.strftime('%d/%m/%Y')

        return aux


class Memo(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_memo'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    documento = Column(String(50), nullable=True)
    evento = Column(String(50), nullable=True)
    detalle = Column(String(50), nullable=True)
    fechaInicio = Column(Date, nullable=True)
    fechaFin = Column(Date, nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechaInicio'] == 'None':
            aux['fechaInicio'] = None
        else:
            aux['fechaInicio'] = self.fechaInicio.strftime('%d/%m/%Y')

        if aux['fechaFin'] == 'None':
            aux['fechaFin'] = None
        else:
            aux['fechaFin'] = self.fechaFin.strftime('%d/%m/%Y')

        return aux


class Idioma(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_idioma'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    idioma = Column(String(50), nullable=True)
    habla = Column(Boolean, default=True)
    lee = Column(Boolean, default=True)
    escribe = Column(Boolean, default=True)
    aprendio = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")


class Experiencia(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_experiencia'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    especialidad = Column(String(50), nullable=True)
    entidad = Column(String(255), nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")


class Padres(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_padres'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    nombreCompleto = Column(String(50), nullable=True)
    fechanacimiento = Column(Date, nullable=True)
    situacion = Column(String(50), nullable=True)
    telefono = Column(String(50), nullable=True)
    tipo = Column(String(50), nullable=True) #papa o mama
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        if aux['fechanacimiento'] == 'None':
            aux['fechanacimiento'] = None
        else:
            aux['fechanacimiento'] = self.fechanacimiento.strftime('%d/%m/%Y')

        return aux


class Coordenadas(Serializable, Base):
    way = {'persona': {}}

    __tablename__ = 'cb_rrhh_persona_coordenadas'
    __table_args__ = ({"schema": "ASISTENCIA"})

    id = Column(Integer, Sequence('id'), primary_key=True)
    fkpersona = Column(Integer, ForeignKey("ASISTENCIA.cb_rrhh_persona.id"))
    latitud = Column(Text, nullable=True)
    longitud = Column(Text, nullable=True)
    estado = Column(Boolean, nullable=True)
    enabled = Column(Boolean, default=True)

    persona = relationship("Persona")