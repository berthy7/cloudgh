from server.common.managers import SuperManager
from ...operaciones.bitacora.managers import BitacoraManager
from ...operaciones.bitacora.models import *
from ...personal.persona.models import *
from ...usuarios.ajustes.models import *
from .models import *
from sqlalchemy.sql import func
from datetime import datetime
from openpyxl import load_workbook
from openpyxl import Workbook

import pytz


class MarcacionesManager(SuperManager):

    def __init__(self, db):
        super().__init__(Marcaciones, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def list_all(self):
        return dict(
            objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def listar_por_dia(self):
        list = {}
        c = 0

        fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha = fecha_zona
        fechahoy = str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)
        fechahoy = datetime.strptime(fechahoy, '%d/%m/%Y')

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(self.entity).filter(func.to_date(self.entity.time).between(fechahoy, fechahoy)).all()
        else:
            # version postgres
            objeto = self.db.query(self.entity).filter(func.date(self.entity.time).between(fechahoy, fechahoy)).all()

        for x in objeto:
            try:
                empleado = self.db.query(Empleado).join(Persona).filter(Empleado.codigo == x.codigo).one()
                nombrepersona = empleado.persona.fullname
            except Exception as ex:
                nombrepersona= "----"

            list[c] = dict(id=x.id,codigo=x.codigo, nombre=nombrepersona, fecha=x.time.strftime("%d/%m/%Y"), hora=x.time.strftime("%H:%M:%S"), dispositivo=x.dispositivo.descripcion)
            c = c + 1

        return list

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip_maquina, accion="Registro Empresa.",
                     fecha=fecha, tabla="rrhh_empresa", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Empresa.",
                     fecha=fecha, tabla="rrhh_empresa", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Empresa.", fecha=fecha,
                     tabla="rrhh_empresa", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def filtrar(self, fechainicio, fechafin):
        list = {}
        c = 0

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(self.entity).filter(func.to_date(self.entity.time).between(fechainicio, fechafin)).order_by(self.entity.id.desc()).all()
        else:
            # version postgres
            objeto = self.db.query(self.entity).filter(func.date(self.entity.time).between(fechainicio, fechafin)).order_by(self.entity.id.desc()).all()

        for x in objeto:
            try:
                empleado = self.db.query(Empleado).join(Persona).filter(Empleado.codigo == x.codigo).one()
                nombrepersona = empleado.persona.fullname
            except Exception as ex:
                nombrepersona= "----"

            list[c] = dict(id=x.id,codigo=x.codigo, nombre=nombrepersona, fecha=x.time.strftime("%d/%m/%Y"), hora=x.time.strftime("%H:%M:%S"), dispositivo=x.dispositivo.descripcion)
            c = c + 1

        return list

    def obtener_marcaciones(self,codigo, fechainicio, fechafin):

        ajuste = self.db.query(Ajustes).filter(Ajustes.enabled == True).first()

        if ajuste.oracle:
            # version oracle
            objeto = self.db.query(self.entity).filter(self.entity.codigo == codigo).filter(func.to_date(self.entity.time).between(fechainicio, fechafin)).order_by(self.entity.id.asc()).all()

        else:
            # version postgres
            objeto = self.db.query(self.entity).filter(self.entity.codigo == codigo).filter(
                func.date(self.entity.time).between(fechainicio, fechafin)).order_by(self.entity.id.asc()).all()

        return objeto

    def importar_excel(self, cname):
        try:
            wb = load_workbook(filename="server/common/resources/uploads/" + cname)
            ws = wb.active
            colnames = ['CODIGO', 'TIME', 'FKDISPOSITIVO']
            indices = {cell[0].value: n - 1 for n, cell in enumerate(ws.iter_cols(min_row=1, max_row=1), start=1) if
                       cell[0].value in colnames}
            if len(indices) == len(colnames):
                for row in ws.iter_rows(min_row=2):
                        time = row[indices['TIME']].value
                        time0 = '01/01/2000 12:00:00'
                        print(str(type(time)) + "longitud: " +str(len(time)))
                        print(str(type(time0)) + "longitud: " +str(len(time0)))

                        time1 = datetime.strptime(time0, '%d/%m/%Y %H:%M:%S')
                        time2 = datetime.strptime(time, '%m/%d/%Y %H:%M:%S')
                        marcaciones = Marcaciones(codigo=row[indices['CODIGO']].value, time=time, fkdispositivo=row[indices['OFFICE']].value)
                        objeto = self.many_to_many(marcaciones)
                        self.db.add(objeto)
                        print(str(marcaciones.codigo) + " "+str(marcaciones.time))

                print("inicio commit")
                self.db.commit()
                print("fin commit")
                return {'message': 'Marcaciones Importadas Correctamente.', 'success': True}
            else:
                return {'message': 'Columnas Faltantes', 'success': False}
        except Exception as e:
            print(e)
            return {'message': 'Error', 'success': False}