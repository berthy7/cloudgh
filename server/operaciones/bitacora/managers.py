from server.common.managers import SuperManager
from .models import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pytz
import calendar

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class BitacoraManager(SuperManager):

    def __init__(self, db):
        super().__init__(Bitacora, db)

    def list_all(self):
        return dict(objects=self.db.query(Bitacora).order_by(Bitacora.id.asc()))

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))

    def fecha(self):
        return fecha_zona.strftime('%Y/%d/%m')

    def obtener_dia(self,fecha):

        dia = calendar.day_name[fecha.weekday()]

        if dia == "Monday":
            dia = "Lu"
        elif dia == "Tuesday":
            dia = "Ma"
        elif dia == "Wednesday":
            dia = "Mi"
        elif dia == "Thursday":
            dia = "Ju"
        elif dia == "Friday":
            dia = "Vi"
        elif dia == "Saturday":
            dia = "Sa"
        elif dia == "Sunday":
            dia = "Do"

        return dia

    def rango_fechas(self,fechai, fechaf):
        rango = []
        dias_totales = (fechaf - fechai).days
        for days in range(dias_totales + 1):
            fecha = fechai + relativedelta(days=days)
            rango.append(fecha)
        return rango

    def obtener_cant_dias(self,fechai,fechaf):
        fechas = BitacoraManager(self.db).rango_fechas(fechai, fechaf)
        cont_dias = 0
        for fech in fechas:
            dia = BitacoraManager(self.db).obtener_dia(fech)
            if dia != "Sa" and dia != "Do":
                cont_dias = cont_dias + 1

        return cont_dias
