from server.database.connection import transaction
from ..dispositivos.lectores.managers import *
from ..dispositivos.marcaciones.models import *
from ..usuarios.usuario.models import Modulo
from ..usuarios.rol.models import Rol
from ..notificaciones.correo.models import *
from ..notificaciones.correo.managers import *
import schedule


def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        portal_m = session.query(Modulo).filter(Modulo.name == 'portal').first()
        if portal_m is None:
            portal_m = Modulo(title='Portal del Empleado', name='portal', icon='portal_empleado.ico')

        portal_marcaciones_m = session.query(Modulo).filter(Modulo.name == 'portal').first()
        if portal_marcaciones_m is None:
            portal_marcaciones_m = Modulo(title='Marcaciones', route='/portal_marcaciones', name='portal_marcaciones_m', icon='marcacion.ico')

        portal_pedido_m = session.query(Modulo).filter(Modulo.name == 'portal_pedido_m').first()
        if portal_pedido_m is None:
            portal_pedido_m = Modulo(title='Ver Menú', route='/portal_pedido', name='portal_pedido_m', icon='menucomensal.ico')

        portal_tarea_m = session.query(Modulo).filter(Modulo.name == 'portal_tarea_m').first()
        if portal_tarea_m is None:
            portal_tarea_m = Modulo(title='Seguimiento de Tareas', route='/portal_tarea', name='portal_tarea_m', icon='controltrabajo.ico')

        portal_ausencia_m = session.query(Modulo).filter(Modulo.name == 'portal_ausencia_m').first()
        if portal_ausencia_m is None:
            portal_ausencia_m = Modulo(title='Solicitar Ausencia', route='/portal_ausencia', name='portal_ausencia_m', icon='solicitud.ico')

        portal_m.children.append(portal_marcaciones_m)
        portal_m.children.append(portal_pedido_m)
        portal_m.children.append(portal_tarea_m)
        portal_m.children.append(portal_ausencia_m)

        query_portal_marcaciones = session.query(Modulo).filter(Modulo.name == 'portal_marcaciones_query').first()
        if query_portal_marcaciones is None:
            query_portal_marcaciones = Modulo(title='Consultar', route='',
                                              name='portal_marcaciones_query',
                                              menu=False)

        filtrar_portal_marcaciones = session.query(Modulo).filter(Modulo.name == 'portal_marcaciones_filtrar').first()
        if filtrar_portal_marcaciones is None:
            filtrar_portal_marcaciones = Modulo(title='Filtrar', route='/portal_marcaciones_filtrar',
                                                 name='portal_marcaciones_filtrar',
                                                 menu=False)

        imprimir_portal_marcaciones = session.query(Modulo).filter(Modulo.name == 'portal_marcaciones_imprimir').first()
        if imprimir_portal_marcaciones is None:
            imprimir_portal_marcaciones = Modulo(title='Reportes', route='/portal_marcaciones_imprimir',
                                                 name='portal_marcaciones_imprimir',
                                                 menu=False)

        portal_marcaciones_m.children.append(query_portal_marcaciones)
        portal_marcaciones_m.children.append(filtrar_portal_marcaciones)
        portal_marcaciones_m.children.append(imprimir_portal_marcaciones)

        query_portal_pedido = session.query(Modulo).filter(Modulo.name == 'portal_pedido_query').first()
        if query_portal_pedido is None:
            query_portal_pedido = Modulo(title='Consultar', route='',
                                           name='portal_pedido_query',
                                           menu=False)

        insert_portal_pedido = session.query(Modulo).filter(Modulo.name == 'portal_pedido_insert').first()
        if insert_portal_pedido is None:
            insert_portal_pedido = Modulo(title='Adicionar', route='/portal_pedido_insert',
                                            name='portal_pedido_insert',
                                            menu=False)
        update_portal_pedido = session.query(Modulo).filter(Modulo.name == 'portal_pedido_update').first()
        if update_portal_pedido is None:
            update_portal_pedido = Modulo(title='Actualizar', route='/portal_pedido_update',
                                            name='portal_pedido_update',
                                            menu=False)
        delete_portal_pedido = session.query(Modulo).filter(Modulo.name == 'portal_pedido_delete').first()
        if delete_portal_pedido is None:
            delete_portal_pedido = Modulo(title='Dar de Baja', route='/portal_pedido_delete',
                                            name='portal_pedido_delete',
                                            menu=False)

        imprimir_portal_pedido = session.query(Modulo).filter(Modulo.name == 'portal_pedido_imprimir').first()
        if imprimir_portal_pedido is None:
            imprimir_portal_pedido = Modulo(title='Reportes', route='/portal_pedido_imprimir',
                                              name='portal_pedido_imprimir',
                                              menu=False)

        portal_pedido_m.children.append(query_portal_pedido)
        portal_pedido_m.children.append(insert_portal_pedido)
        portal_pedido_m.children.append(update_portal_pedido)
        portal_pedido_m.children.append(delete_portal_pedido)
        portal_pedido_m.children.append(imprimir_portal_pedido)

        query_portal_tarea = session.query(Modulo).filter(Modulo.name == 'portal_tarea_query').first()
        if query_portal_tarea is None:
            query_portal_tarea = Modulo(title='Consultar', route='',
                                           name='portal_tarea_query',
                                           menu=False)

        insert_portal_tarea = session.query(Modulo).filter(Modulo.name == 'portal_tarea_insert').first()
        if insert_portal_tarea is None:
            insert_portal_tarea = Modulo(title='Adicionar', route='/portal_tarea_insert',
                                            name='portal_tarea_insert',
                                            menu=False)
        update_portal_tarea = session.query(Modulo).filter(Modulo.name == 'portal_tarea_update').first()
        if update_portal_tarea is None:
            update_portal_tarea = Modulo(title='Actualizar', route='/portal_tarea_update',
                                            name='portal_tarea_update',
                                            menu=False)
        delete_portal_tarea = session.query(Modulo).filter(Modulo.name == 'portal_tarea_delete').first()
        if delete_portal_tarea is None:
            delete_portal_tarea = Modulo(title='Dar de Baja', route='/portal_tarea_delete',
                                            name='portal_tarea_delete',
                                            menu=False)

        imprimir_portal_tarea = session.query(Modulo).filter(Modulo.name == 'portal_tarea_imprimir').first()
        if imprimir_portal_tarea is None:
            imprimir_portal_tarea = Modulo(title='Reportes', route='/portal_tarea_imprimir',
                                              name='portal_tarea_imprimir',
                                              menu=False)

        portal_tarea_m.children.append(query_portal_tarea)
        portal_tarea_m.children.append(insert_portal_tarea)
        portal_tarea_m.children.append(update_portal_tarea)
        portal_tarea_m.children.append(delete_portal_tarea)
        portal_tarea_m.children.append(imprimir_portal_tarea)


        query_portal_ausencia = session.query(Modulo).filter(Modulo.name == 'portal_ausencia_query').first()
        if query_portal_ausencia is None:
            query_portal_ausencia = Modulo(title='Consultar', route='',
                                           name='portal_ausencia_query',
                                           menu=False)

        insert_portal_ausencia = session.query(Modulo).filter(Modulo.name == 'portal_ausencia_insert').first()
        if insert_portal_ausencia is None:
            insert_portal_ausencia = Modulo(title='Adicionar', route='/portal_ausencia_insert',
                                            name='portal_ausencia_insert',
                                            menu=False)
        update_portal_ausencia = session.query(Modulo).filter(Modulo.name == 'portal_ausencia_update').first()
        if update_portal_ausencia is None:
            update_portal_ausencia = Modulo(title='Actualizar', route='/portal_ausencia_update',
                                            name='portal_ausencia_update',
                                            menu=False)
        delete_portal_ausencia = session.query(Modulo).filter(Modulo.name == 'portal_ausencia_delete').first()
        if delete_portal_ausencia is None:
            delete_portal_ausencia = Modulo(title='Dar de Baja', route='/portal_ausencia_delete',
                                            name='portal_ausencia_delete',
                                            menu=False)

        imprimir_portal_ausencia = session.query(Modulo).filter(Modulo.name == 'portal_ausencia_imprimir').first()
        if imprimir_portal_ausencia is None:
            imprimir_portal_ausencia = Modulo(title='Reportes', route='/portal_ausencia_imprimir',
                                              name='portal_ausencia_imprimir',
                                              menu=False)

        portal_ausencia_m.children.append(query_portal_ausencia)
        portal_ausencia_m.children.append(insert_portal_ausencia)
        portal_ausencia_m.children.append(update_portal_ausencia)
        portal_ausencia_m.children.append(delete_portal_ausencia)
        portal_ausencia_m.children.append(imprimir_portal_ausencia)

        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        personal_role = session.query(Rol).filter(Rol.nombre == 'PERSONAL').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(portal_m)
        admin_role.modulos.append(portal_marcaciones_m)
        admin_role.modulos.append(portal_pedido_m)
        admin_role.modulos.append(portal_tarea_m)
        admin_role.modulos.append(portal_ausencia_m)

        admin_role.modulos.append(query_portal_marcaciones)
        admin_role.modulos.append(filtrar_portal_marcaciones)
        admin_role.modulos.append(imprimir_portal_marcaciones)

        admin_role.modulos.append(query_portal_pedido)
        admin_role.modulos.append(insert_portal_pedido)
        admin_role.modulos.append(update_portal_pedido)
        admin_role.modulos.append(delete_portal_pedido)
        admin_role.modulos.append(imprimir_portal_pedido)

        admin_role.modulos.append(query_portal_tarea)
        admin_role.modulos.append(insert_portal_tarea)
        admin_role.modulos.append(update_portal_tarea)
        admin_role.modulos.append(delete_portal_tarea)
        admin_role.modulos.append(imprimir_portal_tarea)

        admin_role.modulos.append(query_portal_ausencia)
        admin_role.modulos.append(insert_portal_ausencia)
        admin_role.modulos.append(update_portal_ausencia)
        admin_role.modulos.append(delete_portal_ausencia)
        admin_role.modulos.append(imprimir_portal_ausencia)

        personal_role.modulos.append(portal_m)
        personal_role.modulos.append(portal_marcaciones_m)
        personal_role.modulos.append(portal_pedido_m)
        personal_role.modulos.append(portal_tarea_m)
        personal_role.modulos.append(portal_ausencia_m)

        personal_role.modulos.append(query_portal_marcaciones)
        personal_role.modulos.append(filtrar_portal_marcaciones)
        personal_role.modulos.append(imprimir_portal_marcaciones)

        personal_role.modulos.append(query_portal_pedido)
        personal_role.modulos.append(insert_portal_pedido)
        personal_role.modulos.append(update_portal_pedido)
        personal_role.modulos.append(delete_portal_pedido)
        personal_role.modulos.append(imprimir_portal_pedido)

        personal_role.modulos.append(query_portal_tarea)
        personal_role.modulos.append(insert_portal_tarea)
        personal_role.modulos.append(update_portal_tarea)
        personal_role.modulos.append(delete_portal_tarea)
        personal_role.modulos.append(imprimir_portal_tarea)

        personal_role.modulos.append(query_portal_ausencia)
        personal_role.modulos.append(insert_portal_ausencia)
        personal_role.modulos.append(update_portal_ausencia)
        personal_role.modulos.append(delete_portal_ausencia)
        personal_role.modulos.append(imprimir_portal_ausencia)

        session.commit()







