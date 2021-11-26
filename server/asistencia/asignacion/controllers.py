from .managers import *
from ...personal.persona.managers import *
from ...common.controllers import CrudController
from ..horario.managers import *

import json

import os.path
import uuid
import json

class AsignacionController(CrudController):

    manager = PeriodoManager
    html_index = "asistencia/asignacion/views/index.html"
    html_table = "asistencia/asignacion/views/table.html"
    routes = {
        '/asignacion': {'GET': 'index', 'POST': 'table'},
        '/asignacion_insert': {'POST': 'insert'},
        '/asignacion_update': {'PUT': 'edit', 'POST': 'update'},
        '/asignacion_delete': {'POST': 'delete'},
        '/asignacion_reporte_xls': {'POST': 'reportexls'},
        '/asignacion_importar': {'POST': 'importar'},

    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['select_semanal'] = SemanalManager(self.db).listar_todo()
        aux['admin'] = PersonaManager(self.db).get_employees_tree()
        aux['personal'] = PersonaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip


        repetidos = set(diccionary['personas_arbol']).intersection(diccionary['personas'])

        for rep in repetidos:
            diccionary['personas'].remove(rep)

        for per in diccionary['personas']:
            diccionary['personas_arbol'].append(per)

        personas_lista = set(diccionary['personas_arbol'])

        lista_Asignacion = list()

        for per in personas_lista:
            asignacion_persona = AsignacionManager(self.db).obtener_x_persona(per)

            if asignacion_persona == None:

                lista_Asignacion.append(dict(fkpersona=per))


        diccionary['asignacion'] = lista_Asignacion

        objeto = self.manager(self.db).entity(**diccionary)
        PeriodoManager(self.db).insert(objeto)

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PeriodoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = PeriodoManager(self.db).eliminar(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')


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

        cname = self.manager(self.db).periodo_excel()
        self.respond({'nombre': cname, 'url': 'resources/downloads/' + cname}, True)
        self.db.close()