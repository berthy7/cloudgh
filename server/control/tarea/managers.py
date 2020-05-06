from ...configuraciones.sucursal.models import *
from ...operaciones.bitacora.managers import *
from ...dispositivos.marcaciones.models import *
from ...usuarios.ajustes.models import *
from .models import *
from sqlalchemy.sql import func


class TareaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Tarea, db)

    def obtener_tareas(self, fkpersona):

        return self.db.query(self.entity).filter(self.entity.fkpersona == fkpersona).all()

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def list_all(self):
        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha = fecha_zona
        fechahoy = str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)
        fechahoy = datetime.strptime(fechahoy, '%d/%m/%Y')

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(func.to_date(self.entity.fechaInicio).between(fechahoy, fechahoy)))

        else:
            # version postgres
            return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
                func.date(self.entity.fechaInicio).between(fechahoy, fechahoy)))


    def list_by_day(self):
        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha = fecha_zona
        fechahoy = str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)
        fechahoy = datetime.strptime(fechahoy, '%d/%m/%Y')

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            return dict(tareas=self.db.query(self.entity).filter(self.entity.enabled == True).filter(func.to_date(self.entity.fechaInicio).between(fechahoy, fechahoy)).all())

        else:
            # version postgres
            return dict(tareas=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
                func.date(self.entity.fechaInicio).between(fechahoy, fechahoy)))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip_maquina, accion="Registro Empresa.",
                     fecha=fecha, tabla="rrhh_empresa", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Empresa.",
                     fecha=fecha, tabla="rrhh_empresa", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Empresa.", fecha=fecha,
                     tabla="rrhh_empresa", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def insert_task(self, descripcion, prioridad, estimacion, fechaInicio, fechaFin, fktarea, fkproyecto, estado):
        fecha = BitacoraManager(self.db).fecha_actual()
        tarea = Tarea(descripcion=descripcion, prioridad=prioridad, estimacion=estimacion, fechaInicio=fechaInicio, fechaFin=fechaFin, fechaCreacion=fecha,
                          fktarea=fktarea, fkproyecto=fkproyecto, estado=estado)
        a = super().insert(tarea)
        b = Bitacora(accion="Registro Tarea.", fecha=fecha, tabla="cb_control_tarea", identificador=a.id)
        super().insert(b)
        return a

    def update_task(self, id, descripcion, prioridad, estimacion, fechaInicio, fechaFin, fktarea, fkproyecto, estado):
        fecha = BitacoraManager(self.db).fecha_actual()

        t = self.db.query(Tarea).filter(Tarea.id == id).one()
        t.descripcion = descripcion
        t.prioridad = prioridad
        t.estimacion = estimacion
        t.fechaInicio = fechaInicio
        t.fechaFin = fechaFin
        t.fktarea = fktarea
        t.fkproyecto = fkproyecto
        t.estado = estado

        b = Bitacora(accion="Modificó Tarea.", fecha=fecha, tabla="cb_control_tarea", identificador=id)
        super().insert(b)
        a = self.db.merge(t)
        return a

    def delete_task(self, id, ip, user):
        x = self.db.query(Tarea).filter(Tarea.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Tarea.", fecha=fecha, tabla="cb_control_tarea", identificador=id)
        super().insert(b)
        a = self.db.merge(x)
        self.db.commit()

        return a

    def obtener_tareas_dia(self):
        fecha_dia = datetime.now(pytz.timezone('America/La_Paz'))

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            return self.db.query(self.entity).filter(self.entity.enabled == True).filter(
                func.to_date(self.entity.fecha).between(fecha_dia.date(), fecha_dia.date())).all()

        else:
            # version postgres
            return self.db.query(self.entity).filter(self.entity.enabled == True).filter(
                func.date(self.entity.fecha) == fecha_dia.date()).all()






