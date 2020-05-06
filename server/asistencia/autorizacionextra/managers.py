from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from ..asistenciapersonal.models import *
from ...usuarios.ajustes.models import *
from sqlalchemy.sql import func
from datetime import datetime, timedelta, time, date
from .models import *


class AutorizacionextraManager(SuperManager):

    def __init__(self, db):
        super().__init__(Autorizacionextra, db)


    def list_all(self):
        return dict(objects=self.db.query(Asistencia).filter(Asistencia.enabled == True))

    def listar_por_dia(self):
        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha = fecha_zona
        fechahoy = str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)
        fechahoy = datetime.strptime(fechahoy, '%d/%m/%Y')

        fechafinn = fechahoy + timedelta(days=1)
        c = 0

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(Asistencia).filter(Asistencia.extra != None).filter(func.to_date(Asistencia.fecha) == fechahoy).order_by(Asistencia.mentrada.asc()).all()
        else:
            # version postgres
            objeto = self.db.query(Asistencia).filter(Asistencia.extra != None).filter(func.date(Asistencia.fecha) == fechahoy).order_by(
                Asistencia.mentrada.asc()).all()

        for obj in objeto:

            for ob in obj.autorizacion:
                if ob.enabled:

                    obj.extra = ob.horaextra

        return objeto

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fecha = fecha
        objeto.horaextra = datetime.strptime('01/01/2000 ' + objeto.horaextra, '%d/%m/%Y %H:%M')

        a = super().insert(objeto)
        x = self.db.query(Asistencia).filter(Asistencia.id == a.fkasistencia).first()
        x.enabled = a.enabled
        super().update(x)

        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Autorizacion.",
                     fecha=fecha, tabla="cb_asistencia_autorizacionextra", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fecha = fecha
        objeto.horaextra = datetime.strptime('01/01/2000 ' + objeto.horaextra, '%d/%m/%Y %H:%M')

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Autorizacion.",
                     fecha=fecha, tabla="cb_asistencia_autorizacionextra", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id,fkasistencia, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).first()
        y = self.db.query(Asistencia).filter(Asistencia.id == fkasistencia).first()
        x.enabled = False
        y.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Autorizacion.", fecha=fecha,
                     tabla="cb_asistencia_autorizacionextra", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.merge(y)
        self.db.commit()

    def filtrar(self, diccionario, fechainicio, fechafin, idpersona):
        lista = diccionario['lista']
        c = diccionario['contador']
        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(Asistencia).filter(Asistencia.fkpersona == idpersona).filter(Asistencia.extra != None).filter(func.to_date(Asistencia.fecha).between(fechainicio, fechafin)).order_by(Asistencia.nombrecompleto.asc()).all()

        else:
            # version postgres
            objeto = self.db.query(Asistencia).filter(Asistencia.fkpersona == idpersona).filter(Asistencia.extra != None).filter(func.date(Asistencia.fecha).between(fechainicio, fechafin)).order_by(Asistencia.nombrecompleto.asc()).all()

        for x in objeto:
            if x.mentrada:
                mentrada = x.mentrada.strftime("%H:%M")
            else:
                mentrada = "------"

            if x.msalida:
                msalida = x.msalida.strftime("%H:%M")
            else:
                msalida = "------"

            if x.retraso:
                retraso = x.retraso.strftime("%H:%M")
            else:
                retraso = "------"

            if x.extra:
                extra = x.extra.strftime("%H:%M")
                for ob in x.autorizacion:
                    if ob.enabled:
                        extra = ob.horaextra.strftime("%H:%M")
            else:
                extra = "------"

            if x.enabled:
                estado = '<input id="'+str(x.id)+'" onClick="event.preventDefault();autorizarhoras(this)" data-id="'+str(x.id)+'" type="checkbox" class="module chk-col-deep-purple estado_platos" checked /><label for="'+str(x.id)+'"></label>'
            else:
                estado = '<input id="'+str(x.id)+'" onClick="event.preventDefault();autorizarhoras(this)" data-id="'+str(x.id)+'" type="checkbox" class="module chk-col-deep-purple estado_platos"  /><label for="'+str(x.id)+'"></label>'

            lista[c] = dict(id=x.id, codigo=x.codigo, nombre=x.nombrecompleto, fecha=x.fecha.strftime("%d/%m/%Y"),
                           entrada=x.entrada.strftime("%H:%M"),salida=x.salida.strftime("%H:%M"),
                           mentrada=mentrada, msalida=msalida, observacion=x.observacion, retraso=retraso, extra=extra,
                           estado= estado)
            c = c + 1

        diccionario = dict(lista=lista, contador=c)

        return diccionario


    def listar_por_dia_autorizar(self):
        lista = list()
        c = 0
        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha = fecha_zona
        fechahoy = str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)
        fechahoy = datetime.strptime(fechahoy, '%d/%m/%Y')

        fechafinn = fechahoy + timedelta(days=1)

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(Asistencia).filter(Asistencia.extra != None).filter(func.to_date(Asistencia.fecha) == fechahoy).order_by(Asistencia.mentrada.asc()).all()
        else:
            # version postgres
            objeto = self.db.query(Asistencia).filter(Asistencia.extra != None).filter(func.date(Asistencia.fecha) == fechahoy).order_by(
                Asistencia.mentrada.asc()).all()

        for x in objeto:

            for ob in x.autorizacion:
                if ob.enabled:
                    x.extra = ob.horaextra

            if x.mentrada:
                mentrada = x.mentrada.strftime("%H:%M")
            else:
                mentrada = "------"

            if x.msalida:
                msalida = x.msalida.strftime("%H:%M")
            else:
                msalida = "------"

            if x.retraso:
                retraso = x.retraso.strftime("%H:%M")
            else:
                retraso = "------"

            if x.extra:
                extra = x.extra.strftime("%H:%M")
                for ob in x.autorizacion:
                    if ob.enabled:
                        extra = ob.horaextra.strftime("%H:%M")
            else:
                extra = "------"

            if x.enabled:
                estado = '<input id="'+str(x.id)+'" onClick="event.preventDefault();autorizarhoras(this)" data-id="'+str(x.id)+'" type="checkbox" class="module chk-col-deep-purple estado_platos" checked /><label for="'+str(x.id)+'"></label>'
            else:
                estado = '<input id="'+str(x.id)+'" onClick="event.preventDefault();autorizarhoras(this)" data-id="'+str(x.id)+'" type="checkbox" class="module chk-col-deep-purple estado_platos"  /><label for="'+str(x.id)+'"></label>'

            lista.append(dict(id=x.id, codigo=x.codigo, nombre=x.nombrecompleto, fecha=x.fecha.strftime("%d/%m/%Y"),
                           entrada=x.entrada.strftime("%H:%M"),salida=x.salida.strftime("%H:%M"),
                           mentrada=mentrada, msalida=msalida, observacion=x.observacion, retraso=retraso, extra=extra,
                           estado= estado))



        return lista
