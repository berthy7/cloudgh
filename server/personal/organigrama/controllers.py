from .managers import *
from server.common.controllers import CrudController
from ..persona.managers import *

import os.path
import uuid
import json


class OrganigramaController(CrudController):

    manager = OrganigramaManager
    html_index = "personal/organigrama/views/index.html"
    routes = {
        '/organigrama': {'GET': 'index'},
        '/organigrama_insert': {'POST': 'insert'},
        '/organigrama_edit': {'POST': 'edit'},
        '/organigrama_delete': {'POST': 'delete'},
        '/organigrama_update': {'POST': 'update'},
        '/organigrama_data': {'POST': 'dataorg'},
        '/organigrama_get_brother': {'POST': 'get_brother'},
        '/organigrama_get': {'POST': 'get_entity'},
        '/organigrama_reporte_xls': {'POST': 'reportexls'},
        '/organigrama_importar': {'POST': 'importar'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        objeto = []
        aux['personas'] = PersonaManager(self.db).listar_todo()
        aux['cargos'] = CargoManager(self.db).get_all_by_name()

        aux['objeto'] = objeto

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

        cname = self.manager(self.db).organigrama_excel()
        self.respond({'nombre': cname, 'url': 'resources/downloads/' + cname}, True)
        self.db.close()

    def dataorg(self):
        self.set_session()
        result = self.manager(self.db).get_all()
        self.respond(result)
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip

        objeto = self.manager(self.db).entity(**diccionary)

        if 'id' not in diccionary:
            result = OrganigramaManager(self.db).insert(objeto)

            if result:
                self.respond(success=True, message='Insertado Correctamente.')
            else:
                self.respond(success=False, message='ERROR 403')
        else:
            result = OrganigramaManager(self.db).update(objeto)
            if result:

                self.respond(success=True, message='Modificado Correctamente.')
            else:
                self.respond(success=False, message='ERROR 403')

    def delete(self):
        self.set_session()
        self.verif_privileges()
        id = json.loads(self.get_argument("object"))['id']
        if id != 1:
            obj = self.db.query(Organigrama).get(id)
            obj.enabled = False
            obj.fkpadre =  None
            obj.siguiente = None
            self.db.commit()
            message = "Dado de Baja!"
            self.respond(obj.get_dict(), message=message)
        else:
            self.respond(dict(), message='Error no puede eliminar raiz', success=False)
        self.db.close()

    def get_brother(self):
        self.set_session()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        data = self.manager(self.db).get_brother(**diccionary)
        if len(ins_manager.errors) == 0:
            self.respond(data)
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al actualizar')
        self.db.close()

    def get_entity(self):
        self.set_session()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        object = ins_manager.obtain(diccionary['id'])
        if len(ins_manager.errors) == 0:
            self.respond(object.get_dict())
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al actualizar')
        self.db.close()

    def edit(self):
        self.set_session()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        object = ins_manager.entity(**diccionary)
        indicted_object = ins_manager.update(object)
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Actualizado correctamente!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al actualizar')
        self.db.close()

    def update(self):
        self.set_session()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        object = ins_manager.obtain(diccionary['id'])
        object.fkpadre = diccionary['parent']
        indicted_object = ins_manager.update(object)
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Actualizado correctamente!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al actualizar')
        self.db.close()
