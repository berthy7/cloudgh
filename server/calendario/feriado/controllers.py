from .managers import *
from datetime import datetime
from ...common.controllers import CrudController
from ...configuraciones.pais.managers import *
from ...configuraciones.departamento.managers import *
from ...configuraciones.ciudad.managers import *
from ...configuraciones.sucursal.managers import *

import calendar
import json
import os.path
import uuid


class FeriadoController(CrudController):
    manager = FeriadoManager
    html_index = "calendario/feriado/views/index.html"
    html_table = "calendario/feriado/views/table.html"
    routes = {
        '/feriado': {'GET': 'index', 'POST': 'table'},
        '/feriado_insert': {'POST': 'insert'},
        '/feriado_update': {'PUT': 'edit', 'POST': 'update'},
        '/feriado_delete': {'POST': 'delete'},
        '/feriado_delete_tabla': {'POST': 'delete_tabla'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        hoy = datetime.now().strftime('%d/%m/%Y')

        aux['feriados'] = FeriadoManager(self.db).listar_todo()
        aux['paises'] = PaisManager(self.db).listar_todo()
        aux['departamentos'] = DepartamentoManager(self.db).listar_todo()
        aux['ciudades'] = CiudadManager(self.db).listar_todo()
        aux['sucursales'] = SucursalManager(self.db).listar_todo()
        aux['hoy'] = hoy

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        feriado = FeriadoManager(self.db).insert(objeto)
        FeriadoManager(self.db).actualizar_feriado(feriado)
        self.respond(message='Insertado correctamente.', success=True)


    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/feriado/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto'] = "/resources/images/feriado/" + cname

        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        FeriadoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        FeriadoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip)

        self.respond(success=True, message="Feriado Eliminado")
        self.db.close()

    def delete_tabla(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        FeriadoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip)

        self.respond(success=True, message="Feriado Eliminado")
        self.db.close()
