from .managers import *
from datetime import datetime
from ...common.controllers import CrudController

import calendar
import json
import os.path
import uuid


class MenuController(CrudController):
    manager = MenuManager
    html_index = "comensales/menu/views/index.html"
    html_table = "comensales/menu/views/table.html"
    routes = {
        '/menu': {'GET': 'index', 'POST': 'table'},
        '/menu_insert': {'POST': 'insert'},
        '/menu_update': {'PUT': 'edit', 'POST': 'update'},
        '/menu_delete': {'POST': 'delete'},
        '/menu_dia': {'POST': 'menu_dia'},
        '/menu_plato_insert': {'POST': 'insert_plato'},
        '/menu_plato_update': {'PUT': 'edit_plato', 'POST': 'update_plato'},
        '/menu_plato_delete': {'POST': 'delete_plato'},
        '/menu_plato_estado': {'POST': 'estado_plato'},
        '/menu_plato_obtener': {'PUT': 'obtener_plato'},
        '/menu_hora': {'POST': 'update_hora'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        diaa = " "
        hoy = datetime.now().strftime('%d/%m/%Y')
        dia = calendar.day_name[datetime.now().weekday()]

        if dia == "Monday":
            diaa = "Lunes"
        elif dia == "Tuesday":
            diaa = "Martes"
        elif dia == "Wednesday":
            diaa = "Miercoles"
        elif dia == "Thursday":
            diaa = "Jueves"
        elif dia == "Friday":
            diaa ="Viernes"
        elif dia == "Saturday":
            diaa = "Sabado"
        elif dia == "Sunday":
            diaa = "Domingo"

        aux['platos'] = MenuManager(self.db).listar_todo_plato()
        aux['platos_habilitados'] = MenuManager(self.db).listar_platos_habilitados()
        aux['menus'] = MenuManager(self.db).listar_todo()
        aux['horarios'] = MenuManager(self.db).obtener_horarios()
        aux['hoy'] = hoy
        aux['dia'] = diaa

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/menu/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto'] = "/resources/images/menu/" + cname

        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        diccionary['nombre'] = "Almuerzo"
        diccionary['id'] = None
        objeto = self.manager(self.db).entity(**diccionary)
        repetido = MenuManager(self.db).insert(objeto)

        if repetido:
            self.respond(message='Insertado correctamente.', success=True)
        else:
            self.respond(message='Ya se Ingreso Menu para este Dia', success=False)

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            fname = fileinfo.filename
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            f = open("server/common/resources/images/menu/" + cname, 'wb')
            f.write(fileinfo.body)
            f.close()
            diccionary['foto'] = "/resources/images/menu/" + cname

        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        MenuManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        MenuManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip)

        self.respond(success=True, message="Menu Eliminado")
        self.db.close()

    def menu_dia(self):
        self.set_session()
        ins_manager = MenuManager(self.db)
        hoy = datetime.now().strftime('%d/%m/%Y')

        indicted_object = ins_manager.menu_dia(hoy)
        if len(ins_manager.errors) == 0 and indicted_object:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def insert_plato(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        diccionary['id'] = None
        MenuManager(self.db).insert_plato(diccionary)

        self.respond(success=True, message='Insertado correctamente.')

    def update_plato(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        MenuManager(self.db).update_plato(diccionary)
        self.respond(success=True, message='Modificado correctamente.')

    def edit_plato(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtener_plato(diccionary['id'])
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def delete_plato(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        MenuManager(self.db).delete_plato(id, self.get_user_id(), self.request.remote_ip)

        self.respond(success=True, message="Plato dado de Baja")
        self.db.close()

    def estado_plato(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        MenuManager(self.db).estado_plato(id, self.get_user_id(), self.request.remote_ip,state)
        if state:
            message = "Plato Habilitado!"
        else:
            message = "Plato deshabilitado!"

        self.respond(success=True, message=message)
        self.db.close()

    def obtener_plato(self):
        self.set_session()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        arraT = ins_manager.get_page(1, 10, None, None, True)
        arraT['datos'] = ins_manager.obtener_platos_menu(diccionary['id'])
        self.respond([objeto_regreso.get_dict() for objeto_regreso in arraT['datos']])
        self.db.close()

    def update_hora(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).obtener_horarios()
        objeto.horaLimite = datetime.strptime('01/01/2000 '+diccionary['horaLimite'], '%d/%m/%Y %H:%M')
        objeto.horaInicio = datetime.strptime('01/01/2000 ' + diccionary['horaInicio'], '%d/%m/%Y %H:%M')
        objeto.horaFin = datetime.strptime('01/01/2000 ' + diccionary['horaFin'], '%d/%m/%Y %H:%M')
        MenuManager(self.db).update_horarios(objeto,diccionary['user'],diccionary['ip'])
        self.respond(success=True, message='Modificado correctamente.')

