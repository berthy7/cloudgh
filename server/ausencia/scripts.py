from ..usuarios.rol.models import Modulo
from ..usuarios.rol.models import Rol
from .tipoausencia.models import *

from server.database.connection import transaction
from datetime import datetime

import schedule
import pytz

def insertions():
    with transaction() as session:

        ###Modulo de Operaciones

        ausencia_m = session.query(Modulo).filter(Modulo.name == 'ausencia').first()
        if ausencia_m is None:
            ausencia_m = Modulo(title='Ausencia', name='ausencia', icon='ausencia.png')


        permiso_m = session.query(Modulo).filter(Modulo.name == 'permiso').first()
        if permiso_m is None:
            permiso_m = Modulo(title='Autorizaciones de salida', route='/permiso', name='permiso', icon='autorizacionsalida.png')

        licencia_m = session.query(Modulo).filter(Modulo.name == 'licencia').first()
        if licencia_m is None:
            licencia_m = Modulo(title='Licencias', route='/licencia', name='licencia', icon='licencia.png')


        regularizacion_m = session.query(Modulo).filter(Modulo.name == 'regularizacion').first()
        if regularizacion_m is None:
            regularizacion_m = Modulo(title='Regularizacion', route='/regularizacion', name='regularizacion', icon='asistenciapersonal.png')

        tipoausencia_m = session.query(Modulo).filter(Modulo.name == 'tipoausencia').first()
        if tipoausencia_m is None:
            tipoausencia_m = Modulo(title='Tipos de Ausencias', route='/tipoausencia', name='tipoausencia', icon='tipoausencia.png')


        ausencia_m.children.append(permiso_m )
        ausencia_m.children.append(licencia_m)
        ausencia_m.children.append(regularizacion_m)
        ausencia_m.children.append(tipoausencia_m)



        query_permiso = session.query(Modulo).filter(Modulo.name == 'permiso_query').first()
        if query_permiso is None:
            query_permiso = Modulo(title='Consultar', route='',
                                      name='permiso_query',
                                      menu=False)

        insert_permiso = session.query(Modulo).filter(Modulo.name == 'permiso_insert').first()
        if insert_permiso is None:
            insert_permiso = Modulo(title='Adicionar', route='/permiso_insert',
                                       name='permiso_insert',
                                       menu=False)
        update_permiso = session.query(Modulo).filter(Modulo.name == 'permiso_update').first()
        if update_permiso is None:
            update_permiso = Modulo(title='Actualizar', route='/permiso_update',
                                       name='permiso_update',
                                       menu=False)
        delete_permiso = session.query(Modulo).filter(Modulo.name == 'permiso_delete').first()
        if delete_permiso is None:
            delete_permiso = Modulo(title='Dar de Baja', route='/permiso_delete',
                                       name='permiso_delete',
                                       menu=False)

        imprimir_permiso = session.query(Modulo).filter(Modulo.name == 'permiso_imprimir').first()
        if imprimir_permiso is None:
            imprimir_permiso = Modulo(title='Imprimir', route='/permiso_imprimir',
                                         name='permiso_imprimir',
                                         menu=False)

        autorizacion_permiso = session.query(Modulo).filter(Modulo.name == 'permiso_autorizacion').first()
        if autorizacion_permiso is None:
            autorizacion_permiso = Modulo(title='Autorizacion', route='/permiso_autorizacion',
                                         name='permiso_autorizacion',
                                         menu=False)

        aprobacion_permiso = session.query(Modulo).filter(Modulo.name == 'permiso_aprobacion').first()
        if aprobacion_permiso is None:
            aprobacion_permiso = Modulo(title='Aprobacion', route='/permiso_aprobacion',
                                         name='permiso_aprobacion',
                                         menu=False)

        permiso_m.children.append(query_permiso)
        permiso_m.children.append(insert_permiso)
        permiso_m.children.append(update_permiso)
        permiso_m.children.append(delete_permiso)
        permiso_m.children.append(imprimir_permiso)
        permiso_m.children.append(autorizacion_permiso)
        permiso_m.children.append(aprobacion_permiso)

        query_licencia = session.query(Modulo).filter(Modulo.name == 'licencia_query').first()
        if query_licencia is None:
            query_licencia = Modulo(title='Consultar', route='',
                                      name='licencia_query',
                                      menu=False)

        insert_licencia = session.query(Modulo).filter(Modulo.name == 'licencia_insert').first()
        if insert_licencia is None:
            insert_licencia = Modulo(title='Adicionar', route='/licencia_insert',
                                       name='licencia_insert',
                                       menu=False)
        update_licencia = session.query(Modulo).filter(Modulo.name == 'licencia_update').first()
        if update_licencia is None:
            update_licencia = Modulo(title='Actualizar', route='/licencia_update',
                                       name='licencia_update',
                                       menu=False)
        delete_licencia = session.query(Modulo).filter(Modulo.name == 'licencia_delete').first()
        if delete_licencia is None:
            delete_licencia = Modulo(title='Dar de Baja', route='/licencia_delete',
                                       name='licencia_delete',
                                       menu=False)

        imprimir_licencia = session.query(Modulo).filter(Modulo.name == 'licencia_imprimir').first()
        if imprimir_licencia is None:
            imprimir_licencia = Modulo(title='Imprimir', route='/licencia_imprimir',
                                         name='licencia_imprimir',
                                         menu=False)

        autorizacion_licencia = session.query(Modulo).filter(Modulo.name == 'permiso_autorizacion').first()
        if autorizacion_licencia is None:
            autorizacion_licencia = Modulo(title='Autorizacion', route='/licencia_autorizacion',
                                         name='licencia_autorizacion',
                                         menu=False)

        aprobacion_licencia = session.query(Modulo).filter(Modulo.name == 'permiso_aprobacion').first()
        if aprobacion_licencia is None:
            aprobacion_licencia = Modulo(title='Aprobacion', route='/licencia_aprobacion',
                                         name='licencia_aprobacion',
                                         menu=False)

        licencia_m.children.append(query_licencia)
        licencia_m.children.append(insert_licencia)
        licencia_m.children.append(update_licencia)
        licencia_m.children.append(delete_licencia)
        licencia_m.children.append(imprimir_licencia)
        licencia_m.children.append(autorizacion_licencia)
        licencia_m.children.append(aprobacion_licencia)

        query_regularizacion = session.query(Modulo).filter(Modulo.name == 'regularizacion_query').first()
        if query_regularizacion is None:
            query_regularizacion = Modulo(title='Consultar', route='',
                                          name='regularizacion_query',
                                          menu=False)

        insert_regularizacion = session.query(Modulo).filter(Modulo.name == 'regularizacion_insert').first()
        if insert_regularizacion is None:
            insert_regularizacion = Modulo(title='Adicionar', route='/regularizacion_insert',
                                           name='regularizacion_insert',
                                           menu=False)
        update_regularizacion = session.query(Modulo).filter(Modulo.name == 'regularizacion_update').first()
        if update_regularizacion is None:
            update_regularizacion = Modulo(title='Actualizar', route='/regularizacion_update',
                                           name='regularizacion_update',
                                           menu=False)
        delete_regularizacion = session.query(Modulo).filter(Modulo.name == 'regularizacion_delete').first()
        if delete_regularizacion is None:
            delete_regularizacion = Modulo(title='Dar de Baja', route='/regularizacion_delete',
                                           name='regularizacion_delete',
                                           menu=False)

        imprimir_regularizacion = session.query(Modulo).filter(Modulo.name == 'regularizacion_imprimir').first()
        if imprimir_regularizacion is None:
            imprimir_regularizacion = Modulo(title='Imprimir', route='/regularizacion_imprimir',
                                             name='regularizacion_imprimir',
                                             menu=False)

        autorizacion_regularizacion = session.query(Modulo).filter(Modulo.name == 'regularizacion_autorizacion').first()
        if autorizacion_regularizacion is None:
            autorizacion_regularizacion = Modulo(title='Autorizacion', route='/regularizacion_autorizacion',
                                                 name='regularizacion_autorizacion',
                                                 menu=False)

        aprobacion_regularizacion = session.query(Modulo).filter(Modulo.name == 'regularizacion_aprobacion').first()
        if aprobacion_regularizacion is None:
            aprobacion_regularizacion = Modulo(title='Aprobacion', route='/regularizacion_aprobacion',
                                               name='regularizacion_aprobacion',
                                               menu=False)

        regularizacion_m.children.append(query_regularizacion)
        regularizacion_m.children.append(insert_regularizacion)
        regularizacion_m.children.append(update_regularizacion)
        regularizacion_m.children.append(delete_regularizacion)
        regularizacion_m.children.append(imprimir_regularizacion)
        regularizacion_m.children.append(autorizacion_regularizacion)
        regularizacion_m.children.append(aprobacion_regularizacion)



        query_tipoausencia = session.query(Modulo).filter(Modulo.name == 'tipoausencia_query').first()
        if query_tipoausencia is None:
            query_tipoausencia = Modulo(title='Consultar', route='',
                                        name='tipoausencia_query',
                                        menu=False)

        insert_tipoausencia = session.query(Modulo).filter(Modulo.name == 'tipoausencia_insert').first()
        if insert_tipoausencia is None:
            insert_tipoausencia = Modulo(title='Adicionar', route='/tipoausencia_insert',
                                         name='tipoausencia_insert',
                                         menu=False)
        update_tipoausencia = session.query(Modulo).filter(Modulo.name == 'tipoausencia_update').first()
        if update_tipoausencia is None:
            update_tipoausencia = Modulo(title='Actualizar', route='/tipoausencia_update',
                                         name='tipoausencia_update',
                                         menu=False)
        delete_tipoausencia = session.query(Modulo).filter(Modulo.name == 'tipoausencia_delete').first()
        if delete_tipoausencia is None:
            delete_tipoausencia = Modulo(title='Dar de Baja', route='/tipoausencia_delete',
                                         name='tipoausencia_delete',
                                         menu=False)

        imprimir_tipoausencia = session.query(Modulo).filter(Modulo.name == 'tipoausencia_imprimir').first()
        if imprimir_tipoausencia is None:
            imprimir_tipoausencia = Modulo(title='Imprimir', route='/tipoausencia_imprimir',
                                           name='tipoausencia_imprimir',
                                           menu=False)

        tipoausencia_m.children.append(query_tipoausencia)
        tipoausencia_m.children.append(insert_tipoausencia)
        tipoausencia_m.children.append(update_tipoausencia)
        tipoausencia_m.children.append(delete_tipoausencia)
        tipoausencia_m.children.append(imprimir_tipoausencia)

        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(ausencia_m)
        admin_role.modulos.append(permiso_m)
        admin_role.modulos.append(licencia_m)
        admin_role.modulos.append(regularizacion_m)
        admin_role.modulos.append(tipoausencia_m)

        admin_role.modulos.append(query_permiso)
        admin_role.modulos.append(insert_permiso)
        admin_role.modulos.append(update_permiso)
        admin_role.modulos.append(delete_permiso)
        admin_role.modulos.append(imprimir_permiso)
        admin_role.modulos.append(autorizacion_permiso)
        admin_role.modulos.append(aprobacion_permiso)

        admin_role.modulos.append(query_licencia)
        admin_role.modulos.append(insert_licencia)
        admin_role.modulos.append(update_licencia)
        admin_role.modulos.append(delete_licencia)
        admin_role.modulos.append(imprimir_licencia)
        admin_role.modulos.append(autorizacion_licencia)
        admin_role.modulos.append(aprobacion_licencia)

        admin_role.modulos.append(query_regularizacion)
        admin_role.modulos.append(insert_regularizacion)
        admin_role.modulos.append(update_regularizacion)
        admin_role.modulos.append(delete_regularizacion)
        admin_role.modulos.append(imprimir_regularizacion)
        admin_role.modulos.append(autorizacion_regularizacion)
        admin_role.modulos.append(aprobacion_regularizacion)

        admin_role.modulos.append(query_tipoausencia)
        admin_role.modulos.append(insert_tipoausencia)
        admin_role.modulos.append(update_tipoausencia)
        admin_role.modulos.append(delete_tipoausencia)
        admin_role.modulos.append(imprimir_tipoausencia)

        session.commit()

