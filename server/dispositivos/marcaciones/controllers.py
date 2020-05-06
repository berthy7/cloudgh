from .managers import *
from ...dispositivos.lectores.managers import *
from ...configuraciones.sucursal.managers import *
from ...common.controllers import CrudController

import json
import os.path
import uuid
import json


class MarcacionesController(CrudController):

    manager = MarcacionesManager
    html_index = "dispositivos/marcaciones/views/index.html"
    html_table = "dispositivos/marcaciones/views/table.html"
    routes = {
        '/marcaciones': {'GET': 'index', 'POST': 'table'},
        '/marcaciones_insert': {'POST': 'insert'},
        '/marcaciones_update': {'PUT': 'edit', 'POST': 'update'},
        '/marcaciones_delete': {'POST': 'delete'},
        '/marcaciones_extraer': {'POST': 'extraer'},
        '/marcaciones_filtrar': {'POST': 'filtrar'},
        '/marcaciones_importar': {'POST': 'importar'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['sucursales'] = SucursalManager(self.db).listar_todo()
        aux['marcaciones'] = MarcacionesManager(self.db).listar_por_dia()

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
            mee = self.manager(self.db).importar_excel(cname)
            self.respond(message=mee['message'], success=mee['success'])
        else:
            if extn == '.txt':
                mee = self.manager(self.db).importar_txt(cname)
                self.respond(message=mee['message'], success=mee['success'])
            else:
                self.respond(message='Formato de Archivo no aceptado¡¡', success=False)
        self.db.close()

    def extraer(self):
        self.set_session()
        LectoresManager(self.db).preparar_dispositivos()
        self.respond(success=True, message='Insertado correctamente.')

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip_maquina'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        MarcacionesManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        MarcacionesManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def filtrar(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        fechainicio = data['fechainicio']
        fechafin = data['fechafin']
        fechainicio = datetime.strptime(fechainicio, '%d/%m/%Y')
        fechafin = datetime.strptime(fechafin, '%d/%m/%Y')
        ins_manager = self.manager(self.db)
        indicted_object = ins_manager.filtrar(fechainicio, fechafin)
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object, message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()
