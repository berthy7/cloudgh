from tornado.gen import coroutine
from .managers import *
from ...common.controllers import CrudController, SuperController, ApiController
from ...personal.persona.managers import *
from ...notificaciones.correo.managers import *
from ..rol.managers import *
from ..login.managers import *

import os.path
import uuid
import json

from server.database.connection import transaction


class UsuarioController(CrudController):
    manager = UsuarioManager
    html_index = "usuarios/usuario/views/index.html"
    html_table = "usuarios/usuario/views/table.html"
    routes = {
        '/usuario': {'GET': 'index', 'POST': 'table'},
        '/usuario_insert': {'POST': 'insert'},
        '/usuario_update': {'PUT': 'edit', 'POST': 'update'},
        '/usuario_delete': {'POST': 'delete_user'},
        '/usuario_activate': {'POST': 'activate_user'},
        '/usuario_actualizar_autenticacion': {'POST': 'usuario_actualizar_autenticacion'},
        '/usuario_profile': {'GET': 'usuario_profile'},
        '/usuario_update_profile': {'POST': 'user_update_profile'},
        '/usuario_update_password': {'POST': 'user_update_password'},
        '/usuario_reset_password': {'POST': 'usuario_reset_password'},
        '/usuario_codigo_reset': {'POST': 'usuario_codigo_reset'},
        '/usuario_registrar': {'POST': 'usuario_registrar'},
        '/usuario_autenticacion': {'PUT': 'usuario_autenticacion'},
        '/usuario_validacion_token': {'PUT': 'usuario_validacion_token'},
        '/usuario_notificacion_token_email': {'PUT': 'usuario_notificacion_token_email'},
        '/usuario_notificacion_token_sms': {'PUT': 'usuario_notificacion_token_sms'},
        '/usuario_notificacion_token_ambosl': {'PUT': 'usuario_notificacion_token_ambosl'},
        '/usuario_reporte_xls': {'POST': 'reportexls'},
        '/usuario_importar': {'POST': 'importar'},
        '/usuario_modificar_password': {'POST': 'modificar_password'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['roles'] = RolManager(self.db).get_all()
        aux['personal'] = PersonaManager(self.db).listar_todo()
        aux['admin'] = PersonaManager(self.db).get_employees_tree()
        return aux

    def importar(self):
        self.set_session()
        fileinfo = self.request.files['archivo'][0]
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open("server/common/resources/uploads/" + cname, 'wb')
        fh.write(fileinfo['body'])
        fh.close()
        if extn in ['.xlsx', '.xls']:
            mee = self.manager(self.db).importar_excel(cname,self.get_user_id(),self.request.remote_ip)
            self.respond(message=mee['message'], success=mee['success'])
        else:
            if extn == '.txt':
                mee = self.manager(self.db).importar_txt(cname)
                self.respond(message=mee['message'], success=mee['success'])
            else:
                self.respond(message='Formato de Archivo no aceptado¡¡', success=False)
        self.db.close()

    def reportexls(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        cname = self.manager(self.db).usuario_excel()
        self.respond({'nombre': cname, 'url': 'resources/downloads/' + cname}, True)
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user_id'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        print(diccionary)
        objeto = self.manager(self.db).entity(**diccionary)
        respuesta = UsuarioManager(self.db).insert(objeto)
        if respuesta['respuesta']:
            self.respond(message=respuesta['Mensaje'],success=True)
        else:
            self.respond(message=respuesta['Mensaje'],success=False)

    def usuario_registrar(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        UsuarioManager(self.db).registrar_usuarios(diccionary)
        self.respond(success=True, message='Registrados correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user_id'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        UsuarioManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')



    def modificar_password(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        new_pass = diccionary['new_pass']
        UsuarioManager(self.db).modificar_contraseña(id, new_pass, self.get_user_id(), self.request.remote_ip)

        self.respond(success=True, message='Usuario cambio de contraseña.')


    def delete_user(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        enable = diccionary['enabled']
        resp = UsuarioManager(self.db).delete_user(id, enable, self.get_user_id(), self.request.remote_ip)

        if resp:
            if enable == True:
                msg = 'Usuario activado correctamente.'
            else:
                msg = 'Usuario eliminado correctamente.'
            self.respond(success=True, message=msg)
        else:
            msg = 'Rol asignado dado de baja, no es posible habilitar el usuario.'
            self.respond(success=False, message=msg)

    def activate_user(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        UsuarioManager(self.db).activate_users(id, self.get_user_id(), self.request.remote_ip)
        self.respond(success=True, message='Usuario activado correctamente.')

    def usuario_profile(self):
        user = self.get_user()
        self.set_session()
        usuario = UsuarioManager(self.db)
        result = usuario.obtener_diccionario_usuario(self.get_user_id())
        empresa = EmpresaManager(self.db).obtener_empresa()
        self.render("usuarios/usuario/views/profile.html", user=user, empresalogo=empresa, **result)
        self.db.close()

    def usuario_autenticacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        username = diccionary['username']
        password = diccionary['password']

        # user = LoginManager().login(username, password)
        password = hashlib.sha512(password.encode()).hexdigest()
        user = self.db.query(Usuario).filter(Usuario.username == username).filter(Usuario.password == password).first()

        if user:

            if user.autenticacion:
                user.token = random.randrange(99999)
                with transaction() as session:
                    session.merge(user)
                    session.commit()

            respuesta = dict(respuesta=True,autenticacion=user.autenticacion,token=user.token)
        else:
            respuesta = dict(respuesta=False, estado=True)

        self.respond(respuesta)
        self.db.close()

    def usuario_validacion_token(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        username = diccionary['username']
        password = diccionary['password']
        token = diccionary['token']

        user = LoginManager().login_token(username, password,token)

        if user:

            respuesta = dict(respuesta=True, autenticacion=user.autenticacion, token=user.token)
        else:
            respuesta = dict(respuesta=False)

        self.respond(respuesta)
        self.db.close()

    def usuario_notificacion_token_email(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        username = diccionary['username']
        password = diccionary['password']
        try:

            password = hashlib.sha512(password.encode()).hexdigest()
            user = self.db.query(Usuario).filter(Usuario.username == username).filter(Usuario.password == password).first()
            with transaction() as db:
                    CorreoManager(db).notificar_token_email(user)

            respuesta = dict(respuesta=True, mensaje="correo enviado")

            self.respond(respuesta)
            self.db.close()
        except Exception as e:
            print(e)
            respuesta = dict(respuesta=False, mensaje=str(e))

            self.respond(respuesta)
            self.db.close()

    def usuario_notificacion_token_sms(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        username = diccionary['username']
        password = diccionary['password']
        try:

            password = hashlib.sha512(password.encode()).hexdigest()
            user = self.db.query(Usuario).filter(Usuario.username == username).filter(Usuario.password == password).first()
            with transaction() as db:
                    SmsManager(db).notificar_token_sms(user)

            respuesta = dict(respuesta=True, mensaje="sms enviado")

            self.respond(respuesta)
            self.db.close()
        except Exception as e:
            print(e)
            respuesta = dict(respuesta=False, mensaje=str(e))

            self.respond(respuesta)
            self.db.close()

    def user_update_password(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        user = self.manager(self.db).get_by_password(self.get_user_id(), diccionary['old_password'])
        if user:
            if diccionary['new_password'] == diccionary['new_password_2']:
                user.password = diccionary['new_password']
                self.manager(self.db).update_password(user)
                self.respond(message="Contraseña cambiada correctamente ", success=True)
            else:
                self.respond(message="Datos incorrectos", success=False)
        else:
            self.respond(message="Datos incorrectos", success=False)
        self.db.close()

    def user_reset_password(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        user = self.manager(self.db).get_by_pass(self.get_user_id())
        if user:
            if diccionary['new_password'] == diccionary['new_password_2']:
                user.password = diccionary['new_password']
                self.manager(self.db).update_password(user)
                self.respond(message="Contraseña cambiada correctamente ", success=True)
            else:
                self.respond(message="Datos incorrectos", success=False)
        else:
            self.respond(message="Datos incorrectos", success=False)
        self.db.close()

    def user_update_profile(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        user = self.manager(self.db).update_profile(objeto, diccionary['ip'])
        self.respond(message="Datos Correctos", success=True)
        self.db.close()

    def usuario_codigo_reset(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        self.manager(self.db).update_codigo(id)
        self.respond(success=True, message='Modificado Correctamente!')

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))

    def usuario_actualizar_autenticacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        estado = diccionary['estado']
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = UsuarioManager(self.db).actualizar_autenticacion(id, estado, user, ip)
        self.respond(success=True, message='Actualizado Correctamente.')

class ApiUserController(ApiController):
    routes = {
        '/api/v1/login_usuario_mobile': {'POST': 'login_usuario_mobile'},
        '/api/v1/update_token_usuario': {'POST': 'update_token_usuario'},
        '/api/v1/listar_usuarios_privilegios': {'POST': 'listar_usuarios_privilegios'},
        '/api/v1/update_movil_privilegio': {'POST': 'update_movil_privilegio'},
    }

    def check_xsrf_cookie(self):
        return


class ManualController(SuperController):

    @coroutine
    def get(self):
        usuario = self.get_user()
        with transaction() as db:
            empresa = EmpresaManager(db).obtener_empresa()
            self.render("usuarios/usuario/views/manual.html", empresalogo=empresa, user=usuario)

class AutenticacionController(SuperController):

    @coroutine
    def get(self):
        username = "admin"
        password = "admin"
        usuario = LoginManager().login(username, password)
        # usuario = self.get_user()
        with transaction() as db:
            empresa = EmpresaManager(db).obtener_empresa()
            self.render("main/index.html", empresalogo=empresa, user=usuario)
