from ...personal.persona.managers import *
from ...comensales.menu.managers import *
from ...comensales.pedido.managers import *
from ...common.controllers import CrudController

from .managers import *
from datetime import datetime

import json


class PortalPedidoController(CrudController):
    manager = PortalPedidoManager
    html_index = "portal/pedido/views/index.html"
    html_table = "portal/pedido/views/table.html"
    routes = {
        '/portal_pedido': {'GET': 'index', 'POST': 'table'},
        '/portal_pedido_insert': {'PUT': 'add','POST': 'insert'},
        '/portal_pedido_update': {'PUT': 'edit', 'POST': 'update'},
        '/portal_pedido_delete': {'POST': 'delete'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        hoy = datetime.now().strftime('%d/%m/%Y')
        us = self.get_user()
        idpersona = us.fkpersona

        if idpersona:
            aux['idpersona'] = idpersona

        else:
            aux['idpersona'] = 0

        aux['pedidos_persona'] = PortalPedidoManager(self.db).listar_x_persona(idpersona)
        aux['pedidos_dia'] = PedidoManager(self.db).pedido_dia(hoy)
        aux['platos'] = MenuManager(self.db).listar_plato_dia(hoy)
        aux['personas'] = PersonaManager(self.db).listar_todo()
        aux['horarios'] = MenuManager(self.db).obtener_horarios()

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
        horarios = MenuManager(self.db).obtener_horarios()

        if diccionary['fecha'].strftime("%H:%M")<= horarios.horaLimite.strftime("%H:%M"):


            for i in diccionary['pedidos']:
                diccionary['sopa'] = i['sopa']
                diccionary['fkplato'] = i['fkplato']
                diccionary['fkpersona'] = i['fkpersona']

                if diccionary['fkplato'] == "0":
                    diccionary['fkplato'] = None

                objeto = self.manager(self.db).entity(**diccionary)
                PedidoManager(self.db).insert(objeto)

            self.respond(success=True, message='Insertado correctamente.')

        else:
            self.respond(success=False, message='Pedido Excedio la hora limite.')

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
