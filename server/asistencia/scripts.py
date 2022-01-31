from ..usuarios.rol.models import Modulo
from ..usuarios.rol.models import Rol
from .asistenciapersonal.managers import AsistenciaManager
from .tipoausencia.models import *

from server.database.connection import transaction
from datetime import datetime

import schedule
import pytz

def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        asistencia_m = session.query(Modulo).filter(Modulo.name == 'asistencia').first()
        if asistencia_m is None:
            asistencia_m = Modulo(title='Asistencia', name='asistencia', icon='asistencia.png')

        turno_m = session.query(Modulo).filter(Modulo.name == 'turno').first()
        if turno_m is None:
            turno_m = Modulo(title='Turnos', route='/turno', name='turno', icon='turnos.png')

        horario_m = session.query(Modulo).filter(Modulo.name == 'horario').first()
        if horario_m is None:
            horario_m = Modulo(title='Horarios Semanal', route='/horario', name='horario', icon='horario.png')

        asignacion_m = session.query(Modulo).filter(Modulo.name == 'asignacion').first()
        if asignacion_m is None:
            asignacion_m = Modulo(title='Asignación Horarios', route='/asignacion', name='asignacion', icon='asignacion.png')

        autorizacion_extra_m = session.query(Modulo).filter(Modulo.name == 'autorizacion_extra').first()
        if autorizacion_extra_m is None:
            autorizacion_extra_m = Modulo(title='Autorizacion de horas Extras', route='/autorizacion_extra', name='autorizacion_extra',
                                  icon='horarioextra.png')

        tipoausencia_m = session.query(Modulo).filter(Modulo.name == 'tipoausencia').first()
        if tipoausencia_m is None:
            tipoausencia_m = Modulo(title='Tipos de Ausencias', route='/tipoausencia', name='tipoausencia', icon='tipoausencia.png')

        ausencia_m = session.query(Modulo).filter(Modulo.name == 'ausencia').first()
        if ausencia_m is None:
            ausencia_m = Modulo(title='Ausencias', route='/ausencia', name='ausencia', icon='ausencia.ico')

        politicas_m = session.query(Modulo).filter(Modulo.name == 'politicas').first()
        if politicas_m is None:
            politicas_m = Modulo(title='Politicas', route='/politicas', name='politicas', icon='configuraciones.png')

        asistenciapersonal_m = session.query(Modulo).filter(Modulo.name == 'asistenciapersonal').first()
        if asistenciapersonal_m is None:
            asistenciapersonal_m = Modulo(title='Asistencia Personal', route='/asistenciapersonal', name='asistenciapersonal', icon='asistenciapersonal.png')

        asistencia_m.children.append(turno_m)
        asistencia_m.children.append(horario_m)
        asistencia_m.children.append(asignacion_m)
        asistencia_m.children.append(autorizacion_extra_m)
        asistencia_m.children.append(politicas_m )
        asistencia_m.children.append(asistenciapersonal_m)

        query_turno = session.query(Modulo).filter(Modulo.name == 'turno_query').first()
        if query_turno is None:
            query_turno = Modulo(title='Consultar', route='',
                                 name='turno_query',
                                 menu=False)

        insert_turno = session.query(Modulo).filter(Modulo.name == 'turno_insert').first()
        if insert_turno is None:
            insert_turno = Modulo(title='Adicionar', route='/turno_insert',
                                  name='turno_insert',
                                  menu=False)
        update_turno = session.query(Modulo).filter(Modulo.name == 'turno_update').first()
        if update_turno is None:
            update_turno = Modulo(title='Actualizar', route='/turno_update',
                                  name='turno_update',
                                  menu=False)
        delete_turno = session.query(Modulo).filter(Modulo.name == 'turno_delete').first()
        if delete_turno is None:
            delete_turno = Modulo(title='Dar de Baja', route='/turno_delete',
                                  name='turno_delete',
                                  menu=False)

        imprimir_turno = session.query(Modulo).filter(Modulo.name == 'turno_imprimir').first()
        if imprimir_turno is None:
            imprimir_turno = Modulo(title='Imprimir', route='/turno_imprimir',
                                    name='turno_imprimir',
                                    menu=False)

        turno_m.children.append(query_turno)
        turno_m.children.append(insert_turno)
        turno_m.children.append(update_turno)
        turno_m.children.append(delete_turno)
        turno_m.children.append(imprimir_turno)

        query_horario = session.query(Modulo).filter(Modulo.name == 'horario_query').first()
        if query_horario is None:
            query_horario = Modulo(title='Consultar', route='',
                                   name='horario_query',
                                   menu=False)

        insert_horario = session.query(Modulo).filter(Modulo.name == 'horario_insert').first()
        if insert_horario is None:
            insert_horario = Modulo(title='Adicionar', route='/horario_insert',
                                    name='horario_insert',
                                    menu=False)
        update_horario = session.query(Modulo).filter(Modulo.name == 'horario_update').first()
        if update_horario is None:
            update_horario = Modulo(title='Actualizar', route='/horario_update',
                                    name='horario_update',
                                    menu=False)
        delete_horario = session.query(Modulo).filter(Modulo.name == 'horario_delete').first()
        if delete_horario is None:
            delete_horario = Modulo(title='Dar de Baja', route='/horario_delete',
                                    name='horario_delete',
                                    menu=False)

        imprimir_horario = session.query(Modulo).filter(Modulo.name == 'horario_imprimir').first()
        if imprimir_horario is None:
            imprimir_horario = Modulo(title='Imprimir', route='/horario_imprimir',
                                      name='horario_imprimir',
                                      menu=False)

        horario_m.children.append(query_horario)
        horario_m.children.append(insert_horario)
        horario_m.children.append(update_horario)
        horario_m.children.append(delete_horario)
        horario_m.children.append(imprimir_horario)

        query_asignacion = session.query(Modulo).filter(Modulo.name == 'asignacion_query').first()
        if query_asignacion is None:
            query_asignacion = Modulo(title='Consultar', route='',
                                      name='asignacion_query',
                                      menu=False)

        insert_asignacion = session.query(Modulo).filter(Modulo.name == 'asignacion_insert').first()
        if insert_asignacion is None:
            insert_asignacion = Modulo(title='Adicionar', route='/asignacion_insert',
                                       name='asignacion_insert',
                                       menu=False)
        update_asignacion = session.query(Modulo).filter(Modulo.name == 'asignacion_update').first()
        if update_asignacion is None:
            update_asignacion = Modulo(title='Actualizar', route='/asignacion_update',
                                       name='asignacion_update',
                                       menu=False)
        delete_asignacion = session.query(Modulo).filter(Modulo.name == 'asignacion_delete').first()
        if delete_asignacion is None:
            delete_asignacion = Modulo(title='Dar de Baja', route='/asignacion_delete',
                                       name='asignacion_delete',
                                       menu=False)

        imprimir_asignacion = session.query(Modulo).filter(Modulo.name == 'asignacion_imprimir').first()
        if imprimir_asignacion is None:
            imprimir_asignacion = Modulo(title='Imprimir', route='/asignacion_imprimir',
                                         name='asignacion_imprimir',
                                         menu=False)

        asignacion_m.children.append(query_asignacion)
        asignacion_m.children.append(insert_asignacion)
        asignacion_m.children.append(update_asignacion)
        asignacion_m.children.append(delete_asignacion)
        asignacion_m.children.append(imprimir_asignacion)

        query_autorizacion_extra = session.query(Modulo).filter(Modulo.name == 'autorizacion_extra_query').first()
        if query_autorizacion_extra is None:
            query_autorizacion_extra = Modulo(title='Consultar', route='',
                                 name='autorizacion_extra_query',
                                 menu=False)

        insert_autorizacion_extra = session.query(Modulo).filter(Modulo.name == 'autorizacion_extra_insert').first()
        if insert_autorizacion_extra is None:
            insert_autorizacion_extra = Modulo(title='Adicionar', route='/autorizacion_extra_insert',
                                  name='autorizacion_extra_insert',
                                  menu=False)
        update_autorizacion_extra = session.query(Modulo).filter(Modulo.name == 'autorizacion_extra_update').first()
        if update_autorizacion_extra is None:
            update_autorizacion_extra = Modulo(title='Actualizar', route='/autorizacion_extra_update',
                                  name='autorizacion_extra_update',
                                  menu=False)
        delete_autorizacion_extra = session.query(Modulo).filter(Modulo.name == 'autorizacion_extra_delete').first()
        if delete_autorizacion_extra is None:
            delete_autorizacion_extra = Modulo(title='Dar de Baja', route='/autorizacion_extra_delete',
                                  name='autorizacion_extra_delete',
                                  menu=False)

        imprimir_autorizacion_extra = session.query(Modulo).filter(Modulo.name == 'autorizacion_extra_imprimir').first()
        if imprimir_autorizacion_extra is None:
            imprimir_autorizacion_extra = Modulo(title='Imprimir', route='/autorizacion_extra_imprimir',
                                    name='autorizacion_extra_imprimir',
                                    menu=False)

        autorizacion_extra_m.children.append(query_autorizacion_extra)
        autorizacion_extra_m.children.append(insert_autorizacion_extra)
        autorizacion_extra_m.children.append(update_autorizacion_extra)
        autorizacion_extra_m.children.append(delete_autorizacion_extra)
        autorizacion_extra_m.children.append(imprimir_autorizacion_extra)


        query_politicas = session.query(Modulo).filter(Modulo.name == 'politicas_query').first()
        if query_politicas is None:
            query_politicas = Modulo(title='Consultar', route='',
                                      name='politicas_query',
                                      menu=False)

        insert_politicas = session.query(Modulo).filter(Modulo.name == 'politicas_insert').first()
        if insert_politicas is None:
            insert_politicas = Modulo(title='Adicionar', route='/politicas_insert',
                                       name='politicas_insert',
                                       menu=False)
        update_politicas = session.query(Modulo).filter(Modulo.name == 'politicas_update').first()
        if update_politicas is None:
            update_politicas = Modulo(title='Actualizar', route='/politicas_update',
                                       name='politicas_update',
                                       menu=False)
        delete_politicas = session.query(Modulo).filter(Modulo.name == 'politicas_delete').first()
        if delete_politicas is None:
            delete_politicas = Modulo(title='Dar de Baja', route='/politicas_delete',
                                       name='politicas_delete',
                                       menu=False)

        imprimir_politicas = session.query(Modulo).filter(Modulo.name == 'politicas_imprimir').first()
        if imprimir_politicas is None:
            imprimir_politicas = Modulo(title='Imprimir', route='/politicas_imprimir',
                                         name='politicas_imprimir',
                                         menu=False)

        politicas_m.children.append(query_politicas)
        politicas_m.children.append(insert_politicas)
        politicas_m.children.append(update_politicas)
        politicas_m.children.append(delete_politicas)
        politicas_m.children.append(imprimir_politicas)

        query_asistenciapersonal = session.query(Modulo).filter(Modulo.name == 'asistenciapersonal_query').first()
        if query_asistenciapersonal is None:
            query_asistenciapersonal = Modulo(title='Consultar', route='',
                                      name='asistenciapersonal_query',
                                      menu=False)

        insert_asistenciapersonal = session.query(Modulo).filter(Modulo.name == 'asistenciapersonal_insert').first()
        if insert_asistenciapersonal is None:
            insert_asistenciapersonal = Modulo(title='Adicionar', route='/asistenciapersonal_insert',
                                       name='asistenciapersonal_insert',
                                       menu=False)
        update_asistenciapersonal = session.query(Modulo).filter(Modulo.name == 'asistenciapersonal_update').first()
        if update_asistenciapersonal is None:
            update_asistenciapersonal = Modulo(title='Actualizar', route='/asistenciapersonal_update',
                                       name='asistenciapersonal_update',
                                       menu=False)
        delete_asistenciapersonal = session.query(Modulo).filter(Modulo.name == 'asistenciapersonal_delete').first()
        if delete_asistenciapersonal is None:
            delete_asistenciapersonal = Modulo(title='Dar de Baja', route='/asistenciapersonal_delete',
                                       name='asistenciapersonal_delete',
                                       menu=False)

        imprimir_asistenciapersonal = session.query(Modulo).filter(Modulo.name == 'asistenciapersonal_imprimir').first()
        if imprimir_asistenciapersonal is None:
            imprimir_asistenciapersonal = Modulo(title='Imprimir', route='/asistenciapersonal_imprimir',
                                         name='asistenciapersonal_imprimir',
                                         menu=False)

        asistenciapersonal_m.children.append(query_asistenciapersonal)
        asistenciapersonal_m.children.append(insert_asistenciapersonal)
        asistenciapersonal_m.children.append(update_asistenciapersonal)
        asistenciapersonal_m.children.append(delete_asistenciapersonal)
        asistenciapersonal_m.children.append(imprimir_asistenciapersonal)

        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(asistencia_m)
        admin_role.modulos.append(turno_m)
        admin_role.modulos.append(horario_m)
        admin_role.modulos.append(asignacion_m)
        admin_role.modulos.append(autorizacion_extra_m)
        admin_role.modulos.append(politicas_m)
        admin_role.modulos.append(asistenciapersonal_m)


        admin_role.modulos.append(query_turno)
        admin_role.modulos.append(insert_turno)
        admin_role.modulos.append(update_turno)
        admin_role.modulos.append(delete_turno)
        admin_role.modulos.append(imprimir_turno)

        admin_role.modulos.append(query_horario)
        admin_role.modulos.append(insert_horario)
        admin_role.modulos.append(update_horario)
        admin_role.modulos.append(delete_horario)
        admin_role.modulos.append(imprimir_horario)

        admin_role.modulos.append(query_asignacion)
        admin_role.modulos.append(insert_asignacion)
        admin_role.modulos.append(update_asignacion)
        admin_role.modulos.append(delete_asignacion)
        admin_role.modulos.append(imprimir_asignacion)

        admin_role.modulos.append(query_autorizacion_extra)
        admin_role.modulos.append(insert_autorizacion_extra)
        admin_role.modulos.append(update_autorizacion_extra)
        admin_role.modulos.append(delete_autorizacion_extra)
        admin_role.modulos.append(imprimir_autorizacion_extra)

        admin_role.modulos.append(query_politicas)
        admin_role.modulos.append(insert_politicas)
        admin_role.modulos.append(update_politicas)
        admin_role.modulos.append(delete_politicas)
        admin_role.modulos.append(imprimir_politicas)

        admin_role.modulos.append(query_asistenciapersonal)
        admin_role.modulos.append(insert_asistenciapersonal)
        admin_role.modulos.append(update_asistenciapersonal)
        admin_role.modulos.append(delete_asistenciapersonal)
        admin_role.modulos.append(imprimir_asistenciapersonal)

        session.commit()


def asistencia_schedule():

    def crear_horarios():
        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))

        with transaction() as db:
            AsistenciaManager(db).crear_horarios(fecha_zona, fecha_zona,None)

    schedule.every().day.at("00:05").do(crear_horarios)
