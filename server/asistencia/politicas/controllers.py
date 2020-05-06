from ...personal.persona.managers import *
from ..asistenciapersonal.managers import *
from ..horario.managers import *
from ..asignacion.managers import *
from ...common.controllers import CrudController
from ..politicas.managers import *
from ...usuarios.usuario.managers import *


import json


class PoliticasController(CrudController):

    manager = PoliticasManager
    html_index = "asistencia/politicas/views/index.html"
    html_table = "asistencia/politicas/views/table.html"
    routes = {
        '/politicas': {'GET': 'index', 'POST': 'table'},
        '/politicas_insert': {'POST': 'insert'},
        '/politicas_update': {'PUT': 'edit', 'POST': 'update'},
        '/politicas_delete': {'POST': 'delete'},

    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['select_semanal'] = SemanalManager(self.db).listar_todo()
        aux['admin'] = PersonaManager(self.db).get_employees_tree()
        aux['horarios'] = AsistenciaManager(self.db).listar_por_dia()

        return aux

    def index(self):
        self.set_session()
        self.verif_privileges()
        self.manager(self.db).actualizar_politicas()
        result = self.manager(self.db).list_all()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result['empresalogo'] = EmpresaManager(self.db).obtener_empresa()
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PeriodoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')


