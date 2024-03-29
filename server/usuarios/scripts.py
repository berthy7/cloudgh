import hashlib
from server.database.connection import transaction
from .usuario.models import Modulo, Usuario
from .rol.models import Rol
from .ajustes.models import Ajustes
from datetime import datetime


def insertions():
    with transaction() as session:
        user_m = session.query(Modulo).filter(Modulo.name == 'user_Modulo').first()
        if user_m is None:
            user_m = Modulo(title='Usuarios', name='user_Modulo', icon='usuarios.png')

        roles_m = session.query(Modulo).filter(Modulo.name == 'roles').first()
        if roles_m is None:
            roles_m = Modulo(title='Rol', route='/rol', name='roles', icon='rol.png')

        usuarios_m = session.query(Modulo).filter(Modulo.name == 'usuario').first()
        if usuarios_m is None:
            usuarios_m = Modulo(title='Usuario', route='/usuario', name='usuario', icon='usuario.png')

        perfil_m = session.query(Modulo).filter(Modulo.name == 'perfil').first()
        if perfil_m is None:
            perfil_m = Modulo(title='Perfil Usuario', route='/usuario_profile', name='perfil', icon='usuario.ico')

        bitacora_m = session.query(Modulo).filter(Modulo.name == 'bitacora').first()
        if bitacora_m is None:
            bitacora_m = Modulo(title='Bitácora', route='/bitacora', name='bitacora', icon='bitacora.png')

        ajustes_m = session.query(Modulo).filter(Modulo.name == 'bitacora').first()
        if ajustes_m is None:
            ajustes_m = Modulo(title='Ajustes de Sistema', route='/ajustes', name='ajustes', icon='ajustes.png')

        user_m.children.append(roles_m)
        user_m.children.append(usuarios_m)
        user_m.children.append(perfil_m)
        user_m.children.append(bitacora_m)
        user_m.children.append(ajustes_m)

        query_rol = session.query(Modulo).filter(Modulo.name == 'rol_query').first()
        if query_rol is None:
            query_rol = Modulo(title='Consultar', route='', name='rol_query', menu=False)
        insert_rol = session.query(Modulo).filter(Modulo.name == 'rol_insert').first()
        if insert_rol is None:
            insert_rol = Modulo(title='Adicionar', route='/rol_insert', name='rol_insert', menu=False)
        update_rol = session.query(Modulo).filter(Modulo.name == 'rol_update').first()
        if update_rol is None:
            update_rol = Modulo(title='Actualizar', route='/rol_update', name='rol_update', menu=False)
        delete_rol = session.query(Modulo).filter(Modulo.name == 'rol_delete').first()
        if delete_rol is None:
            delete_rol = Modulo(title='Dar de Baja', route='/rol_delete', name='rol_delete', menu=False)

        roles_m.children.append(query_rol)
        roles_m.children.append(insert_rol)
        roles_m.children.append(update_rol)
        roles_m.children.append(delete_rol)

        query_usuario = session.query(Modulo).filter(Modulo.name == 'usuario_query').first()
        if query_usuario is None:
            query_usuario = Modulo(title='Consultar', route='', name='usuario_query', menu=False)
        insert_usuario = session.query(Modulo).filter(Modulo.name == 'usuario_insert').first()
        if insert_usuario is None:
            insert_usuario = Modulo(title='Adicionar', route='/usuario_insert', name='usuario_insert', menu=False)
        update_usuario = session.query(Modulo).filter(Modulo.name == 'usuario_update').first()
        if update_usuario is None:
            update_usuario = Modulo(title='Actualizar', route='/usuario_update', name='usuario_update', menu=False)
        delete_usuario = session.query(Modulo).filter(Modulo.name == 'usuario_delete').first()
        if delete_usuario is None:
            delete_usuario = Modulo(title='Dar de Baja', route='/usuario_delete', name='usuario_delete', menu=False)

        usuarios_m.children.append(query_usuario)
        usuarios_m.children.append(insert_usuario)
        usuarios_m.children.append(update_usuario)
        usuarios_m.children.append(delete_usuario)

        query_bitacora = session.query(Modulo).filter(Modulo.name == 'bitacora_query').first()
        if query_bitacora is None:
            query_bitacora = Modulo(title='Consultar', route='', name='bitacora_query', menu=False)

        bitacora_m.children.append(query_bitacora)

        query_ajustes = session.query(Modulo).filter(Modulo.name == 'ajustes_query').first()
        if query_ajustes is None:
            query_ajustes = Modulo(title='Consultar', route='', name='ajustes_query', menu=False)

        update_ajustes = session.query(Modulo).filter(Modulo.name == 'ajustes_update').first()
        if update_ajustes is None:
            update_ajustes = Modulo(title='Actualizar', route='/ajustes_update', name='ajustes_update', menu=False)


        ajustes_m.children.append(query_ajustes)
        ajustes_m.children.append(update_ajustes)


        admin_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()
        if admin_role is None:
            admin_role = Rol(id= 1,nombre='SUPER ADMINISTRADOR', descripcion='Todos los permisos')

        personal_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        if personal_role is None:
            personal_role = Rol(id= 2,nombre='ADMINISTRADOR', descripcion='permisos del sistema')


        ###Modulo de Usuarios
        admin_role.modulos.append(user_m)
        admin_role.modulos.append(roles_m)
        admin_role.modulos.append(usuarios_m)
        admin_role.modulos.append(perfil_m)
        admin_role.modulos.append(bitacora_m)
        admin_role.modulos.append(ajustes_m)
        admin_role.modulos.append(query_usuario)
        admin_role.modulos.append(insert_usuario)
        admin_role.modulos.append(update_usuario)
        admin_role.modulos.append(delete_usuario)
        admin_role.modulos.append(query_rol)
        admin_role.modulos.append(insert_rol)
        admin_role.modulos.append(update_rol)
        admin_role.modulos.append(delete_rol)
        admin_role.modulos.append(query_bitacora)
        admin_role.modulos.append(query_ajustes)
        admin_role.modulos.append(update_ajustes)

        super_user = session.query(Usuario).filter(Usuario.username == 'admin').first()
        if super_user is None:
            hex_dig = hashlib.sha512(b'Cloudgh2021').hexdigest()
            super_user = Usuario(username='admin', password=hex_dig,autenticacion=False)
            super_user.rol = admin_role

        ajustes = Ajustes(id=1,dominio='' ,mysql=True, postgres=False,oracle=False, sqlserver=False, enabled=True,iniciohoranocturno=datetime.strptime('01/01/2000 20:00' , '%d/%m/%Y %H:%M'),finhoranocturno=datetime.strptime('01/01/2000 20:00' , '%d/%m/%Y %H:%M'),porcentajehoranocturno=30)

        session.add(ajustes)
        session.add(super_user)
        session.add(admin_role)
        session.add(personal_role)

        session.commit()
