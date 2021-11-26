from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from ...asistencia.tipoausencia.managers import *
from ...notificaciones.correo_rrhh.managers import *
from ...personal.organigrama.managers import *
from ...personal.persona.managers import *
from datetime import datetime, timedelta, time, date
from .models import *
from ..tipoausencia.models import *
from ...usuarios.ajustes.models import *
from ...asistencia.asistenciapersonal.models import *
from sqlalchemy.sql import func, and_



class LicenciaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Ausencia, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def obtener_x_id(self, id):
        return self.db.query(self.entity).filter(self.entity.id == id).first()


    def listar_todo(self):
        return self.db.query(self.entity).join(Tipoausencia).filter(self.entity.enabled == True).filter(Tipoausencia.tipo == "Licencia").all()

    def insert(self, diccionary):

        if diccionary['tiempo_duracion'] == "Hora":

            diccionary['horai'] = datetime.strptime('01/01/2000 ' + diccionary['horai'], '%d/%m/%Y %H:%M')
            diccionary['horaf'] = diccionary['horai'] + timedelta(hours=int(diccionary['tiempo']))


            diccionary['fechai'] = datetime.strptime(diccionary['fechai'], '%d/%m/%Y')
            diccionary['fechaf'] = datetime.strptime(diccionary['fechaf'], '%d/%m/%Y')

        elif diccionary['tiempo_duracion'] == "Dia":

            diccionario = dict(dias=diccionary['tiempo'], fechai= diccionary['fechai'])
            fechafin = BitacoraManager(self.db).obtener_fechafin(diccionario)
            diccionary['fechai'] = datetime.strptime(diccionary['fechai'], '%d/%m/%Y')
            diccionary['fechaf'] = datetime.strptime(fechafin, '%d/%m/%Y')

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

        diccionary['tipo'] = "Licencia"

        superiores = OrganigramaManager(self.db).obtener_autorizacion_aprobacion(diccionary['fkpersona'])

        diccionary['fkautorizacion'] = superiores['fkautorizacion']
        diccionary['fkaprobacion'] = superiores['fkaprobacion']
        diccionary['estadoautorizacion'] = superiores['estadoautorizacion']
        diccionary['estadoaprobacion'] = superiores['estadoaprobacion']

        objeto = LicenciaManager(self.db).entity(**diccionary)


        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        CorreoManager(self.db).notificar_ausencia(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Licencia.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=a.id)
        super().insert(b)

        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico licencia.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=a.id)
        super().insert(b)
        return a


    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó licencia.", fecha=fecha,
                     tabla="cb_ausencia_solicitud", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x


    def actualizar_licencias(self, objeto,persona):

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

        ausencia = super().update(ausencia)
        b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Autorizacion Licencia.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=ausencia.id)
        super().insert(b)

        if not ausencia.persona.empleado[0].aprobacion:

            if ausencia.estadoautorizacion == "Aceptado":
                LicenciaManager(self.db).actualizar_licencias(ausencia, ausencia.fkpersona)


        idsuperior = CorreoManager(self.db).notificar_ausencia_respuesta_autorizacion(ausencia)

        return ausencia

    def aprobacion(self, diccionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        ausencia = self.db.query(Ausencia).filter(Ausencia.id == diccionary['id']).first()
        ausencia.estadoaprobacion = diccionary['estadoaprobacion']
        ausencia.respuestaaprobacion = diccionary['respuestaaprobacion']

        ausencia = super().update(ausencia)
        b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Aprobacion Licencia.",
                     fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=ausencia.id)
        super().insert(b)

        idsuperior = CorreoManager(self.db).notificar_ausencia_respuesta_aprobacion(ausencia)

        if ausencia.estadoautorizacion == "Aceptado":
            LicenciaManager(self.db).actualizar_licencias(ausencia, ausencia.fkpersona)

        return ausencia
