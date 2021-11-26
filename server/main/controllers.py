from server.database.connection import transaction
from tornado.web import authenticated
from tornado.gen import coroutine
from server.common.utils import decorators
from ..common.controllers import SuperController
from threading import Thread
from datetime import datetime, timedelta, time, date
import pytz
from ..usuarios.usuario.managers import *
from ..asistencia.asistenciapersonal.managers import AsistenciaManager
from ..configuraciones.empresa.managers import *


class Index(SuperController):

    @decorators(authenticated, coroutine)
    def get(self):
        Thread(target=self.crear_horarios).start()
        try:
            usuario = self.get_user()
            if usuario:
                empresa = self.obtener_empresa()
                self.render("main/index.html", user=usuario, empresalogo=empresa)
            else:
                self.redirect('/logout')
        except Exception as e:
            print(e)
            self.redirect('/logout')

    def crear_horarios(self):
        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
        with transaction() as db:
            AsistenciaManager(db).crear_horarios(fecha_zona,fecha_zona,None)

    def obtener_empresa(self):
        with transaction() as db:
            x = EmpresaManager(db).obtener_empresa()
            return x
