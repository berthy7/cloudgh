from tornado.gen import coroutine

from server.usuarios.usuario.managers import *
from server.dispositivos.lectores.managers import *
from server.dispositivos.marcaciones.managers import *


from server.usuarios.login.managers import *
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from server.common.controllers import CrudController, SuperController, ApiController
import os.path
import json
import ast


class ApiCloudghController(ApiController):
    manager = UsuarioManager
    routes = {
        '/api/v4/login_movil': {'POST': 'login_movil'},
        '/api/v4/listar_dispositivos': {'POST': 'listar_dispositivos'},
        '/api/v4/marcaciones_dispositivo': {'POST': 'marcaciones_dispositivo'},
    }


    def login_movil(self):
        self.set_session()
        data = json.loads(self.request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        ip = data['ip']
        user = LoginManager().login(username, password)

        if user:
            fecha = self.fecha_actual()
            b = Bitacora(fkusuario=user.id, ip=ip, accion="Inicio de sesión.", fecha=fecha)
            self.insertar_bitacora(b)
            users =  UsuarioManager(self.db).get_by_pass(user.id)
            usuario = users.get_dict()
            usuario['rol']['modulos'] = None

            self.respond(success=True, response=usuario, message='Usuario Logueado correctamente.')

        else:
            self.respond(success=False, response="", message='El Usuario no se pudo Loguear.')

    def listar_dispositivos(self):
        try:
            self.set_session()
            print('listar_dispositivos')
            data = json.loads(self.request.body.decode('utf-8'))
            x = ast.literal_eval(data)
            arraT = self.manager(self.db).get_page(1, 10, None, None, True)
            resp = []

            arraT['objeto'] = LectoresManager(self.db).ws_listar_dispositivos(x)
            for item in arraT['objeto']:
                obj_dict = item.get_dict()
                resp.append(obj_dict)
            self.db.close()

            self.respond(response=resp, success=True, message="dispositivos recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=0, success=False, message=str(e))
        self.db.close()

    def marcaciones_dispositivo(self):
        self.set_session()
        data = json.loads(self.request.body.decode('utf-8'))
        x = ast.literal_eval(data)
        # print("ws marcaciones dispositivo " + str(x['iddispositivo']))

        LectoresManager(self.db).ws_insertRegistros_biometricos(x)
        self.respond(success=True, message='Insertado correctamente.')

    # Funciones de Bitacora
    def insertar_bitacora(self, bitacora):
        with transaction() as session:
            session.add(bitacora)
            session.commit()
    def obtener_usuario(self, Usuario_id):
        with transaction() as session:
            return session.query(Usuario).filter(Usuario.id == Usuario_id).first()
    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))