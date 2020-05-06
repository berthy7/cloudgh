from server.common.managers import SuperManager
from .models import *


class SemanalManager(SuperManager):

    def __init__(self, db):
        super().__init__(Semanal, db)

    def tabla_semanal(self):
        list = {}
        c = 0
        objeto = self.db.query(self.entity).all()

        for x in objeto:
            list_libre = {}
            list_libre[0]= dict(hora="Libre")
            lunes = list_libre
            martes = list_libre
            miercoles = list_libre
            jueves = list_libre
            viernes = list_libre
            sabado = list_libre
            domingo = list_libre
            for detalle in x.semanaldetalle:
                list_hora = {}
                ch = 0
                for horario in detalle.dia.hora:
                    aux = horario.entrada.strftime("%H:%M") + " - " + horario.salida.strftime("%H:%M")

                    list_hora[ch]= dict(hora=aux)
                    ch = ch + 1

                if detalle.lunes:
                    lunes= list_hora
                if detalle.martes:
                    martes=list_hora
                if detalle.miercoles:
                    miercoles=list_hora
                if detalle.jueves:
                    jueves=list_hora
                if detalle.viernes:
                    viernes=list_hora
                if detalle.sabado:
                    sabado=list_hora
                if detalle.domingo:
                    domingo=list_hora

            list[c] = dict(id=x.id, nombre=x.nombre,lunes=lunes,martes=martes,miercoles=miercoles,jueves=jueves,viernes=viernes,sabado=sabado,domingo=domingo)
            c = c + 1

        return list

    def listar_todo(self):
        return self.db.query(self.entity)
