from ...personal.persona.managers import *
from ...comensales.menu.managers import *
from ...common.controllers import CrudController

from .managers import *
from datetime import datetime

import json


class PedidoController(CrudController):
    manager = PedidoManager
    html_index = "comensales/pedido/views/index.html"
    html_table = "comensales/pedido/views/table.html"
    routes = {
        '/pedido': {'GET': 'index', 'POST': 'table'},
        '/pedido_insert': {'PUT': 'add','POST': 'insert'},
        '/pedido_update': {'PUT': 'edit', 'POST': 'update'},
        '/pedido_delete': {'POST': 'delete'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        hoy = datetime.now().strftime('%d/%m/%Y')
        aux['pedidos_dia'] = PedidoManager(self.db).pedido_dia(hoy)
        aux['platos'] = MenuManager(self.db).listar_plato_dia(hoy)
        aux['personas'] = PersonaManager(self.db).listar_todo()

        return aux

    def add(self):
        self.set_session()
        ins_manager = MenuManager(self.db)
        hoy = datetime.now().strftime('%d/%m/%Y')

        indicted_object = ins_manager.menu_dia(hoy)
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        hoy = datetime.now(pytz.timezone('America/La_Paz'))
        diccionary['fecha'] = hoy

        for i in diccionary['pedidos']:
            diccionary['sopa'] = i['sopa']
            diccionary['fkplato'] = i['fkplato']
            diccionary['fkpersona'] = i['fkpersona']

            if diccionary['fkplato'] == "0":
                diccionary['fkplato'] = None

            objeto = self.manager(self.db).entity(**diccionary)
            PedidoManager(self.db).insert(objeto)

        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip

        hoy = datetime.now(pytz.timezone('America/La_Paz'))
        diccionary['fecha'] = hoy
        for i in diccionary['pedidos']:
            try:
                diccionary['sopa'] = i['sopa']
                diccionary['fkplato'] = i['fkplato']
                diccionary['fkpersona'] = i['fkpersona']
                diccionary['id'] = i['id']

                objeto = self.manager(self.db).entity(**diccionary)
                PedidoManager(self.db).update(objeto)
            except Exception as e:
                diccionary['id'] = None
                objeto = self.manager(self.db).entity(**diccionary)
                PedidoManager(self.db).insert(objeto)

        self.respond(success=True, message='Modificado correctamente.')
