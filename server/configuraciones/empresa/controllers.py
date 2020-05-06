from .managers import *
from ...common.controllers import CrudController

import json
import os
import uuid


class EmpresaController(CrudController):

    manager = EmpresaManager
    html_index = "configuraciones/empresa/views/index.html"
    html_table = "configuraciones/empresa/views/table.html"
    routes = {
        '/empresa': {'GET': 'index', 'POST': 'table'},
        '/empresa_insert': {'POST': 'insert'},
        '/empresa_update': {'PUT': 'edit', 'POST': 'update'},
        '/empresa_delete': {'POST': 'delete'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/logoempresa/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto1'] = "/resources/images/logoempresa/" + cname

        if "archivo2" in self.request.files:
            fileinfo = self.request.files["archivo2"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/logoempresa/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto2'] = "/resources/images/logoempresa/" + cname

        if "archivo3" in self.request.files:
            fileinfo = self.request.files["archivo3"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/logoempresa/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto3'] = "/resources/images/logoempresa/" + cname
        objeto = self.manager(self.db).entity(**diccionary)
        EmpresaManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/logoempresa/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto1'] = "/resources/images/logoempresa/" + cname

        if "archivo2" in self.request.files:
            fileinfo = self.request.files["archivo2"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/logoempresa/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto2'] = "/resources/images/logoempresa/" + cname

        if "archivo3" in self.request.files:
            fileinfo = self.request.files["archivo3"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/logoempresa/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto3'] = "/resources/images/logoempresa/" + cname
        objeto = self.manager(self.db).entity(**diccionary)
        EmpresaManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        estado = json.loads(self.get_argument("enabled"))
        user = self.get_user_id()
        ip = self.request.remote_ip
        result = EmpresaManager(self.db).delete(id, estado, user, ip)
        if result:
            self.respond(success=True, message='Baja Realizada Correctamente.')
        else:
            self.respond(success=False, message='ERROR 403')