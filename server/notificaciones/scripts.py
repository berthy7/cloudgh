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

        notificaciones_m = session.query(Modulo).filter(Modulo.name == 'notificaciones').first()
        if notificaciones_m is None:
            notificaciones_m = Modulo(title='Notificaciones', name='notificaciones', icon='notificaciones.png')

        correo_m = session.query(Modulo).filter(Modulo.name == 'correo').first()
        if correo_m is None:
            correo_m = Modulo(title='Envio de Correos ', route='/correo', name='correo', icon='correo.png')

        correo_rrhh_m = session.query(Modulo).filter(Modulo.name == 'correo').first()
        if correo_rrhh_m is None:
            correo_rrhh_m = Modulo(title='Correos de RRHH ', route='/correo_rrhh', name='correo_rrhh', icon='correorrhh.png')

        notificaciones_m.children.append(correo_m)
        notificaciones_m.children.append(correo_rrhh_m)

        query_correo = session.query(Modulo).filter(Modulo.name == 'correo_query').first()
        if query_correo is None:
            query_correo = Modulo(title='Consultar', route='',
                                 name='correo_query',
                                 menu=False)

        insert_correo = session.query(Modulo).filter(Modulo.name == 'correo_insert').first()
        if insert_correo is None:
            insert_correo = Modulo(title='Adicionar', route='/correo_insert',
                                  name='correo_insert',
                                  menu=False)
        update_correo = session.query(Modulo).filter(Modulo.name == 'correo_update').first()
        if update_correo is None:
            update_correo = Modulo(title='Actualizar', route='/correo_update',
                                  name='correo_update',
                                  menu=False)
        delete_correo = session.query(Modulo).filter(Modulo.name == 'correo_delete').first()
        if delete_correo is None:
            delete_correo = Modulo(title='Dar de Baja', route='/correo_delete',
                                  name='correo_delete',
                                  menu=False)

        imprimir_correo = session.query(Modulo).filter(Modulo.name == 'correo_imprimir').first()
        if imprimir_correo is None:
            imprimir_correo = Modulo(title='Imprimir', route='/correo_imprimir',
                                    name='correo_imprimir',
                                    menu=False)

        correo_m.children.append(query_correo)
        correo_m.children.append(insert_correo)
        correo_m.children.append(update_correo)
        correo_m.children.append(delete_correo)
        correo_m.children.append(imprimir_correo)

        query_correo_rrhh = session.query(Modulo).filter(Modulo.name == 'correo_rrhh_query').first()
        if query_correo_rrhh is None:
            query_correo_rrhh = Modulo(title='Consultar', route='',
                                 name='correo_rrhh_query',
                                 menu=False)

        insert_correo_rrhh = session.query(Modulo).filter(Modulo.name == 'correo_rrhh_insert').first()
        if insert_correo_rrhh is None:
            insert_correo_rrhh = Modulo(title='Adicionar', route='/correo_rrhh_insert',
                                  name='correo_rrhh_insert',
                                  menu=False)
        update_correo_rrhh = session.query(Modulo).filter(Modulo.name == 'correo_rrhh_update').first()
        if update_correo_rrhh is None:
            update_correo_rrhh = Modulo(title='Actualizar', route='/correo_rrhh_update',
                                  name='correo_rrhh_update',
                                  menu=False)
        delete_correo_rrhh = session.query(Modulo).filter(Modulo.name == 'correo_rrhh_delete').first()
        if delete_correo_rrhh is None:
            delete_correo_rrhh = Modulo(title='Dar de Baja', route='/correo_rrhh_delete',
                                  name='correo_rrhh_delete',
                                  menu=False)

        imprimir_correo_rrhh = session.query(Modulo).filter(Modulo.name == 'correo_rrhh_imprimir').first()
        if imprimir_correo_rrhh is None:
            imprimir_correo_rrhh = Modulo(title='Imprimir', route='/correo_rrhh_imprimir',
                                    name='correo_rrhh_imprimir',
                                    menu=False)

        correo_rrhh_m.children.append(query_correo_rrhh)
        correo_rrhh_m.children.append(insert_correo_rrhh)
        correo_rrhh_m.children.append(update_correo_rrhh)
        correo_rrhh_m.children.append(delete_correo_rrhh)
        correo_rrhh_m.children.append(imprimir_correo_rrhh)

        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(notificaciones_m)
        admin_role.modulos.append(correo_m)
        admin_role.modulos.append(correo_rrhh_m)

        admin_role.modulos.append(query_correo)
        admin_role.modulos.append(insert_correo)
        admin_role.modulos.append(update_correo)
        admin_role.modulos.append(delete_correo)
        admin_role.modulos.append(imprimir_correo)

        admin_role.modulos.append(query_correo_rrhh)
        admin_role.modulos.append(insert_correo_rrhh)
        admin_role.modulos.append(update_correo_rrhh)
        admin_role.modulos.append(delete_correo_rrhh)
        admin_role.modulos.append(imprimir_correo_rrhh)

        # servidor = ServidorCorreo(id=1,servidor='webmail.cloudbit.com.bo' ,puerto='537', correo='devcloudbit@gmail.com'
        #                           ,password='5398617acm', hora=datetime.strptime('01/01/2000 10:00', '%d/%m/%Y %H:%M'), enabled=True)

        servidor = ServidorCorreo(id=1, servidor='smtp.gmail.com', puerto='587', correo='notificacioncloudgh@gmail.com'
                                  , password='Cloudbit2020', hora=datetime.strptime('01/01/2000 10:00', '%d/%m/%Y %H:%M'),
                                  enabled=True)

        session.add(servidor)

        session.commit()


def notificaciones_schedule():

    def correo_reporte():
        with transaction() as db:
            fecha_actual = datetime.now(pytz.timezone('America/La_Paz'))
            servidor = CorreoManager(db).obtener_servidor()

            hora_actual = fecha_actual.strftime("%H:%M")
            hora_correo = servidor.hora.strftime("%H:%M")

            if hora_actual == hora_correo:
                CorreoManager(db).envio_reporte_correo()

    schedule.every(1).minutes.do(correo_reporte)





