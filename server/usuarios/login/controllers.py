from tornado.gen import coroutine
from .managers import *
from ...common.controllers import SuperController
from ...operaciones.bitacora.models import *
from ...configuraciones.empresa.managers import *
import json


class LoginController(SuperController):

    @coroutine
    def get(self):
        """Renderiza el login"""
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')
        usuario = self.get_secure_cookie("user")
        if usuario:
            self.redirect("/")
        else:
            self.clear_cookie("user")
            with transaction() as db:
                empresa = EmpresaManager(db).obtener_empresa()
            self.render("usuarios/login/views/index.html",empresalogo=empresa, error=0)

    @coroutine
    def post(self):
        """Inicia sesión en la aplicación.

        Si se inicia sesión con éxito enctonces se guarda el
        usuario en la cookie caso contrario se vuelve al login.
        """
        self.check_xsrf_cookie()
        ip = self.request.remote_ip
        diccionary = json.loads(self.get_argument("object"))
        username = diccionary['username']
        password = diccionary['password']
        # username = self.get_argument('username', default=None)
        # password = self.get_argument('password', default=None)

        with transaction() as db:
            empresa = EmpresaManager(db).obtener_empresa()

        if username is not None and password is not None:
            user = LoginManager().login(username, password)
            if user:
                fecha = self.fecha_actual()
                b = Bitacora(fkusuario=user.id, ip=ip, accion="Inicio de sesión.", fecha=fecha)
                # self.insertar_bitacora(b)
                self.set_user_id(user.id)
                self.redirect("/")
            else:
                userb = LoginManager().not_enabled(username, password)
                if userb:
                    self.render("usuarios/login/views/index.html",empresalogo=empresa, error=1)
                else:
                    self.render("usuarios/login/views/index.html",empresalogo=empresa, error=2)
        else:
            self.render("usuarios/login/views/index.html",empresalogo=empresa, error=2)

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))

    def insertar_bitacora(self, bitacora):
        with transaction() as session:
            session.add(bitacora)
            session.commit()


class LogoutController(SuperController):

    @coroutine
    def get(self):
        try:
            user_id = self.get_user_id()
            ip = self.request.remote_ip
            fecha = self.fecha_actual()
            b = Bitacora(fkusuario=user_id, ip=ip, accion="Finalizó sesión.", fecha=fecha)
            self.insertar_bitacora(b)
            self.clear_cookie('user')
            self.redirect(self.get_argument("next", "/"))
        except Exception as e:
            self.clear_cookie('user')
            self.redirect(self.get_argument("next", "/"))

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))

    def insertar_bitacora(self, bitacora):
        with transaction() as session:
            session.add(bitacora)
            session.commit()


class ApiLoginController(SuperController):

    @coroutine
    def post(self):
        """Devuelve el usuario que coincida con el username y password dados.

        Si ocurre algún error se retornará None en la respuesta json al
        cliente invocador.
        """
        try:
            username = self.get_argument('username')
            password = self.get_argument('password')
            usuario = LoginManager().login(username, password)
            self.respond(usuario.getDict())
        except:
            self.respond(success=False)
