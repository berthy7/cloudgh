from .managers import *
from ...common.controllers import CrudController
from ...personal.persona.managers import *
from ...asistencia.asistenciapersonal.managers import *

import json
import os
import uuid


class AutorizacionextraController(CrudController):

    manager = AutorizacionextraManager
    html_index = "asistencia/autorizacionextra/views/index.html"
    html_table = "asistencia/autorizacionextra/views/table.html"
    routes = {
        '/autorizacion_extra': {'GET': 'index', 'POST': 'table'},
        '/autorizacion_extra_insert': {'POST': 'insert'},
        '/autorizacion_extra_update': {'PUT': 'edit', 'POST': 'update'},
        '/autorizacion_extra_delete': {'POST': 'delete'},
        '/autorizacion_extra_filtrar': {'POST': 'filtrar'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['personal'] = PersonaManager(self.db).listar_todo()
        aux['horarios'] = AutorizacionextraManager(self.db).listar_por_dia()
        aux['admin'] = PersonaManager(self.db).get_employees_tree()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        ins_manager = self.manager(self.db)
        c = 0
        list = {}
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        if diccionary['autorizado'] == "":
            diccionary['horaextra'] = diccionary['extra']
        else:
            diccionary['horaextra'] = diccionary['autorizado']

        objeto = self.manager(self.db).entity(**diccionary)
        AutorizacionextraManager(self.db).insert(objeto)
        # self.respond(success=True, message='Insertado correctamente.')

        if diccionary['filtro'] == "si":

            diccionario = dict(lista=list, contador=c)
            fechainicio = diccionary['fechainicio']
            fechafin = diccionary['fechafin']

            for per in diccionary['personas']:
               diccionario = ins_manager.filtrar(diccionario,fechainicio, fechafin,per['id_persona'])

            for per in diccionary['personas_arbol']:
                diccionario = ins_manager.filtrar(diccionario,fechainicio, fechafin,per['id_persona'])

            if len(ins_manager.errors) == 0:
                self.respond(diccionario['lista'], message='Operacion exitosa!')
            else:
                self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
            self.db.close()
        else:

            a = ins_manager.listar_por_dia_autorizar()
            self.respond(a, message='Operacion exitosa!')
            self.db.close()


    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        ins_manager = self.manager(self.db)
        list = {}
        c = 0

        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        if diccionary['autorizado'] == "":
            diccionary['horaextra'] = diccionary['extra']
        else:
            diccionary['horaextra'] = diccionary['autorizado']

        objeto = self.manager(self.db).entity(**diccionary)
        AutorizacionextraManager(self.db).update(objeto)
        # self.respond(success=True, message='Insertado correctamente.')

        if diccionary['filtro'] == "si":

            diccionario = dict(lista=list, contador=c)
            fechainicio = diccionary['fechainicio']
            fechafin = diccionary['fechafin']

            for per in diccionary['personas']:
               diccionario = ins_manager.filtrar(diccionario,fechainicio, fechafin,per['id_persona'])

            for per in diccionary['personas_arbol']:
                diccionario = ins_manager.filtrar(diccionario,fechainicio, fechafin,per['id_persona'])

            if len(ins_manager.errors) == 0:
                self.respond(diccionario['lista'], message='Operacion exitosa!')
            else:
                self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
            self.db.close()
        else:

            a = AutorizacionextraManager(self.db).listar_por_dia_autorizar()
            self.respond(a, message='Operacion exitosa!')
            self.db.close()


    def filtrar(self):
        self.set_session()
        data = json.loads(self.get_argument("object"))
        ins_manager = self.manager(self.db)
        list = {}
        c = 0

        diccionario = dict(lista=list, contador=c)
        #fechainicio = data['fechainicio']
        #fechafin = data['fechafin']

        fechainicio = datetime.strptime(data['fechainicio'], '%d/%m/%Y')
        fechafin = datetime.strptime(data['fechafin'], '%d/%m/%Y')

        repetidos = set(data['personas_arbol']).intersection(data['personas'])

        for rep in repetidos:
            data['personas'].remove(rep)

        for per in data['personas']:
            data['personas_arbol'].append(per)

        personas_lista = set(data['personas_arbol'])

        for per in personas_lista:
            persona_horario = self.db.query(Asignacion).filter(Asignacion.fkpersona == per).first()

            if persona_horario:
                diccionario = ins_manager.filtrar(diccionario,fechainicio, fechafin,per)

        if len(ins_manager.errors) == 0:
            self.respond(diccionario['lista'], message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def edit(self):
        self.set_session()
        self.verif_privileges()
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = AsistenciaManager(self.db).obtener_asistencia(diccionary['id'])
        self.respond(indicted_object.get_dict(), message='Operacion exitosa!')

        self.db.close()

    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        ins_manager = self.manager(self.db)
        list = {}
        c = 0

        id = diccionary['id']
        fkasistencia = diccionary['fkasistencia']
        user = self.get_user_id()
        ip = self.request.remote_ip

        AutorizacionextraManager(self.db).delete(id,fkasistencia, user, ip)
        # self.respond(success=True, message='Insertado correctamente.')

        if diccionary['filtro'] == "si":

            diccionario = dict(lista=list, contador=c)
            fechainicio = diccionary['fechainicio']
            fechafin = diccionary['fechafin']

            for per in diccionary['personas']:
               diccionario = ins_manager.filtrar(diccionario,fechainicio, fechafin,per['id_persona'])

            for per in diccionary['personas_arbol']:
                diccionario = ins_manager.filtrar(diccionario,fechainicio, fechafin,per['id_persona'])

            if len(ins_manager.errors) == 0:
                self.respond(diccionario['lista'], message='Operacion exitosa!')
            else:
                self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
            self.db.close()
        else:

            a = AutorizacionextraManager(self.db).listar_por_dia_autorizar()
            self.respond(a, message='Operacion exitosa!')
            self.db.close()
