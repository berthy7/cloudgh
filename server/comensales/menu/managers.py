from ...operaciones.bitacora.managers import *
from sqlalchemy.sql import func
from server.common.managers import SuperManager
from .models import *


class MenuManager(SuperManager):

    def __init__(self, db):
        super().__init__(Menu, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.fecha.desc()).all()

    # def listar_todo(self):
    #     menus =  self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.fecha.desc()).all()
    #     listamenus = list()
    #     for menu in menus:
    #         listaplatos = list()
    #         dicmenu = dict(id=menu.id, nombre=menu.nombre,fecha=menu.fecha.strftime('%d/%m/%Y'),foto=menu.foto,fechadia=menu.fecha.day,fechames=menu.fecha.month)
    #
    #         for platos in menu.menuplato:
    #             listaplatos.append(dict(id=platos.id, fkplato = platos.plato.id, nombreplato = platos.plato.nombre))
    #
    #         dicmenu['platos'] = listaplatos
    #         listamenus.append(dicmenu)
    #
    #     return listamenus


    def menu_dia(self,hoy):
        hoy = datetime.strptime(hoy, '%d/%m/%Y')
        return self.db.query(self.entity).filter(self.entity.fecha == hoy).filter(self.entity.enabled == True).first()

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fecha = datetime.strptime(objeto.fecha, '%d/%m/%Y')

        c = self.db.query(func.count(self.entity.id)).filter(self.entity.fecha == objeto.fecha)\
            .filter(self.entity.enabled == True).scalar()

        if c == 0:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Menu.", fecha=fecha,
                         tabla="rrhh_menu", identificador=a.id)
            super().insert(b)

            return a
        else:
            return False

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fecha = datetime.strptime(objeto.fecha, '%d/%m/%Y')

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Menu.", fecha=fecha,
                     tabla="rrhh_menu", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Menu.", fecha=fecha, tabla="cb_comensales_menu",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def listar_todo_plato(self):
        return self.db.query(Plato).filter(Plato.enabled == True).order_by(Plato.nombre.asc()).all()

    def listar_platos_habilitados(self):
        return self.db.query(Plato).filter(Plato.enabled == True).filter(Plato.estado == True).order_by(Plato.tipo.desc()).all()


    def insert_plato(self, diccionario):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto = Plato(nombre=diccionario['nombre'], tipo=diccionario['tipo'])

        a = super().insert(objeto)
        b = Bitacora(fkusuario=diccionario['user'], ip=diccionario['ip'], accion="Registro Plato.", fecha=fecha,
                     tabla="rrhh_plato", identificador=a.id)
        super().insert(b)
        return a

    def update_plato(self, diccionario):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto = Plato(id =diccionario['id'],nombre=diccionario['nombre'], tipo=diccionario['tipo'])

        a = super().update(objeto)
        b = Bitacora(fkusuario=diccionario['user'], ip=diccionario['ip'], accion="Modifico Plato.", fecha=fecha,
                     tabla="rrhh_plato", identificador=a.id)
        super().insert(b)
        return a

    def delete_plato(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Plato.", fecha=fecha, tabla="rrhh_plato",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def obtener_plato(self, key):
        x = self.db.query(Plato).get(key)
        return x

    def estado_plato(self, id, user, ip, state):
        x = self.db.query(Plato).filter(Plato.id == id).one()
        x.estado = state
        if state:
            mensaje = "Habilito Plato"
        else:
            mensaje = "Deshabilito Plato"

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="cb_comensales_plato", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def listar_plato_dia(self,hoy):
        hoy = datetime.strptime(hoy, '%d/%m/%Y')
        x = self.db.query(Plato).join(Menuplato).join(Menu).filter(Menu.enabled == True).filter(Menu.fecha == hoy).filter(Plato.tipo == "Segundo").order_by(Plato.nombre.asc()).all()

        return x

    def obtener_platos_menu(self,idmenu):
        return self.db.query(Menuplato).filter(Menuplato.enabled == True).filter(Menuplato.fkmenu == idmenu).all()

    def obtener_horarios(self):
        x = self.db.query(HorarioComensal).filter(HorarioComensal.id == 1).first()
        return  x

    def update_horarios(self, objeto,usuario,ip):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=usuario, ip=ip, accion="Modifico hora de comensal.",
                     fecha=fecha, tabla="cb_comensal_horario", identificador=a.id)
        super().insert(b)
        return a