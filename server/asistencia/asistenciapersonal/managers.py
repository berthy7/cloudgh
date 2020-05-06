from ..ausencia.managers import AusenciaManager
from ..asignacion.managers import AsignacionManager
from ...personal.persona.models import *


from ..asignacion.models import Asignacion
from ..politicas.models import Politicas
from ...operaciones.bitacora.models import Bitacora
from ...personal.persona.models import Empleado
from ...control.tarea.models import Tarea
from ...usuarios.ajustes.models import *
from ...calendario.feriado.models import *

from ...operaciones.bitacora.managers import BitacoraManager
from ...dispositivos.marcaciones.managers import MarcacionesManager
from ...personal.persona.managers import PersonaManager

from sqlalchemy.sql import func
from datetime import datetime, timedelta, time, date
from dateutil.relativedelta import relativedelta

from server.common.managers import SuperManager
from .models import *

import calendar
import pytz


class AsistenciaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Asistencia,db)

    def existe_horario(self,fkpersona,fecha):

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == fkpersona).filter(func.to_date(Asistencia.fecha).between(fecha,fecha)).all()
        else:
            # version postgres
            asistencia_personal = self.db.query(Asistencia).filter(Asistencia.fkpersona == fkpersona).filter(
                func.date(Asistencia.fecha) == fecha).all()

        if len(asistencia_personal) !=0:
            return False
        else:
            return True

    def rango_fechas(self,fechai, fechaf):
        rango = []
        dias_totales = (fechaf - fechai).days
        for days in range(dias_totales + 1):
            fecha = fechai + relativedelta(days=days)
            rango.append(fecha)
        return rango

    def crear_horarios(self,fechai, fechaf):
        fechas = AsistenciaManager(self.db).rango_fechas(fechai, fechaf)
        for fech in fechas:
            fecha_hoy = fech.date()
            dia =calendar.day_name[fecha_hoy.weekday()]
            asignacion = self.db.query(Asignacion).all()

            for asig in asignacion:
                respuesta = False
                personal = asig.fkpersona
                periodo = asig.fkperiodo

                crear_horario = AsistenciaManager(self.db).existe_horario(personal,fecha_hoy)

                if crear_horario:
                    for semanal in asig.periodo.semanal.semanaldetalle:
                        if dia == "Monday":
                            respuesta = semanal.lunes
                        elif dia == "Tuesday":
                            respuesta = semanal.martes
                        elif dia == "Wednesday":
                            respuesta = semanal.miercoles
                        elif dia == "Thursday":
                            respuesta = semanal.jueves
                        elif dia == "Friday":
                            respuesta = semanal.viernes
                        elif dia == "Saturday":
                            respuesta = semanal.sabado
                        elif dia =="Sunday":
                            respuesta = semanal.domingo

                        if respuesta:
                            for hora in semanal.dia.hora:
                                observacion = "Falta"
                                codigo_empleado = self.db.query(Empleado).filter(Empleado.fkpersona == personal).one()
                                ausencia = AusenciaManager(self.db).obtener_ausencia(personal, fecha_hoy)
                                feriado = AsistenciaManager(self.db).obtener_feriado(personal, fecha_hoy)
                                if feriado == "":
                                    if ausencia != "":
                                        observacion = ausencia
                                else:
                                    observacion = feriado

                                reg = Asistencia(fkpersona=personal, codigo=codigo_empleado.codigo, nombrecompleto=asig.persona.fullname, entradamin=hora.entradamin,
                                                 entrada=hora.entrada, entradamax=hora.entradamax, salidamin=hora.salidamin, salida=hora.salida,
                                                 salidamax=hora.salidamax, fecha=fecha_hoy, observacion=observacion)

                                self.db.add(reg)

            self.db.commit()

        return True

    def listar_por_dia(self):
        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha = fecha_zona
        fechahoy = str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)
        fechahoy = datetime.strptime(fechahoy, '%d/%m/%Y')

        fechafinn = fechahoy + timedelta(days=1)

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(self.entity).filter(func.to_date(self.entity.fecha) == fechahoy).order_by(self.entity.mentrada.asc()).all()
        else:
            # version postgres
            objeto = self.db.query(self.entity).filter(func.date(self.entity.fecha) == fechahoy).order_by(
                self.entity.mentrada.asc()).all()

        for obj in objeto:

            if obj.enabled == False:
                obj.extra = None


            for ob in obj.autorizacion:
                if ob.enabled:

                    obj.extra = ob.horaextra

        return objeto

    def filtrar(self, fechainicio, fechafin):
        list = {}
        c = 0

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(self.entity).filter(func.to_date(self.entity.fecha).between(fechainicio, fechafin)).order_by(self.entity.nombrecompleto.asc()).all()

        else:
            # version postgres
            objeto = self.db.query(self.entity).filter(
                func.date(self.entity.fecha).between(fechainicio, fechafin)).order_by(
                self.entity.nombrecompleto.asc()).all()

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
            else:
                extra = "------"

            if x.enabled:
                if x.extra:
                    extra = x.extra.strftime("%H:%M")

                    for ob in x.autorizacion:
                        if ob.enabled:
                            extra = ob.horaextra.strftime("%H:%M")
                else:
                    extra = "------"
            else:
                extra = "------"

            list[c] = dict(id=x.id, codigo=x.codigo, nombre=x.nombrecompleto, fecha=x.fecha.strftime("%d/%m/%Y"),
                           entrada=x.entrada.strftime("%H:%M"),salida=x.salida.strftime("%H:%M"),
                           mentrada=mentrada, msalida=msalida, observacion=x.observacion, retraso=retraso, extra=extra)
            c = c + 1

        return list

    def asignar_marcaciones(self, fechainicio, fechafin):
        list = {}
        c = 0

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled== True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(self.entity).filter(func.to_date(self.entity.fecha).between(fechainicio, fechafin)).order_by(self.entity.id.desc()).all()

        else:
            # version postgres
            objeto = self.db.query(self.entity).filter(
                func.date(self.entity.fecha).between(fechainicio, fechafin)).order_by(self.entity.id.desc()).all()

        for x in objeto:
            if x.mentrada is None:
                marcaciones = MarcacionesManager(self.db).obtener_marcaciones(x.codigo,x.fecha,x.fecha)

                for marca in marcaciones:
                    if marca.time.time() > x.entradamin.time():
                        if marca.time.time() < x.entradamax.time():
                            AsistenciaManager(self.db).actualizar_marcacion_entrada(x,marca.time)
                            break

            if x.msalida is None:
                marcaciones = MarcacionesManager(self.db).obtener_marcaciones(x.codigo, x.fecha, x.fecha)

                for marca in marcaciones:
                    if marca.time.time() > x.salidamin.time():
                        if marca.time.time() < x.salidamax.time():
                            AsistenciaManager(self.db).actualizar_marcacion_salida(x,marca.time)
                            break

        return list

    def actualizar_marcacion_entrada(self,horario,marca):
        retraso = None
        idempresa= horario.persona.empleado[0].sucursal.empresa.id
        politica_empresa = self.db.query(Politicas).filter(Politicas.fkempresa == idempresa).first()
        politica = ""

        if politica_empresa:
            politica = politica_empresa.toleranciadia

        else:
            politica = 0

        horariopolitica = horario.entrada + timedelta(minutes=politica)

        if marca.time() > horariopolitica.time():
            retraso = marca - timedelta(hours=horariopolitica.hour, minutes=horariopolitica.minute,
                                                                  seconds=horariopolitica.second)

        horario.mentrada = marca
        horario.retraso = retraso
        if horario.observacion == "Falta":
            horario.observacion = ""
        super().update(horario)
        return True

    def actualizar_marcacion_salida(self,horario,marca):
        extra = None
        idempresa= horario.persona.empleado[0].sucursal.empresa.id

        if marca.time() > horario.salida.time():
            extra = marca - timedelta(hours=horario.salida.hour, minutes=horario.salida.minute,
                                        seconds=horario.salida.second)

        horario.msalida = marca
        horario.extra = extra
        if horario.observacion == "Falta":
            horario.observacion = ""
        super().update(horario)
        return True

    def insertar_marcaciones(self,fecha,codigo):
        list = {}
        c = 0

        x= self.db.query(self.entity).filter(self.entity.codigo == codigo).filter(self.entity.fecha == fecha.date()).order_by(self.entity.id.asc()).first()

        if x:
            if x.mentrada is None:
                if fecha.time() > x.entradamin.time():
                    if fecha.time() < x.entradamax.time():
                        AsistenciaManager(self.db).actualizar_marcacion_entrada(x,fecha)

            if x.msalida is None:

                if fecha.time() > x.salidamin.time():
                    if fecha.time() < x.salidamax.time():
                        AsistenciaManager(self.db).actualizar_marcacion_salida(x,fecha)

        return list

    def insert_by_range(self, usuario, ip, fechaini, fechafin, fkpersona):
        fecha = BitacoraManager(self.db).fecha_actual()
        fecha_hoy = date.today()
        dia = calendar.day_name[fecha_hoy.weekday()]
        asignacion = self.db.query(Asignacion).filter(Asignacion.fkpersona == fkpersona).all()

        fechaini_str = fechaini
        fechaini_obj = datetime.strptime(fechaini_str, '%Y-%m-%d')
        fechafin_str = fechafin
        fechafin_obj = datetime.strptime(fechafin_str, '%Y-%m-%d')

        while fechaini_obj <= fechafin_obj:
            dia_rev = calendar.day_name[fechaini_obj.weekday()]

            for asig in asignacion:
                respuesta = False
                personal = asig.fkpersona
                periodo = asig.fkperiodo

                crear_horario = AsistenciaManager(self.db).existe_horario(personal, fechaini_obj)

                if crear_horario:
                    for semanal in asig.periodo.semanal.semanaldetalle:
                        if dia_rev == "Monday":
                            respuesta = semanal.lunes
                        elif dia_rev == "Tuesday":
                            respuesta = semanal.martes
                        elif dia_rev == "Wednesday":
                            respuesta = semanal.miercoles
                        elif dia_rev == "Thursday":
                            respuesta = semanal.jueves
                        elif dia_rev == "Friday":
                            respuesta = semanal.viernes
                        elif dia_rev == "Saturday":
                            respuesta = semanal.sabado
                        elif dia_rev =="Sunday":
                            respuesta = semanal.domingo

                        if respuesta:
                            for hora in semanal.dia.hora:
                                codigo_empleado = self.db.query(Empleado).filter(Empleado.fkpersona == personal).one()
                                reg = Asistencia(fkpersona=personal, codigo=codigo_empleado.codigo, nombrecompleto=asig.persona.fullname, entradamin=hora.entradamin,
                                                 entrada=hora.entrada, entradamax=hora.entradamax, salidamin=hora.salidamin, salida=hora.salida,
                                                 salidamax=hora.salidamax, fecha=fechaini_obj, observacion="Falta")


                                self.db.add(reg)

            fechaini_obj = fechaini_obj + timedelta(days=1)

        self.db.commit()

        b = Bitacora(fkusuario=usuario, ip=ip, accion="Registro Empresa.",
                     fecha=fecha, tabla="rrhh_empresa")
        super().insert(b)
        return b

    def insert(self, usuario, ip):
        fecha = BitacoraManager(self.db).fecha_actual()
        fecha_hoy = date.today()
        dia =calendar.day_name[fecha_hoy.weekday()]
        asignacion = self.db.query(Asignacion).all()

        for asig in asignacion:
            respuesta = False
            personal = asig.fkpersona
            periodo = asig.fkperiodo

            crear_horario = AsistenciaManager(self.db).existe_horario(personal,fecha_hoy)

            if crear_horario:
                for semanal in asig.periodo.semanal.semanaldetalle:
                    if dia == "Monday":
                        respuesta = semanal.lunes
                    elif dia == "Tuesday":
                        respuesta = semanal.martes
                    elif dia == "Wednesday":
                        respuesta = semanal.miercoles
                    elif dia == "Thursday":
                        respuesta = semanal.jueves
                    elif dia == "Friday":
                        respuesta = semanal.viernes
                    elif dia == "Saturday":
                        respuesta = semanal.sabado
                    elif dia =="Sunday":
                        respuesta = semanal.domingo

                    if respuesta:
                        for hora in semanal.dia.hora:
                            codigo_empleado = self.db.query(Empleado).filter(Empleado.fkpersona == personal).one()

                            ausencia = AusenciaManager(self.db).obtener_ausencia(personal,fecha_hoy)

                            reg = Asistencia(fkpersona=personal, codigo=codigo_empleado.codigo, nombrecompleto=asig.persona.fullname, entradamin=hora.entradamin,
                                             entrada=hora.entrada, entradamax=hora.entradamax, salidamin=hora.salidamin, salida=hora.salida,
                                             salidamax=hora.salidamax, fecha=fecha_hoy, observacion="Falta")



                            self.db.add(reg)

        self.db.commit()

        b = Bitacora(fkusuario=usuario, ip=ip, accion="Registro Empresa.",
                     fecha=fecha, tabla="rrhh_empresa")
        super().insert(b)
        return b

    def obtener_horarios(self, fechainicio, fechafin,id):
        list = {}
        c = 0
        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(self.entity).filter(self.entity.fkpersona == id).filter(func.to_date(self.entity.fecha).between(fechainicio, fechafin)).order_by(self.entity.fecha.asc(),self.entity.entrada.asc()).all()

        else:
            # version postgres
            objeto = self.db.query(self.entity).filter(self.entity.fkpersona == id).filter(func.date(self.entity.fecha).between(fechainicio, fechafin)).order_by(self.entity.fecha.asc(),self.entity.entrada.asc()).all()

        for x in objeto:

            list[c] = x
            c = c + 1

        return list

    def crear_pdf(self, per, diccionary, html):
        fechainicio = datetime.strptime(diccionary['fechainicio'], '%d/%m/%Y')
        fechafin = datetime.strptime(diccionary['fechafin'], '%d/%m/%Y')

        persona = PersonaManager(self.db).obtener_persona(per['id_persona'])
        politicas = persona.empleado[0].sucursal.empresa.politicas[0]
        asignaciones = AsignacionManager(self.db).obtener_horarios(per['id_persona'])
        detalle = ""
        horarios = AsistenciaManager(self.db).obtener_horarios(diccionary['fechainicio'], diccionary['fechafin'],
                                                               per['id_persona'])

        lista_fechas = AsistenciaManager(self.db).rango_fechas(fechainicio, fechafin)
        contador = 0
        contador_aux = 0
        lista_auxiliar = list()
        retrasototaldelta = timedelta(hours=0, minutes=0)
        extratotaldelta = timedelta(hours=0, minutes=0)
        trabajototaldelta = timedelta(hours=0, minutes=0)

        while contador < len(horarios):

            for fechadia in lista_fechas:
                mentrada = ""
                msalida = ""
                mentrada2 = ""
                msalida2 = ""
                retraso = ""
                retraso2 = ""
                extra = ""
                extra2 = ""
                retrasodelta = ""
                extradelta = ""
                retrasodia = ""
                extradia = ""
                trabajodelta = ""
                trabajodia = ""
                trabajo = ""
                trabajo2 = ""
                observacion = ""
                observacion2 = ""
                observaciondia = ""

                retrasototal = ""
                extratotal = ""
                trabajototal = ""

                dia = BitacoraManager(self.db).obtener_dia(fechadia)
                try:
                    if horarios[contador].fecha.strftime("%d/%m/%Y") == fechadia.strftime("%d/%m/%Y"):

                        lista_auxiliar.append(horarios[contador])
                        auxiliar = contador + 1
                        try:
                            if horarios[auxiliar].fecha.strftime("%d/%m/%Y") == fechadia.strftime("%d/%m/%Y"):
                                lista_auxiliar.append(horarios[auxiliar])
                                contador = contador + 1

                        except Exception as ex:
                            print(ex)
                        if len(lista_auxiliar) == 1:
                            # 1 horario

                            if lista_auxiliar[0].mentrada:
                                mentrada = lista_auxiliar[0].mentrada.strftime("%H:%M")
                            else:
                                mentrada = "-----"

                            if lista_auxiliar[0].msalida:
                                msalida = lista_auxiliar[0].msalida.strftime("%H:%M")
                            else:
                                msalida = "-----"

                            # calculo del retraso
                            if lista_auxiliar[0].retraso:
                                aux_retraso = (lista_auxiliar[0].retraso.hour * 60) + lista_auxiliar[0].retraso.minute
                                if int(aux_retraso) >= politicas.toleranciadia:
                                    retrasocalculado = lista_auxiliar[0].retraso #- timedelta(minutes=politicas.toleranciadia)
                                    retrasodia = retrasocalculado.strftime("%H:%M")
                                    retrasototaldelta = retrasototaldelta + timedelta(hours=retrasocalculado.hour, minutes=retrasocalculado.minute)
                                else:
                                    retrasodia = "-----"
                            else:
                                retrasodia = "-----"

                            # calculo del extra
                            if lista_auxiliar[0].extra and lista_auxiliar[0].enabled:
                                    extradia = lista_auxiliar[0].extra.strftime("%H:%M")
                                    for ob in lista_auxiliar[0].autorizacion:
                                        if ob.enabled:
                                            extradia = ob.horaextra.strftime("%H:%M")

                                    extratotaldelta = extratotaldelta + timedelta(hours=ob.horaextra.hour, minutes=ob.horaextra.minute)
                            else:
                                extradia = "-----"

                            # calculo de horas trabajadas
                            if lista_auxiliar[0].mentrada:
                                if lista_auxiliar[0].msalida:

                                    trabajodelta = timedelta(hours=lista_auxiliar[0].msalida.hour, minutes=lista_auxiliar[0].msalida.minute) -  timedelta(hours=lista_auxiliar[0].mentrada.hour, minutes=lista_auxiliar[0].mentrada.minute)
                                    trabajototaldelta = trabajototaldelta + trabajodelta

                                    trabajo_cadena = str(trabajodelta)
                                    trabajodia = trabajo_cadena[0:len(trabajo_cadena) - 3]
                                    if len(trabajo_cadena) < 8:
                                        trabajodia = "0"+trabajodia

                            # observacion
                            observaciondia = lista_auxiliar[0].observacion

                        else:
                            # 2 horarios
                            if lista_auxiliar[0].mentrada:
                                mentrada = lista_auxiliar[0].mentrada.strftime("%H:%M")
                            else:
                                mentrada = "-----"

                            if lista_auxiliar[0].msalida:
                                msalida = lista_auxiliar[0].msalida.strftime("%H:%M")
                            else:
                                msalida = "-----"

                            if lista_auxiliar[1].mentrada:
                                mentrada2 = lista_auxiliar[1].mentrada.strftime("%H:%M")
                            else:
                                mentrada2 = "-----"

                            if lista_auxiliar[1].msalida:
                                msalida2 = lista_auxiliar[1].msalida.strftime("%H:%M")
                            else:
                                msalida2 = "-----"

                            #calculo del retraso
                            if lista_auxiliar[0].retraso:
                                if lista_auxiliar[1].retraso:
                                    #suma
                                    retraso = lista_auxiliar[0].retraso
                                    retraso2 = lista_auxiliar[1].retraso

                                    retrasodelta = timedelta(hours=retraso.hour, minutes=retraso.minute) + timedelta(hours=retraso2.hour, minutes=retraso2.minute)

                                    #if int(lista_auxiliar[0].retraso.minute) >= politicas.toleranciadia:
                                    retrasodate = datetime.strptime('01/01/2000 ' + str(retrasodelta),'%d/%m/%Y %H:%M:%S')
                                    retrasodia = retrasodate.strftime("%H:%M")
                                    retrasototaldelta = retrasototaldelta + timedelta(hours=retrasodate.hour, minutes=retrasodate.minute)
                                else:
                                    aux_retraso = lista_auxiliar[0].retraso
                                    retrasodia = aux_retraso.strftime("%H:%M")
                                    retrasototaldelta = retrasototaldelta + timedelta(hours=aux_retraso.hour, minutes=aux_retraso.minute)
                            else:
                                if lista_auxiliar[1].retraso:
                                    aux_retraso = lista_auxiliar[1].retraso
                                    retrasodia = aux_retraso.strftime("%H:%M")
                                    retrasototaldelta = retrasototaldelta + timedelta(hours=aux_retraso.hour, minutes=aux_retraso.minute)
                                else:
                                    retrasodia = "-----"

                            # calculo del extra
                            if lista_auxiliar[0].extra and lista_auxiliar[0].enabled:
                                if lista_auxiliar[1].extra and lista_auxiliar[1].enabled:
                                    # suma
                                    extra = lista_auxiliar[0].extra
                                    extra2 = lista_auxiliar[1].extra

                                    extradelta = timedelta(hours=extra.hour, minutes=extra.minute) + timedelta(hours=extra2.hour, minutes=extra2.minute)
                                    extradate = datetime.strptime('01/01/2000 ' + str(extradelta),'%d/%m/%Y %H:%M:%S')
                                    extradia = extradate.strftime("%H:%M")

                                    for ob in lista_auxiliar[0].autorizacion:
                                        if ob.enabled:
                                            extraday = ob.horaextra.strftime("%H:%M")

                                    extratotaldelta = extratotaldelta + timedelta(hours=ob.horaextra.hour, minutes=ob.horaextra.minute)

                                    for ob in lista_auxiliar[1].autorizacion:
                                        if ob.enabled:
                                            extraday = ob.horaextra.strftime("%H:%M")

                                    extratotaldelta = extratotaldelta + timedelta(hours=ob.horaextra.hour, minutes=ob.horaextra.minute)
                                else:
                                    extradia = lista_auxiliar[0].extra.strftime("%H:%M")
                                    for ob in lista_auxiliar[0].autorizacion:
                                        if ob.enabled:
                                            extradia = ob.horaextra.strftime("%H:%M")

                                    extratotaldelta = extratotaldelta + timedelta(hours=ob.horaextra.hour, minutes=ob.horaextra.minute)
                            else:
                                if lista_auxiliar[1].extra and lista_auxiliar[1].enabled:
                                    extradia = lista_auxiliar[1].extra.strftime("%H:%M")
                                    for ob in lista_auxiliar[1].autorizacion:
                                        if ob.enabled:
                                            extradia = ob.horaextra.strftime("%H:%M")

                                    extratotaldelta = extratotaldelta + timedelta(hours=ob.horaextra.hour, minutes=ob.horaextra.minute)
                                else:
                                    extradia = "-----"

                            # calculo de horas trabajadas
                            if lista_auxiliar[0].mentrada:
                                if lista_auxiliar[0].msalida:
                                    trabajo = timedelta(hours=lista_auxiliar[0].msalida.hour, minutes=lista_auxiliar[0].msalida.minute) -  timedelta(hours=lista_auxiliar[0].mentrada.hour, minutes=lista_auxiliar[0].mentrada.minute)
                                    trabajototaldelta = trabajototaldelta + trabajo

                            if lista_auxiliar[1].mentrada:
                                if lista_auxiliar[1].msalida:
                                    trabajo2 = timedelta(hours=lista_auxiliar[1].msalida.hour, minutes=lista_auxiliar[1].msalida.minute) -  timedelta(hours=lista_auxiliar[1].mentrada.hour, minutes=lista_auxiliar[1].mentrada.minute)
                                    trabajototaldelta = trabajototaldelta + trabajo2

                            if trabajo != "":
                                if trabajo2 != "":
                                    trabajodelta = trabajo + trabajo2

                                    trabajo_cadena = str(trabajodelta)
                                    trabajodia = trabajo_cadena[0:len(trabajo_cadena) - 3]
                                    if len(trabajo_cadena) < 8:
                                        trabajodia = "0"+trabajodia

                                else:
                                    trabajodelta = trabajo

                                    trabajo_cadena = str(trabajodelta)
                                    trabajodia = trabajo_cadena[0:len(trabajo_cadena) - 3]
                                    if len(trabajo_cadena) < 8:
                                        trabajodia = "0" + trabajodia

                            else:
                                if trabajo2 != "":
                                    trabajodelta = trabajo2

                                    trabajo_cadena = str(trabajodelta)
                                    trabajodia = trabajo_cadena[0:len(trabajo_cadena) - 3]
                                    if len(trabajo_cadena) < 8:
                                        trabajodia = "0"+trabajodia
                                else:
                                    trabajodia = "-----"

                            # caldulo de observacion
                            if lista_auxiliar[0].observacion != "":
                                observaciondia = lista_auxiliar[0].observacion
                            elif lista_auxiliar[1].observacion != "":
                                observaciondia = lista_auxiliar[1].observacion
                            else:
                                observaciondia = lista_auxiliar[1].observacion


                            observacion = lista_auxiliar[0].observacion

                        lista_auxiliar.clear()

                        contador_aux = contador_aux + 1
                        contador = contador + 1
                except Exception as ex:
                    print(ex)

                detalle = detalle + "<tr style='font-size: 12px; border: 0px; '>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(fechadia.strftime("%d/%m/%Y")) + "</font></td>" \
                                    "   <td colspan='1' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(dia) + "</font></td>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(mentrada) + "</font></td>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(msalida) + "</font></td>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(mentrada2) + "</font></td>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(msalida2) + "</font></td>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(retrasodia) + "</font></td>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(extradia) + "</font></td>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(trabajodia) + "</font></td>" \
                                    "   <td colspan='2' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font></font></td>" \
                                    "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(observaciondia) + "</font></td>" \
                                    "</tr>" \

        retrasototaldelta = retrasototaldelta - timedelta(minutes=politicas.toleranciames)
        retrasototal_cadena = str(retrasototaldelta)
        retrasototal = retrasototal_cadena[0:len(retrasototal_cadena) - 3]
        if len(retrasototal_cadena) < 8:
            retrasototal = "0" + retrasototal

        extratotal_cadena = str(extratotaldelta)
        extratotal = extratotal_cadena[0:len(extratotal_cadena) - 3]
        if len(extratotal_cadena) < 8:
            extratotal = "0" + extratotal

        trabajototal_cadena = str(trabajototaldelta)

        lista_trabajototal = trabajototal_cadena.split(' ')

        if len(trabajototal_cadena) < 9:
            listatiempo = lista_trabajototal[0].split(':')
            trabajototal = listatiempo[0] + ":" + listatiempo[1]
        else:

            listatiempo = lista_trabajototal[2].split(':')
            hora_dias = lista_trabajototal[0]
            hora = listatiempo[0]
            minuto = listatiempo[1]

            horatotal = 24*int(hora_dias)
            horatotal = horatotal + int(hora)

            trabajototal = str(horatotal) + ":" + minuto

        if len(trabajototal_cadena) < 8:
            trabajototal = "0" + trabajototal

        print(trabajototal)

        html += "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "<tr color='#ffffff' >" \
                "   <th colspan='22' scope='colgroup' align='left' style='background-color: #1976d2; font-size=4; color: white; margin-top: 4px'>BOLETA DE ASISTENCIA</th>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Nombres y Apellidos: </strong></td>" \
                "   <td colspan='12' scope='colgroup'align='left'><font>" + str(persona.fullname) + "</font></td>" \
                "   <td colspan='5' style='border-left: 1px solid grey ' scope='colgroup'align='left'><font>Tolerancia Dia " + str(politicas.toleranciadia) + " Min</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Cargo: </strong></td>" \
                "   <td colspan='12' scope='colgroup'align='left'><font>" + str(persona.empleado[0].cargo.nombre) + "</font></td>" \
                "   <td colspan='5' style='border-left: 1px solid grey '  scope='colgroup'align='left'><font>Tolerancia Mes " + str(politicas.toleranciames) + " Min</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Codigo: </strong></td>" \
                "   <td colspan='12' scope='colgroup'align='left'><font>" + str(persona.empleado[0].codigo) + "</font></td>" \
                "   <td colspan='5' style='border-left: 1px solid grey ' scope='colgroup'align='left'><font></font></td>" \
                "</tr>" \
                "<tr color='#ffffff' >" \
                "   <th colspan='3' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Lunes</th>" \
                "   <th colspan='3' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Martes</th>" \
                "   <th colspan='3' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Miercoles</th>" \
                "   <th colspan='3' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Jueves</th>" \
                "   <th colspan='3' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Viernes</th>" \
                "   <th colspan='3' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Sabado</th>" \
                "   <th colspan='4' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Domingo</th>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(asignaciones[0]) + "</font></td>" \
                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(asignaciones[1]) + "</font></td>" \
                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(asignaciones[2]) + "</font></td>" \
                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(asignaciones[3]) + "</font></td>" \
                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(asignaciones[4]) + "</font></td>" \
                "   <td colspan='3' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(asignaciones[5]) + "</font></td>" \
                "   <td colspan='4' style='border-right: 1px solid grey 'scope='colgroup'align='center'><font>" + str(asignaciones[6]) + "</font></td>" \
                "</tr>" \
                "<tr color='#ffffff' >" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Fecha</th>" \
                "   <th colspan='1' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Dia</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Mar. 1</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Mar. 2</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Mar. 3</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Mar. 4</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Retraso</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Sobre Tiempo</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Trabajo Efect.</th>" \
                "   <th colspan='2' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Recargo nocturno</th>" \
                "   <th colspan='3' scope='colgroup' align='center' style='background-color: #a3a3a3; font-size=4; color: white; margin-top: 4px'>Observaciones</th>" \
                "</tr>" \
                "" + detalle + "" \
                "<tr style='font-size: 12px; border: 0px; border-top:1px solid grey; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Total Horas Retraso: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(retrasototal) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Total Horas Extras: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(extratotal) + "</font></td>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "   <td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Total Horas Trabajadas: </strong></td>" \
                "   <td colspan='17' scope='colgroup'align='left'><font>" + str(trabajototal) + "</font></td>" \
                "</tr>" \
                "</table>" \
              "</br>"

        return html

    def actualizar_ausencia(self, ausencia):

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            asistenciapersonal = self.db.query(self.entity).filter(self.entity.fkpersona == ausencia.fkpersona).filter(func.to_date(self.entity.fecha).between(ausencia.fechai, ausencia.fechaf)).order_by(self.entity.fecha.asc()).all()

        else:
            # version postgres
            asistenciapersonal = self.db.query(self.entity).filter(self.entity.fkpersona == ausencia.fkpersona).filter(
                func.date(self.entity.fecha).between(ausencia.fechai, ausencia.fechaf)).order_by(
                self.entity.fecha.asc()).all()


        for asistencia in asistenciapersonal:
            asistencia.observacion = ausencia.tipoausencia.nombre
            super().update(asistencia)

        return ausencia

    def obtener_localizacion(self, feriado):
        list = {}
        asistencia_personal = 0

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if feriado.fkpais:

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(Empleado.fkpais == feriado.fkpais).filter(
                    func.to_date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(Empleado.fkpais == feriado.fkpais).filter(
                    func.date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()

        if feriado.fkdepartamento:

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(Empleado.fkdepartamento == feriado.fkdepartamento).filter(
                    func.to_date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(Empleado.fkdepartamento == feriado.fkdepartamento).filter(
                    func.date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()

        if feriado.fkciudad:

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(Empleado.fkciudad == feriado.fkciudad).filter(
                    func.to_date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(Empleado.fkciudad == feriado.fkciudad).filter(
                    func.date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()

        if feriado.fksucursal:

            if ajuste.oracle:
                # version oracle
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(Empleado.fksucursal == feriado.fksucursal).filter(
                    func.to_date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()
            else:
                # version postgres
                asistencia_personal = self.db.query(Asistencia).join(Persona).join(Empleado).filter(Empleado.fksucursal == feriado.fksucursal).filter(
                    func.date(Asistencia.fecha).between(feriado.fecha, feriado.fecha)).all()

        return asistencia_personal

    def obtener_feriado(self,fkpersona,fecha):
        respuesta = ""

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled== True).first()

        if ajuste.oracle:
            # version oracle
            feriado = self.db.query(Feriado).filter(Feriado.fecha == fecha).filter(Feriado.enabled == True).first()

        else:
            # version postgres
            feriado = self.db.query(Feriado).filter(Feriado.fecha == fecha).filter(Feriado.enabled == True).first()

        persona = self.db.query(Persona).filter(Persona.id == fkpersona).filter(Persona.enabled == True).first()

        if feriado:

            if feriado.fkpais:
                if feriado.fkpais == persona.empleado[0].fkpais:
                    respuesta = feriado.nombre

            if feriado.fkdepartamento:
                if feriado.fkdepartamento == persona.empleado[0].fkdepartamento:
                    respuesta = feriado.nombre

            if feriado.fkciudad:
                if feriado.fkciudad == persona.empleado[0].fkciudad:
                    respuesta = feriado.nombre

            if feriado.fksucursal:
                if feriado.fksucursal == persona.empleado[0].fksucursal:
                    respuesta = feriado.nombre

        return respuesta

    def obtener_asistencia(self, key):
        x = self.db.query(self.entity).filter(self.entity.id == key).first()
        return x
