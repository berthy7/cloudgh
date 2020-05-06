from server.common.managers import SuperManager
from .models import *


class PeriodoManager(SuperManager):

    def __init__(self, db):
        super().__init__(Periodo, db)


class AsignacionManager(SuperManager):

    def __init__(self, db):
        super().__init__(Asignacion,db)

    def obtener_horarios(self, id):
        objeto = self.db.query(Asignacion).filter(Asignacion.fkpersona == id).first()
        horario_lunes = "------"
        horario_martes = "-----"
        horario_miercoles = "-----"
        horario_jueves = "-----"
        horario_viernes = "-----"
        horario_sabado = "-----"
        horario_domingo = "-----"
        vectotr_horarios = []

        for horarios in objeto.periodo.semanal.semanaldetalle:
            if horarios.lunes:
                horario_lunes = ""
                for hora in horarios.dia.hora:
                    horario_lunes += "<p>" + str(hora.entrada.strftime("%H:%M")) + " - " + str(hora.salida.strftime("%H:%M")) + "</p>"

            if horarios.martes:
                horario_martes = ""
                for hora in horarios.dia.hora:
                    horario_martes += "<p>" + str(hora.entrada.strftime("%H:%M")) + " - " + str(hora.salida.strftime("%H:%M")) + "</p>"

            if horarios.miercoles:
                horario_miercoles = ""
                for hora in horarios.dia.hora:
                    horario_miercoles += "<p>" + str(hora.entrada.strftime("%H:%M")) + " - " + str(hora.salida.strftime("%H:%M")) + "</p>"

            if horarios.jueves:
                horario_jueves = ""
                for hora in horarios.dia.hora:
                    horario_jueves += "<p>" + str(hora.entrada.strftime("%H:%M")) + " - " + str(hora.salida.strftime("%H:%M")) + "</p>"

            if horarios.viernes:
                horario_viernes = ""
                for hora in horarios.dia.hora:
                    horario_viernes += "<p>" + str(hora.entrada.strftime("%H:%M")) + " - " + str(hora.salida.strftime("%H:%M")) + "</p>"

            if horarios.sabado:
                horario_sabado = ""
                for hora in horarios.dia.hora:
                    horario_sabado += "<p>" + str(hora.entrada.strftime("%H:%M")) + " - " + str(hora.salida.strftime("%H:%M")) + "</p>"

            if horarios.domingo:
                horario_domingo = ""
                for hora in horarios.dia.hora:
                    horario_domingo += "<p>" + str(hora.entrada.strftime("%H:%M")) + " - " + str(hora.salida.strftime("%H:%M")) + "</p>"

        vectotr_horarios.append(horario_lunes)
        vectotr_horarios.append(horario_martes)
        vectotr_horarios.append(horario_miercoles)
        vectotr_horarios.append(horario_jueves)
        vectotr_horarios.append(horario_viernes)
        vectotr_horarios.append(horario_sabado)
        vectotr_horarios.append(horario_domingo)

        return vectotr_horarios
