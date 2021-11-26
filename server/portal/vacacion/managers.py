from ...operaciones.bitacora.managers import *
from ...configuraciones.empresa.managers import EmpresaManager
from ...asistencia.asistenciapersonal.models import *
from ...asistencia.tipoausencia.models import *
from ...usuarios.ajustes.models import *
from ...personal.organigrama.managers import *
from ...notificaciones.correo.managers import *
from ...calendario.feriado.managers import *
from ...vacaciones.solicitud.models import *

from server.common.managers import SuperManager
from .models import *

from sqlalchemy.sql import func, and_,or_
from datetime import datetime

class PortalVacacionManager(SuperManager):
    def __init__(self, db):
        super().__init__(V_solicitud, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def obtener_x_persona(self, fkpersona):
        return self.db.query(self.entity).filter(self.entity.fkpersona == fkpersona).order_by(self.entity.id.desc()).all()

    def obtener_x_supervisor(self, fkpersona):
        solicitudes = self.db.query(self.entity).filter(or_(self.entity.fkautorizacion == fkpersona,self.entity.fkaprobacion == fkpersona)).order_by(self.entity.id.desc()).all()


        # organi_super = self.db.query(Organigrama).filter(Organigrama.enabled == True).filter(
        #     Organigrama.fkpersona == fkpersona).first()
        #
        # if organi_super:
        #     solicitudes_superior = self.db.query(self.entity).filter(self.entity.fksuperior == organi_super.fkpersona).all()
        #
        #     for soli in solicitudes_superior:
        #         solicitudes.append(soli)

        return solicitudes



    def obtener_vacacion(self,fkpersona,fecha):
        respuesta = ""

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            ausencia = self.db.query(V_solicitud).filter(V_solicitud.fkpersona == fkpersona).filter(
                V_solicitud.estado == "Aceptado").filter(
                and_(func.to_date(V_solicitud.fechai) <= fecha, func.to_date(V_solicitud.fechaf) >= fecha)).all()
        else:
            # version postgres
            ausencia = self.db.query(V_solicitud).filter(V_solicitud.fkpersona == fkpersona).filter(
                V_solicitud.estado == "Aceptado").filter(
                and_(func.date(V_solicitud.fechai) <= fecha, func.date(V_solicitud.fechaf) >= fecha)).all()

        if len(ausencia) > 0:
             respuesta = ausencia[0].tipovacacion.nombre

        return respuesta

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.id.desc()).all()

    def insert_2(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fechai = datetime.strptime(objeto.fechai, '%d/%m/%Y')
        objeto.fechaf = datetime.strptime(objeto.fechaf, '%d/%m/%Y')

        idsuperior = OrganigramaManager(self.db).obtener_superior(objeto.fkpersona)

        objeto.fksuperior = idsuperior

        if objeto.horai == "":
            objeto.horai = None
        else:
            objeto.horai = datetime.strptime('01/01/2000 ' + objeto.horai, '%d/%m/%Y %H:%M')

        if objeto.horaf == "":
            objeto.horaf = None
        else:
            objeto.horaf = datetime.strptime('01/01/2000 ' + objeto.horaf, '%d/%m/%Y %H:%M')

        a = super().insert(objeto)
        idsuperior = CorreoManager(self.db).notificar_ausencia(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Ausencia.",
                     fecha=fecha, tabla="cb_asistencia_ausencia", identificador=a.id)
        super().insert(b)


        return a

    def insert(self, diccionary):

        fecha = BitacoraManager(self.db).fecha_actual()
        diccionary['fechai'] = datetime.strptime(diccionary['fechai'], '%d/%m/%Y')
        diccionary['fechaf'] = datetime.strptime(diccionary['fechaf'], '%d/%m/%Y')

        if int(diccionary['fktipovacacion']) != 3:
            if diccionary['mañana']:
                diccionary['jornada'] = "Mañana"
            elif diccionary['tarde']:
                diccionary['jornada'] = "Tarde"

            idsuperior = OrganigramaManager(self.db).obtener_superior(diccionary['fkpersona'])

            # idsuperior es None cuando no tiene Superior
            if idsuperior is None:
                diccionary['fksuperior'] = None
            else:
                diccionary['fksuperior'] = idsuperior

            objeto = PortalVacacionManager(self.db).entity(**diccionary)
            a = super().insert(objeto)
            idsuperior = CorreoManager(self.db).notificar_ausencia(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro V_solicitud.",
                         fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=a.id)
            super().insert(b)

            return a
        else:
            lista_colectiva = list()

            repetidos = set(diccionary['personas_arbol']).intersection(diccionary['personas'])

            for rep in repetidos:
                diccionary['personas'].remove(rep)

            for per in diccionary['personas']:
                diccionary['personas_arbol'].append(per)

            for sv in diccionary['sin_vacacion']:
                if sv['estado'] == False:
                    diccionary['personas_arbol'].remove(int(sv['id']))

            for p in diccionary['personas_arbol']:
                lista_colectiva.append(dict(fkpersona=p))

            diccionary['colectiva'] = lista_colectiva

            if diccionary['fkpersona'] == "":
                diccionary['fkpersona'] = None

            objeto = V_solicitudManager(self.db).entity(**diccionary)
            a = super().insert(objeto)
            idsuperior = CorreoManager(self.db).notificar_ausencia(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro V_solicitud.",
                         fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=a.id)
            super().insert(b)

            return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fechai = datetime.strptime(objeto.fechai, '%d/%m/%Y')
        objeto.fechaf = datetime.strptime(objeto.fechaf, '%d/%m/%Y')

        if objeto.horai == "":
            objeto.horai = None
        else:
            objeto.horai = datetime.strptime('01/01/2000 ' + objeto.horai, '%d/%m/%Y %H:%M')

        if objeto.horaf == "":
            objeto.horaf = None
        else:
            objeto.horaf = datetime.strptime('01/01/2000 ' + objeto.horaf, '%d/%m/%Y %H:%M')

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Ausencia.",
                     fecha=fecha, tabla="cb_asistencia_ausencia", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Ausencia.", fecha=fecha,
                     tabla="cb_asistencia_ausencia", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()


    def actualizar_ausencias(self, objeto):

        fechas = BitacoraManager(self.db).rango_fechas(objeto.fechai, objeto.fechaf)

        for fech in fechas:
            fecha_hoy = fech.date()

            ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == objeto.fkpersona).filter(func.to_date(Asistencia.fecha).between(fecha_hoy, fecha_hoy)).all()

            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == objeto.fkpersona).filter(
                    func.date(Asistencia.fecha) == fecha_hoy).all()

            for asistencia in asistencia_personal:
                tipoausencia = self.db.query(Tipoausencia).filter(Tipoausencia.id == objeto.fktipoausencia).first()
                asistencia.observacion = tipoausencia.nombre
                super().update(asistencia)

        return objeto