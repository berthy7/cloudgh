from server.database.connection import transaction
from ..dispositivos.lectores.managers import *
from ..dispositivos.marcaciones.models import *
from ..usuarios.usuario.models import Modulo
from ..usuarios.rol.models import Rol

import schedule


def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        control_m = session.query(Modulo).filter(Modulo.name == 'control').first()
        if control_m is None:
            control_m = Modulo(title='Control de Trabajo', name='control', icon='controltrabajo.ico')

        proyecto_m = session.query(Modulo).filter(Modulo.name == 'proyecto').first()
        if proyecto_m is None:
            proyecto_m = Modulo(title='Proyectos', route='/proyecto', name='proyecto',
                                   icon='seguimiento.ico')

        tarea_m = session.query(Modulo).filter(Modulo.name == 'tarea').first()
        if tarea_m is None:
            tarea_m = Modulo(title='Seguimiento de Tareas', route='/tarea', name='tarea',
                                    icon='seguimiento_tareas.ico')

        control_m.children.append(proyecto_m)
        control_m.children.append(tarea_m)

        query_proyecto = session.query(Modulo).filter(Modulo.name == 'proyecto_query').first()
        if query_proyecto is None:
            query_proyecto = Modulo(title='Consultar', route='',
                                       name='proyecto_query',
                                       menu=False)

        insert_proyecto = session.query(Modulo).filter(Modulo.name == 'proyecto_insert').first()
        if insert_proyecto is None:
            insert_proyecto = Modulo(title='Adicionar', route='/proyecto_insert',
                                        name='proyecto_insert',
                                        menu=False)
        update_proyecto = session.query(Modulo).filter(Modulo.name == 'proyecto_update').first()
        if update_proyecto is None:
            update_proyecto = Modulo(title='Actualizar', route='/proyecto_update',
                                        name='proyecto_update',
                                        menu=False)
        delete_proyecto = session.query(Modulo).filter(Modulo.name == 'proyecto_delete').first()
        if delete_proyecto is None:
            delete_proyecto = Modulo(title='Dar de Baja', route='/proyecto_delete',
                                        name='proyecto_delete',
                                        menu=False)

        imprimir_proyecto = session.query(Modulo).filter(Modulo.name == 'proyecto_imprimir').first()
        if imprimir_proyecto is None:
            imprimir_proyecto = Modulo(title='Imprimir', route='/proyecto_imprimir',
                                          name='proyecto_imprimir',
                                          menu=False)

        proyecto_m.children.append(query_proyecto)
        proyecto_m.children.append(insert_proyecto)
        proyecto_m.children.append(update_proyecto)
        proyecto_m.children.append(delete_proyecto)
        proyecto_m.children.append(imprimir_proyecto)

        query_tarea = session.query(Modulo).filter(Modulo.name == 'tarea_query').first()
        if query_tarea is None:
            query_tarea = Modulo(title='Consultar', route='',
                                       name='tarea_query',
                                       menu=False)

        insert_tarea = session.query(Modulo).filter(Modulo.name == 'tarea_insert').first()
        if insert_tarea is None:
            insert_tarea = Modulo(title='Adicionar', route='/tarea_insert',
                                        name='tarea_insert',
                                        menu=False)
        update_tarea = session.query(Modulo).filter(Modulo.name == 'tarea_update').first()
        if update_tarea is None:
            update_tarea = Modulo(title='Actualizar', route='/tarea_update',
                                        name='tarea_update',
                                        menu=False)
        delete_tarea = session.query(Modulo).filter(Modulo.name == 'tarea_delete').first()
        if delete_tarea is None:
            delete_tarea = Modulo(title='Dar de Baja', route='/tarea_delete',
                                        name='tarea_delete',
                                        menu=False)

        imprimir_tarea = session.query(Modulo).filter(Modulo.name == 'tarea_imprimir').first()
        if imprimir_tarea is None:
            imprimir_tarea = Modulo(title='Imprimir', route='/tarea_imprimir',
                                          name='tarea_imprimir',
                                          menu=False)

        tarea_m.children.append(query_tarea)
        tarea_m.children.append(insert_tarea)
        tarea_m.children.append(update_tarea)
        tarea_m.children.append(delete_tarea)
        tarea_m.children.append(imprimir_tarea)


        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(control_m)
        admin_role.modulos.append(proyecto_m)
        admin_role.modulos.append(tarea_m)

        admin_role.modulos.append(query_proyecto)
        admin_role.modulos.append(insert_proyecto)
        admin_role.modulos.append(update_proyecto)
        admin_role.modulos.append(delete_proyecto)
        admin_role.modulos.append(imprimir_proyecto)

        admin_role.modulos.append(query_tarea)
        admin_role.modulos.append(insert_tarea)
        admin_role.modulos.append(update_tarea)
        admin_role.modulos.append(delete_tarea)
        admin_role.modulos.append(imprimir_tarea)

        session.commit()

