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
            portal_m = Modulo(title='Portal del Empleado', name='portal', icon='portal_empleado.png')

        portal_asistencia_m = session.query(Modulo).filter(Modulo.name == 'portal_asistencia_m').first()
        if portal_asistencia_m is None:
            portal_asistencia_m = Modulo(title='Asistencia Oficina en casa', route='/portal_asistencia', name='portal_asistencia_m', icon='homeoffice.png')

        portal_marcaciones_m = session.query(Modulo).filter(Modulo.name == 'portal').first()
        if portal_marcaciones_m is None:
            portal_marcaciones_m = Modulo(title='Marcaciones', route='/portal_marcaciones', name='portal_marcaciones_m', icon='marcacion.png')

        portal_pedido_m = session.query(Modulo).filter(Modulo.name == 'portal_pedido_m').first()
        if portal_pedido_m is None:
            portal_pedido_m = Modulo(title='Ver Menú', route='/portal_pedido', name='portal_pedido_m', icon='menu.png')

        # portal_tarea_m = session.query(Modulo).filter(Modulo.name == 'portal_tarea_m').first()
        # if portal_tarea_m is None:
        #     portal_tarea_m = Modulo(title='Seguimiento de Tareas', route='/portal_tarea', name='portal_tarea_m', icon='controltrabajo.ico')

        portal_permiso_m = session.query(Modulo).filter(Modulo.name == 'portal_permiso_m').first()
        if portal_permiso_m is None:
            portal_permiso_m = Modulo(title='Autorizaciones de salida', route='/portal_permiso', name='portal_permiso_m', icon='autorizacionsalida.png')

        portal_licencia_m = session.query(Modulo).filter(Modulo.name == 'portal_licencia_m').first()
        if portal_licencia_m is None:
            portal_licencia_m = Modulo(title='Licencias', route='/portal_licencia', name='portal_licencia_m', icon='licencia.png')

        portal_regularizacion_m = session.query(Modulo).filter(Modulo.name == 'portal_licencia_m').first()
        if portal_regularizacion_m is None:
            portal_regularizacion_m = Modulo(title='Regularizacion', route='/portal_regularizacion', name='portal_regularizacion_m', icon='asistenciapersonal.png')

        portal_vacacion_m = session.query(Modulo).filter(Modulo.name == 'portal_vacacion').first()
        if portal_vacacion_m is None:
            portal_vacacion_m = Modulo(title='Solicitud de Vacacion', route='/portal_vacacion', name='portal_vacacion', icon='solicitudvacacion.png')

        portal_m.children.append(portal_asistencia_m)
        portal_m.children.append(portal_marcaciones_m)
        # portal_m.children.append(portal_pedido_m)

        portal_m.children.append(portal_permiso_m)
        portal_m.children.append(portal_licencia_m)
        portal_m.children.append(portal_regularizacion_m)
        portal_m.children.append(portal_vacacion_m)

        query_portal_asistencia = session.query(Modulo).filter(Modulo.name == 'portal_asistencia_query').first()
        if query_portal_asistencia is None:
            query_portal_asistencia = Modulo(title='Consultar', route='',
                                              name='portal_asistencia_query',
                                              menu=False)

        insert_portal_asistencia = session.query(Modulo).filter(Modulo.name == 'portal_asistencia_insert').first()
        if insert_portal_asistencia is None:
            insert_portal_asistencia = Modulo(title='Adicionar', route='/portal_asistencia_insert',
                                            name='portal_asistencia_insert',
                                            menu=False)
        update_portal_asistencia = session.query(Modulo).filter(Modulo.name == 'portal_asistencia_update').first()
        if update_portal_asistencia is None:
            update_portal_asistencia = Modulo(title='Actualizar', route='/portal_asistencia_update',
                                            name='portal_asistencia_update',
                                            menu=False)

        portal_asistencia_m.children.append(query_portal_asistencia)
        portal_asistencia_m.children.append(insert_portal_asistencia)
        portal_asistencia_m.children.append(update_portal_asistencia)



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

        # portal_pedido_m.children.append(query_portal_pedido)
        # portal_pedido_m.children.append(insert_portal_pedido)
        # portal_pedido_m.children.append(update_portal_pedido)
        # portal_pedido_m.children.append(delete_portal_pedido)
        # portal_pedido_m.children.append(imprimir_portal_pedido)

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

        # portal_tarea_m.children.append(query_portal_tarea)
        # portal_tarea_m.children.append(insert_portal_tarea)
        # portal_tarea_m.children.append(update_portal_tarea)
        # portal_tarea_m.children.append(delete_portal_tarea)
        # portal_tarea_m.children.append(imprimir_portal_tarea)

        query_portal_permiso = session.query(Modulo).filter(Modulo.name == 'portal_permiso_query').first()
        if query_portal_permiso is None:
            query_portal_permiso = Modulo(title='Consultar', route='',
                                   name='portal_permiso_query',
                                   menu=False)

        insert_portal_permiso = session.query(Modulo).filter(Modulo.name == 'portal_permiso_insert').first()
        if insert_portal_permiso is None:
            insert_portal_permiso = Modulo(title='Adicionar', route='/portal_permiso_insert',
                                    name='portal_permiso_insert',
                                    menu=False)

        update_portal_permiso = session.query(Modulo).filter(Modulo.name == 'portal_permiso_update').first()
        if update_portal_permiso is None:
            update_portal_permiso = Modulo(title='Actualizar', route='/portal_permiso_update',
                                    name='portal_permiso_update',
                                    menu=False)
        delete_portal_permiso = session.query(Modulo).filter(Modulo.name == 'portal_permiso_delete').first()
        if delete_portal_permiso is None:
            delete_portal_permiso = Modulo(title='Dar de Baja', route='/portal_permiso_delete',
                                    name='portal_permiso_delete',
                                    menu=False)

        imprimir_portal_permiso = session.query(Modulo).filter(Modulo.name == 'portal_permiso_imprimir').first()
        if imprimir_portal_permiso is None:
            imprimir_portal_permiso = Modulo(title='Imprimir', route='/portal_permiso_imprimir',
                                      name='portal_permiso_imprimir',
                                      menu=False)

        autorizacion_portal_permiso = session.query(Modulo).filter(Modulo.name == 'portal_permiso_autorizacion').first()
        if autorizacion_portal_permiso is None:
            autorizacion_portal_permiso = Modulo(title='Autorizacion', route='/portal_permiso_autorizacion',
                                          name='portal_permiso_autorizacion',
                                          menu=False)

        aprobacion_portal_permiso = session.query(Modulo).filter(Modulo.name == 'portal_permiso_aprobacion').first()
        if aprobacion_portal_permiso is None:
            aprobacion_portal_permiso = Modulo(title='Aprobacion', route='/portal_permiso_aprobacion',
                                          name='portal_permiso_aprobacion',
                                          menu=False)

        portal_permiso_m.children.append(query_portal_permiso)
        portal_permiso_m.children.append(insert_portal_permiso)
        portal_permiso_m.children.append(update_portal_permiso)
        portal_permiso_m.children.append(delete_portal_permiso)
        portal_permiso_m.children.append(imprimir_portal_permiso)
        portal_permiso_m.children.append(autorizacion_portal_permiso)
        portal_permiso_m.children.append(aprobacion_portal_permiso)

        query_portal_licencia = session.query(Modulo).filter(Modulo.name == 'portal_licencia_query').first()
        if query_portal_licencia is None:
            query_portal_licencia = Modulo(title='Consultar', route='',
                                           name='portal_licencia_query',
                                           menu=False)

        insert_portal_licencia = session.query(Modulo).filter(Modulo.name == 'portal_licencia_insert').first()
        if insert_portal_licencia is None:
            insert_portal_licencia = Modulo(title='Adicionar', route='/portal_licencia_insert',
                                            name='portal_licencia_insert',
                                            menu=False)
        update_portal_licencia = session.query(Modulo).filter(Modulo.name == 'portal_licencia_update').first()
        if update_portal_licencia is None:
            update_portal_licencia = Modulo(title='Actualizar', route='/portal_licencia_update',
                                            name='portal_licencia_update',
                                            menu=False)
        delete_portal_licencia = session.query(Modulo).filter(Modulo.name == 'portal_licencia_delete').first()
        if delete_portal_licencia is None:
            delete_portal_licencia = Modulo(title='Dar de Baja', route='/portal_licencia_delete',
                                            name='portal_licencia_delete',
                                            menu=False)

        imprimir_portal_licencia = session.query(Modulo).filter(Modulo.name == 'portal_licencia_imprimir').first()
        if imprimir_portal_licencia is None:
            imprimir_portal_licencia = Modulo(title='Imprimir', route='/portal_licencia_imprimir',
                                              name='portal_licencia_imprimir',
                                              menu=False)

        autorizacion_portal_licencia = session.query(Modulo).filter(Modulo.name == 'portal_permiso_autorizacion').first()
        if autorizacion_portal_licencia is None:
            autorizacion_portal_licencia = Modulo(title='Autorizacion', route='/portal_licencia_autorizacion',
                                                  name='portal_licencia_autorizacion',
                                                  menu=False)

        aprobacion_portal_licencia = session.query(Modulo).filter(Modulo.name == 'portal_licencia_aprobacion').first()
        if aprobacion_portal_licencia is None:
            aprobacion_portal_licencia = Modulo(title='Aprobacion', route='/portal_licencia_aprobacion',
                                                  name='portal_licencia_aprobacion',
                                                  menu=False)

        portal_licencia_m.children.append(query_portal_licencia)
        portal_licencia_m.children.append(insert_portal_licencia)
        portal_licencia_m.children.append(update_portal_licencia)
        portal_licencia_m.children.append(delete_portal_licencia)
        portal_licencia_m.children.append(imprimir_portal_licencia)
        portal_licencia_m.children.append(autorizacion_portal_licencia)
        portal_licencia_m.children.append(aprobacion_portal_licencia)

        query_portal_regularizacion = session.query(Modulo).filter(Modulo.name == 'portal_regularizacion_query').first()
        if query_portal_regularizacion is None:
            query_portal_regularizacion = Modulo(title='Consultar', route='',
                                                 name='portal_regularizacion_query',
                                                 menu=False)

        insert_portal_regularizacion = session.query(Modulo).filter(
            Modulo.name == 'portal_regularizacion_insert').first()
        if insert_portal_regularizacion is None:
            insert_portal_regularizacion = Modulo(title='Adicionar', route='/portal_regularizacion_insert',
                                                  name='portal_regularizacion_insert',
                                                  menu=False)

        update_portal_regularizacion = session.query(Modulo).filter(
            Modulo.name == 'portal_regularizacion_update').first()
        if update_portal_regularizacion is None:
            update_portal_regularizacion = Modulo(title='Actualizar', route='/portal_regularizacion_update',
                                                  name='portal_regularizacion_update',
                                                  menu=False)
        delete_portal_regularizacion = session.query(Modulo).filter(
            Modulo.name == 'portal_regularizacion_delete').first()
        if delete_portal_regularizacion is None:
            delete_portal_regularizacion = Modulo(title='Dar de Baja', route='/portal_regularizacion_delete',
                                                  name='portal_regularizacion_delete',
                                                  menu=False)

        imprimir_portal_regularizacion = session.query(Modulo).filter(
            Modulo.name == 'portal_regularizacion_imprimir').first()
        if imprimir_portal_regularizacion is None:
            imprimir_portal_regularizacion = Modulo(title='Imprimir', route='/portal_regularizacion_imprimir',
                                                    name='portal_regularizacion_imprimir',
                                                    menu=False)

        autorizacion_portal_regularizacion = session.query(Modulo).filter(
            Modulo.name == 'portal_regularizacion_autorizacion').first()
        if autorizacion_portal_regularizacion is None:
            autorizacion_portal_regularizacion = Modulo(title='Autorizacion',
                                                        route='/portal_regularizacion_autorizacion',
                                                        name='portal_regularizacion_autorizacion',
                                                        menu=False)

        aprobacion_portal_regularizacion = session.query(Modulo).filter(
            Modulo.name == 'portal_regularizacion_aprobacion').first()
        if aprobacion_portal_regularizacion is None:
            aprobacion_portal_regularizacion = Modulo(title='Aprobacion', route='/portal_regularizacion_aprobacion',
                                                      name='portal_regularizacion_aprobacion',
                                                      menu=False)

        portal_regularizacion_m.children.append(query_portal_regularizacion)
        portal_regularizacion_m.children.append(insert_portal_regularizacion)
        portal_regularizacion_m.children.append(update_portal_regularizacion)
        portal_regularizacion_m.children.append(delete_portal_regularizacion)
        portal_regularizacion_m.children.append(imprimir_portal_regularizacion)
        portal_regularizacion_m.children.append(autorizacion_portal_regularizacion)
        portal_regularizacion_m.children.append(aprobacion_portal_regularizacion)


        query_portal_vacacion = session.query(Modulo).filter(Modulo.name == 'portal_vacacion_query').first()
        if query_portal_vacacion is None:
            query_portal_vacacion = Modulo(title='Consultar', route='',
                                           name='portal_vacacion_query',
                                           menu=False)

        insert_portal_vacacion = session.query(Modulo).filter(Modulo.name == 'portal_vacacion_insert').first()
        if insert_portal_vacacion is None:
            insert_portal_vacacion = Modulo(title='Adicionar', route='/portal_vacacion_insert',
                                            name='portal_vacacion_insert',
                                            menu=False)
        update_portal_vacacion = session.query(Modulo).filter(Modulo.name == 'portal_vacacion_update').first()
        if update_portal_vacacion is None:
            update_portal_vacacion = Modulo(title='Actualizar', route='/portal_vacacion_update',
                                            name='portal_vacacion_update',
                                            menu=False)
        delete_portal_vacacion = session.query(Modulo).filter(Modulo.name == 'portal_vacacion_delete').first()
        if delete_portal_vacacion is None:
            delete_portal_vacacion = Modulo(title='Dar de Baja', route='/portal_vacacion_delete',
                                            name='portal_vacacion_delete',
                                            menu=False)

        imprimir_portal_vacacion = session.query(Modulo).filter(Modulo.name == 'portal_vacacion_imprimir').first()
        if imprimir_portal_vacacion is None:
            imprimir_portal_vacacion = Modulo(title='Imprimir', route='/portal_vacacion_imprimir',
                                              name='portal_vacacion_imprimir',
                                              menu=False)

        autorizacion_portal_vacacion = session.query(Modulo).filter(Modulo.name == 'portal_vacacion_autorizacion').first()
        if autorizacion_portal_vacacion is None:
            autorizacion_portal_vacacion = Modulo(title='Autorizacion', route='/portal_vacacion_autorizacion',
                                                  name='portal_vacacion_autorizacion',
                                                  menu=False)

        aprobacion_portal_vacacion = session.query(Modulo).filter(Modulo.name == 'portal_vacacion_aprobacion').first()
        if aprobacion_portal_vacacion is None:
            aprobacion_portal_vacacion = Modulo(title='Aprobacion', route='/portal_vacacion_aprobacion',
                                                  name='portal_vacacion_aprobacion',
                                                  menu=False)

        portal_vacacion_m.children.append(query_portal_vacacion)
        portal_vacacion_m.children.append(insert_portal_vacacion)
        portal_vacacion_m.children.append(update_portal_vacacion)
        portal_vacacion_m.children.append(delete_portal_vacacion)
        portal_vacacion_m.children.append(imprimir_portal_vacacion)
        portal_vacacion_m.children.append(autorizacion_portal_vacacion)
        portal_vacacion_m.children.append(aprobacion_portal_vacacion)

        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()


        ###Modulos de Operaciones

        admin_role.modulos.append(portal_m)
        admin_role.modulos.append(portal_asistencia_m)
        admin_role.modulos.append(portal_marcaciones_m)
        # admin_role.modulos.append(portal_pedido_m)
        # admin_role.modulos.append(portal_tarea_m)
        admin_role.modulos.append(portal_permiso_m)
        admin_role.modulos.append(portal_licencia_m)
        admin_role.modulos.append(portal_regularizacion_m)
        admin_role.modulos.append(portal_vacacion_m)

        admin_role.modulos.append(query_portal_asistencia)
        admin_role.modulos.append(insert_portal_asistencia)
        admin_role.modulos.append(update_portal_asistencia)

        admin_role.modulos.append(query_portal_marcaciones)
        admin_role.modulos.append(filtrar_portal_marcaciones)
        admin_role.modulos.append(imprimir_portal_marcaciones)

        # admin_role.modulos.append(query_portal_pedido)
        # admin_role.modulos.append(insert_portal_pedido)
        # admin_role.modulos.append(update_portal_pedido)
        # admin_role.modulos.append(delete_portal_pedido)
        # admin_role.modulos.append(imprimir_portal_pedido)

        # admin_role.modulos.append(query_portal_tarea)
        # admin_role.modulos.append(insert_portal_tarea)
        # admin_role.modulos.append(update_portal_tarea)
        # admin_role.modulos.append(delete_portal_tarea)
        # admin_role.modulos.append(imprimir_portal_tarea)

        admin_role.modulos.append(query_portal_permiso)
        admin_role.modulos.append(insert_portal_permiso)
        admin_role.modulos.append(update_portal_permiso)
        admin_role.modulos.append(delete_portal_permiso)
        admin_role.modulos.append(imprimir_portal_permiso)
        admin_role.modulos.append(autorizacion_portal_permiso)
        admin_role.modulos.append(aprobacion_portal_permiso)

        admin_role.modulos.append(query_portal_licencia)
        admin_role.modulos.append(insert_portal_licencia)
        admin_role.modulos.append(update_portal_licencia)
        admin_role.modulos.append(delete_portal_licencia)
        admin_role.modulos.append(imprimir_portal_licencia)
        admin_role.modulos.append(autorizacion_portal_licencia)
        admin_role.modulos.append(aprobacion_portal_licencia)

        admin_role.modulos.append(query_portal_regularizacion)
        admin_role.modulos.append(insert_portal_regularizacion)
        admin_role.modulos.append(update_portal_regularizacion)
        admin_role.modulos.append(delete_portal_regularizacion)
        admin_role.modulos.append(imprimir_portal_regularizacion)
        admin_role.modulos.append(autorizacion_portal_regularizacion)
        admin_role.modulos.append(aprobacion_portal_regularizacion)

        admin_role.modulos.append(query_portal_vacacion)
        admin_role.modulos.append(insert_portal_vacacion)
        admin_role.modulos.append(update_portal_vacacion)
        admin_role.modulos.append(delete_portal_vacacion)
        admin_role.modulos.append(imprimir_portal_vacacion)
        admin_role.modulos.append(autorizacion_portal_vacacion)
        admin_role.modulos.append(aprobacion_portal_vacacion)

        # personal_role.modulos.append(portal_m)
        # personal_role.modulos.append(portal_asistencia_m)
        # personal_role.modulos.append(portal_marcaciones_m)
        # personal_role.modulos.append(portal_pedido_m)
        # personal_role.modulos.append(portal_tarea_m)
        # personal_role.modulos.append(portal_permiso_m)
        # personal_role.modulos.append(portal_licencia_m)
        # personal_role.modulos.append(portal_vacacion_m)
        #
        # personal_role.modulos.append(query_portal_asistencia)
        # personal_role.modulos.append(insert_portal_asistencia)
        # personal_role.modulos.append(update_portal_asistencia)
        #
        # personal_role.modulos.append(query_portal_marcaciones)
        # personal_role.modulos.append(filtrar_portal_marcaciones)
        # personal_role.modulos.append(imprimir_portal_marcaciones)

        # personal_role.modulos.append(query_portal_pedido)
        # personal_role.modulos.append(insert_portal_pedido)
        # personal_role.modulos.append(update_portal_pedido)
        # personal_role.modulos.append(delete_portal_pedido)
        # personal_role.modulos.append(imprimir_portal_pedido)

        # personal_role.modulos.append(query_portal_tarea)
        # personal_role.modulos.append(insert_portal_tarea)
        # personal_role.modulos.append(update_portal_tarea)
        # personal_role.modulos.append(delete_portal_tarea)
        # personal_role.modulos.append(imprimir_portal_tarea)

        # personal_role.modulos.append(query_portal_permiso)
        # personal_role.modulos.append(insert_portal_permiso)
        # personal_role.modulos.append(update_portal_permiso)
        # personal_role.modulos.append(delete_portal_permiso)
        # personal_role.modulos.append(imprimir_portal_permiso)
        # personal_role.modulos.append(autorizacion_portal_permiso)
        # personal_role.modulos.append(aprobacion_portal_permiso)
        #
        # personal_role.modulos.append(query_portal_licencia)
        # personal_role.modulos.append(insert_portal_licencia)
        # personal_role.modulos.append(update_portal_licencia)
        # personal_role.modulos.append(delete_portal_licencia)
        # personal_role.modulos.append(imprimir_portal_licencia)
        # personal_role.modulos.append(autorizacion_portal_licencia)
        # personal_role.modulos.append(aprobacion_portal_licencia)
        #
        # personal_role.modulos.append(query_portal_vacacion)
        # personal_role.modulos.append(insert_portal_vacacion)
        # personal_role.modulos.append(update_portal_vacacion)
        # personal_role.modulos.append(delete_portal_vacacion)
        # personal_role.modulos.append(imprimir_portal_vacacion)
        # personal_role.modulos.append(autorizacion_portal_vacacion)
        # personal_role.modulos.append(aprobacion_portal_vacacion)

        session.commit()







