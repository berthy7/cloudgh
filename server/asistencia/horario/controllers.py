from .managers import *
from ...common.controllers import CrudController
from ..turno.managers import *


import os.path
import uuid
import json


class HorarioController(CrudController):

    manager = SemanalManager
    html_index = "asistencia/horario/views/index.html"
    html_table = "asistencia/horario/views/table.html"
    routes = {
        '/horario': {'GET': 'index', 'POST': 'table'},
        '/horario_insert': {'POST': 'insert'},
        '/horario_update': {'PUT': 'edit', 'POST': 'update'},
        '/horario_delete': {'POST': 'delete'},
        '/horario_reporte_xls': {'POST': 'reportexls'},
        '/horario_importar': {'POST': 'importar'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['dias'] = DiaManager(self.db).litar_todo()
        aux['tabla_semanal'] = SemanalManager(self.db).tabla_semanal()

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

        cname = self.manager(self.db).horario_excel()
        self.respond({'nombre': cname, 'url': 'resources/downloads/' + cname}, True)
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        diccionary['id'] = None
        objeto = self.manager(self.db).entity(**diccionary)
        SemanalManager(self.db).insert(objeto)

        self.respond(success=True, message='Insertado correctamente.')


    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = SemanalManager(self.db).eliminar(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')
