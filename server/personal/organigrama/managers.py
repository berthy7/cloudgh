from .models import *
from ...configuraciones.cargo.managers import *
from ...configuraciones.ciudad.managers import *
from ...configuraciones.empresa.models import *

from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Font


class OrganigramaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Organigrama, db)

    def list_all(self):
        return dict(objects=self.db.query(Organigrama).filter(Organigrama.enabled is True))

    def list_son(self):
        listaID=self.list_all()
        listaHijos=list()
        listaFK=self.list_all()
        fks=list()
        for lid in listaID:
            fks.append(lid.fkpadre)
        for lfk in listaFK:
            if lfk.id not in fks:
                listaHijos.append(lfk)
        return listaHijos

    def get_brother(self, fkpadre, id):
        return dict(contador_bro=self.db.query(self.entity).filter(self.entity.enabled == True).\
            filter(self.entity.fkpadre == fkpadre).count(), contador_son=self.db.query(self.entity).filter(self.entity.enabled == True).\
            filter(self.entity.fkpadre == id).count())

    def get_all(self):
        query = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkpadre == None).first()
        s = self.order_tree(query)
        return s

    def order_tree(self, tree):
        tree2 = tree
        return self.order_tree_pri(tree, dict(), tree2)

    def order_tree_pri(self, tree, item, item_tree):
        if tree:
            # rs = tree.pop()
            if tree.fkcargo:
                cargo = tree.cargo.nombre
            else:
                empresa = self.db.query(Empresa).filter(Empresa.enabled == True).first()
                if empresa:
                    cargo = empresa.nombre
                else:
                    cargo = "Por Definir"

            if tree.fkpersona:
                persona = tree.persona.fullname
            else:
                persona = ""

            item = dict(id=tree.id, name=cargo, title=persona, fk_parent='', children=[])
            for h in tree.hijos:

                h_copia = h
                item_hijos = self.order_tree_pri(h, item['children'],  h_copia)
                item['children'].append(item_hijos)

            return item
        else:
            return item

    def checked_object_position(self,pos,fkpadre):
        return self.db.query(self.entity).filter(self.entity.fkpadre==fkpadre).filter(self.entity.siguiente==pos).first()

    def update(self, object):
        pos = self.checked_object_position(object.siguiente,object.fkpadre)
        obj = self.obtain(object.id)
        if pos is not None:
            pos.siguiente = obj.siguiente
            super().update(pos)
        return super().update(object)


    def obtener_superior(self,fkpersona):

        # Obtener Superior del Organigrama
        x = self.db.query(self.entity).filter(self.entity.fkpersona==fkpersona).first()
        
        #Si no hay Superior de 'x', devolver None
        if(x is None):
            return None
        # Obtener Padre
        padre = self.db.query(self.entity).filter(self.entity.id == x.fkpadre).first()

        return padre.fkpersona

    # def get_all(self):
    #     return self.db.query(self.entity).filter(self.entity.enabled == True).all()
    #
    # def list_all(self):
    #     return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))
    #
    # def listar_todo(self):
    #     return self.db.query(self.entity).filter(self.entity.enabled == True)
    #
    # def insert(self, objeto):
    #     fecha = BitacoraManager(self.db).fecha_actual()
    #
    #     a = super().insert(objeto)
    #     b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Organigrama.", fecha=fecha,tabla="rrhh_organigrama", identificador=a.id)
    #     super().insert(b)
    #
    #     return a
    #
    # def update(self, objeto):
    #     fecha = BitacoraManager(self.db).fecha_actual()
    #
    #     a = super().update(objeto)
    #     b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Organigrama.", fecha=fecha,tabla="rrhh_organigrama", identificador=a.id)
    #     super().insert(b)
    #     return a
    #
    # def delete(self, id, user, ip):
    #     x = self.db.query(self.entity).filter(self.entity.id == id).one()
    #     x.enabled = False
    #     fecha = BitacoraManager(self.db).fecha_actual()
    #     b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Organigrama.", fecha=fecha,tabla="rrhh_organigrama", identificador=id)
    #     super().insert(b)
    #     a = self.db.merge(x)
    #     self.db.commit()
    #     return a
