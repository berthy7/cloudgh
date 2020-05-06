from .managers import *
from ...control.tarea.managers import *
from ...common.controllers import CrudController
from ...asistencia.asistenciapersonal.managers import *
from ...personal.persona.managers import *
from ...control.proyecto.managers import *

import json


class TareaController(CrudController):

    manager = TareaManager
    html_index = "control/tarea/views/index.html"
    html_table = "control/tarea/views/table.html"
    routes = {
        '/tarea': {'GET': 'index', 'POST': 'table'},
        '/tarea_insert': {'POST': 'insert'},
        '/tarea_update': {'PUT': 'edit', 'POST': 'update'},
        '/tarea_delete': {'POST': 'delete'},
        '/tarea_create': {'POST': 'create'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['proyectos'] = ProyectoManager(self.db).get_all()
        aux['personas'] = PersonaManager(self.db).listar_todo()

        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip

        try:
            i = 0
            while i < len(diccionary['datos']):
                id = int(diccionary['datos'][i]['id'])
                descripcion = diccionary['datos'][i]['descripcion']
                prioridad = diccionary['datos'][i]['prioridad']
                estimacion = int(diccionary['datos'][i]['estimacion'])
                FechaInicio = diccionary['datos'][i]['fechaInicio']
                fechaFin = diccionary['datos'][i]['fechaFin']
                fktarea = diccionary['id']
                fkproyecto = int(diccionary['datos'][i]['fkproyecto'])
                estado = diccionary['datos'][i]['estado']

                if id == 0:
                    TareaManager(self.db).insert_task(descripcion, prioridad, estimacion, FechaInicio, fechaFin, fktarea, fkproyecto, estado)
                else:
                    TareaManager(self.db).update_task(id, descripcion, prioridad, estimacion, FechaInicio, fechaFin, fktarea, fkproyecto, estado)
                i = i + 1

            for task_id in diccionary['remove_task']:
                TareaManager(self.db).delete_task(task_id, diccionary['ip'], diccionary['user'])

            self.respond(success=True, message='Insertado correctamente.')
        except Exception as e:
            print(e)
            self.respond(success=False, message='ERROR 403')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        TareaManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        arraT = ins_manager.get_page(1, 10, None, None, True)
        arraT['datos'] = ins_manager.obtener_tareas(diccionary['id'])
        self.respond([objeto_regreso.get_dict() for objeto_regreso in arraT['datos']])
        self.db.close()

    def create(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        AsistenciaManager(self.db).insert_by_range(diccionary['user'], diccionary['ip'], diccionary['fechaini'], diccionary['fechafin'], diccionary['fkpersona'])

        self.respond(success=True, message='Insertado correctamente.')
