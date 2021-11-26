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



class RegularizacionManager(SuperManager):

    def __init__(self, db):
        super().__init__(Regularizacion, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity))

    def obtener_x_id(self, id):
        return self.db.query(self.entity).filter(self.entity.id == id).first()


    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def insert(self, diccionary):


        diccionary['tipo'] = "Regularizacion"

        superiores = OrganigramaManager(self.db).obtener_autorizacion_aprobacion(diccionary['fkpersona'])

        diccionary['fkautorizacion'] = superiores['fkautorizacion']
        diccionary['fkaprobacion'] = superiores['fkaprobacion']
        diccionary['estadoautorizacion'] = superiores['estadoautorizacion']
        diccionary['estadoaprobacion'] = superiores['estadoaprobacion']

        objeto = RegularizacionManager(self.db).entity(**diccionary)


        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        CorreoManager(self.db).notificar_ausencia(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Regularizacion.",
                     fecha=fecha, tabla="cb_ausencia_regularizacion", identificador=a.id)
        super().insert(b)

        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico regularizacion.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=a.id)
        super().insert(b)
        return a


    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó regularizacion.", fecha=fecha,
                     tabla="cb_ausencia_solicitud", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x


    def actualizar_regularizacion(self, objeto):

        for reg in objeto.regularizaciondetalle:
            if reg.entrada:
                x = self.db.query(Asistencia).filter(Asistencia.id == reg.fkasistencia).one()
                x.mentrada = datetime.strptime(str(x.fecha.date()) + " " + str(x.entrada.time())[0:7], '%Y-%m-%d %H:%M:%S')
                x.observacion = "Regularizado"
                self.db.merge(x)
                self.db.commit()

            if reg.salida:
                x = self.db.query(Asistencia).filter(Asistencia.id == reg.fkasistencia).one()
                x.msalida = datetime.strptime(str(x.fecha.date()) +" "+ str(x.salida.time())[0:7], '%Y-%m-%d %H:%M:%S')
                x.observacion = "Regularizado"
                self.db.merge(x)
                self.db.commit()

        return objeto

    def autorizacion(self, diccionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        regularizacion = self.db.query(self.entity).filter(self.entity.id == diccionary['id']).first()
        regularizacion.estadoautorizacion = diccionary['estadoautorizacion']
        regularizacion.respuestaautorizacion = diccionary['respuestaautorizacion']

        regularizacion = super().update(regularizacion)
        b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Autorizacion Regularizacion.",
                     fecha=fecha, tabla="cb_ausencia_solicitud", identificador=regularizacion.id)
        super().insert(b)

        if not regularizacion.persona.empleado[0].aprobacion:

            if regularizacion.estadoautorizacion == "Aceptado":
                RegularizacionManager(self.db).actualizar_regularizacion(regularizacion)


        idsuperior = CorreoManager(self.db).notificar_ausencia_respuesta_autorizacion(regularizacion)

        return regularizacion

    def aprobacion(self, diccionary):
        fecha = BitacoraManager(self.db).fecha_actual()

        regularizacion = self.db.query(self.entity).filter(self.entity.id == diccionary['id']).first()
        regularizacion.estadoaprobacion = diccionary['estadoaprobacion']
        regularizacion.respuestaaprobacion = diccionary['respuestaaprobacion']

        regularizacion = super().update(regularizacion)
        b = Bitacora(fkusuario=diccionary['user'], ip=diccionary['ip'], accion="Aprobacion Regularizacion.",
                     fecha=fecha, tabla="cb_vacaciones_solicitud", identificador=regularizacion.id)
        super().insert(b)

        idsuperior = CorreoManager(self.db).notificar_ausencia_respuesta_aprobacion(regularizacion)

        if regularizacion.estadoautorizacion == "Aceptado":
            RegularizacionManager(self.db).actualizar_regularizacion(regularizacion)

        return regularizacion
