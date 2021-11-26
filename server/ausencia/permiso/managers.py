from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from ...asistencia.tipoausencia.managers import *
from ...notificaciones.correo_rrhh.managers import *
from ...personal.persona.managers import *
from ...personal.organigrama.managers import *
from datetime import datetime, timedelta, time, date
from .models import *
from ..tipoausencia.models import *
from ...usuarios.ajustes.models import *
from ...asistencia.asistenciapersonal.models import *
from sqlalchemy.sql import func, and_
from sqlalchemy import extract


class PermisoManager(SuperManager):

    def __init__(self, db):
        super().__init__(Ausencia, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def listar_todo(self):
        return self.db.query(self.entity).join(Tipoausencia).filter(self.entity.enabled == True).filter(Tipoausencia.tipo == "Permiso").all()

    def obtener_x_id(self,id):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.id == id).first()


    def insert(self, diccionary):
        if diccionary['tiempo_duracion'] == "Hora":
            date_ini = diccionary['fechai']
            diccionary['horai'] = datetime.strptime('01/01/2000 ' + diccionary['horai'], '%d/%m/%Y %H:%M')
            diccionary['horaf'] = diccionary['horai'] + timedelta(hours=int(diccionary['tiempo']))

            diccionary['fechai'] = datetime.strptime(date_ini, '%d/%m/%Y')
            diccionary['fechaf'] = datetime.strptime(date_ini, '%d/%m/%Y')
        elif diccionary['tiempo_duracion'] == "Dia":
            diccionary['fechai'] = datetime.strptime(diccionary['fechai'], '%d/%m/%Y')
            diccionary['fechaf'] = diccionary['fechai'] + timedelta(days=int(diccionary['tiempo']) - 1)

            if diccionary['horai'] == "":
                diccionary['horai'] = None
            else:
                diccionary['horai'] = datetime.strptime('01/01/2000 ' + diccionary['horai'], '%d/%m/%Y %H:%M')

            if diccionary['horaf'] == "":
                diccionary['horaf'] = None
            else:
                diccionary['horaf'] = datetime.strptime('01/01/2000 ' + diccionary['horaf'], '%d/%m/%Y %H:%M')
        elif diccionary['tiempo_duracion'] == "Medio dia":
            diccionary['fechai'] = datetime.strptime(diccionary['fechai'], '%d/%m/%Y')
            diccionary['fechaf'] = diccionary['fechai']

            if diccionary['horai'] == "":
                diccionary['horai'] = None
            else:
                diccionary['horai'] = datetime.strptime('01/01/2000 ' + diccionary['horai'], '%d/%m/%Y %H:%M')

            if diccionary['horaf'] == "":
                diccionary['horaf'] = None
            else:
                diccionary['horaf'] = datetime.strptime('01/01/2000 ' + diccionary['horaf'], '%d/%m/%Y %H:%M')

        elif diccionary['tiempo_duracion'] == "Ilimitado":
            diccionary['fechai'] = datetime.strptime(diccionary['fechai'], '%d/%m/%Y')
            diccionary['fechaf'] = datetime.strptime(diccionary['fechaf'], '%d/%m/%Y')


            if diccionary['horai'] == "":
                diccionary['horai'] = None
            else:
                diccionary['horai'] = datetime.strptime('01/01/2000 ' + diccionary['horai'], '%d/%m/%Y %H:%M')

            if diccionary['horaf'] == "":
                diccionary['horaf'] = None
            else:
                diccionary['horaf'] = datetime.strptime('01/01/2000 ' + diccionary['horaf'], '%d/%m/%Y %H:%M')

        diccionary['tipo'] = "Permiso"

        superiores = OrganigramaManager(self.db).obtener_autorizacion_aprobacion(diccionary['fkpersona'])

        diccionary['fkautorizacion'] = superiores['fkautorizacion']
        diccionary['fkaprobacion'] = superiores['fkaprobacion']
        diccionary['estadoautorizacion'] = superiores['estadoautorizacion']
        diccionary['estadoaprobacion'] = superiores['estadoaprobacion']


        objeto = PermisoManager(self.db).entity(**diccionary)


        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        CorreoManager(self.db).notificar_ausencia(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Solicitud de Salida.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=a.id)
        super().insert(b)

        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Solicitud de Salida.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Permiso.", fecha=fecha,
                     tabla="rrhh_Permiso", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def disponibilidad(self, fkpersona, fktipoausencia, dia, fechai):

        fechai = datetime.strptime(fechai, '%d/%m/%Y')

        fecha_mes = fechai.month

        n = self.db.query(func.count(Ausencia.id)).filter(Ausencia.fkpersona == fkpersona).filter(
            extract('month', Ausencia.fechai) == fecha_mes).filter(Ausencia.fktipoausencia == fktipoausencia)

        cantidad = n[0][0]

        if int(dia) > cantidad:
            return dict(mensaje="", respuesta=True, tipo="")

        else:
            return dict(mensaje="Ha superado la cantidad de disponibilidad", respuesta=False, tipo="warning")

    def actualizar_permisos(self, objeto,persona):

        fechas = BitacoraManager(self.db).rango_fechas(objeto.fechai, objeto.fechaf)

        for fech in fechas:
            fecha_hoy = fech.date()

            ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == persona).filter(
                    func.to_date(Asistencia.fecha).between(fecha_hoy, fecha_hoy)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == persona).filter(
                    func.date(Asistencia.fecha) == fecha_hoy).all()

            for asistencia in asistencia_personal:
                tipoausencia = self.db.query(Tipoausencia).filter(Tipoausencia.id == objeto.fktipoausencia).first()
                asistencia.observacion = tipoausencia.nombre
                super().update(asistencia)

        return objeto

    def autorizacion(self, diccionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        ausencia = self.db.query(Ausencia).filter(Ausencia.id == diccionary['id']).first()
        ausencia.estadoautorizacion = diccionary['estadoautorizacion']
        ausencia.respuestaautorizacion = diccionary['respuestaautorizacion']

        a = super().update(ausencia)
        b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Autorizacion Autorizacion de salida.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=a.id)
        super().insert(b)

        if not a.persona.empleado[0].aprobacion:

            if ausencia.estadoautorizacion == "Aceptado":
                PermisoManager(self.db).actualizar_permisos(ausencia, ausencia.fkpersona)

        idsuperior = CorreoManager(self.db).notificar_ausencia_respuesta_autorizacion(ausencia)

        return ausencia

    def aprobacion(self, diccionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        ausencia = self.db.query(Ausencia).filter(Ausencia.id == diccionary['id']).first()
        ausencia.estadoaprobacion = diccionary['estadoaprobacion']
        ausencia.respuestaaprobacion = diccionary['respuestaaprobacion']

        a = super().update(ausencia)
        b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Aprobacion Autorizacion de salida.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=a.id)
        super().insert(b)

        idsuperior = CorreoManager(self.db).notificar_ausencia_respuesta_aprobacion(ausencia)

        if ausencia.estadoaprobacion == "Aceptado":
            PermisoManager(self.db).actualizar_permisos(ausencia, ausencia.fkpersona)

        return ausencia
