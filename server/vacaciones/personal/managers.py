from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *
from sqlalchemy.exc import IntegrityError
from ...personal.persona.models import *
from ..historico.models import *
from sqlalchemy.sql import func

from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Font


class V_personalManager(SuperManager):

    def __init__(self, db):
        super().__init__(V_personal, db)


    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def obtener_x_personal(self,fkpersona):
        return self.db.query(self.entity).filter(self.entity.fkpersona == fkpersona).first()

    def listar_x_ciudad(self, idciudad):
        return self.db.query(self.entity).filter(self.entity.fkciudad == idciudad).filter(
            self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro V_personal.",
                     fecha=fecha, tabla="rrhh_sucursal", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico V_personal.",
                     fecha=fecha, tabla="rrhh_sucursal", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó V_personal.", fecha=fecha,
                     tabla="rrhh_sucursal", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def importar_excel(self, cname, user, ip):
        try:
            wb = load_workbook(filename="server/common/resources/uploads/" + cname)
            ws = wb.active
            colnames = ['CODIGO', 'NOMBRE','APELLIDO_P', 'APELLIDO_M','DIAS_VACACION']
            indices = {cell[0].value: n - 1 for n, cell in enumerate(ws.iter_cols(min_row=1, max_row=1), start=1) if
                       cell[0].value in colnames}
            if len(indices) == len(colnames):
                for row in ws.iter_rows(min_row=2):
                    codigo = row[indices['CODIGO']].value
                    dias_vacacion = row[indices['DIAS_VACACION']].value

                    if codigo is not None and dias_vacacion is not None:

                        query_v_personal = self.db.query(V_personal).join(Persona).join(Empleado).filter(Empleado.codigo == str(codigo)).first()
                        if not query_v_personal:

                            query = self.db.query(Persona).join(Empleado).filter(Empleado.codigo == str(codigo)).first()

                            if query:
                                fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))
                                histori = V_historico(fkpersona=query.id, dias=dias_vacacion,descripcion="Importacion Excel",operacion="+",fecha=fecha_zona)

                                self.db.add(histori)
                                self.db.flush()

                                personal = V_personal(fkpersona=query.id, dias=dias_vacacion)
                                self.db.add(personal)
                                self.db.flush()
                    else:
                        self.db.rollback()
                        return {'message': 'Hay Columnas vacias', 'success': False}

                self.db.commit()

                return {'message': 'Importado Todos Correctamente.', 'success': True}
            else:
                return {'message': 'Columnas Faltantes', 'success': False}
        except IntegrityError as e:
            self.db.rollback()
            if 'UNIQUE constraint failed: rrhh_persona.dni' in str(e):
                return {'message': 'CI duplicado', 'success': False}
            if 'UNIQUE constraint failed: rrhh_empleado.codigo' in str(e):
                return {'message': 'codigo de empleado duplicado', 'success': False}
            return {'message': str(e), 'success': False}

    def actualizar_nro_vacacion(self, fkpersona,dias,operacion,user,ip):
        v_personal = self.db.query(V_personal).filter(V_personal.fkpersona == fkpersona).first()
        total_dias = 0
        accion = ""
        if operacion =="+":
            total_dias = (v_personal.dias) + int(dias)
            accion = "agrego dias de vacaciones"

        elif operacion == "-":
            total_dias = (v_personal.dias) - int(dias)
            accion = "resto dias de vacaciones"

        if total_dias !=0:
            fecha_vacacion = datetime.now(pytz.timezone('America/La_Paz'))
            v_personal.dias = total_dias
            self.db.merge(v_personal)
            self.db.commit()

            b = Bitacora(fkusuario=user, ip=ip, accion=accion, fecha=fecha_vacacion,
                         tabla="cb_vacaciones_personal", identificador=v_personal.id)
            super().insert(b)

    def disponibilidad(self, fkpersona,fechai,fechaf):
        fechai = datetime.strptime(fechai, '%d/%m/%Y')
        fechaf = datetime.strptime(fechaf, '%d/%m/%Y')

        cant_dias = BitacoraManager(self.db).obtener_cant_dias(fechai,fechaf)
        n = self.db.query(V_personal).filter(V_personal.fkpersona == fkpersona).first()

        if n:
            if n.dias != 0:
                if cant_dias <= n.dias:

                    return dict(mensaje="", respuesta=True,tipo="")
                else:

                    return dict(mensaje="Tiene "+ str(n.dias) +" dias", respuesta=False, tipo="warning")

            else:

                return dict(mensaje="Tiene 0 dias", respuesta=False,tipo="warning")
        else:
                return dict(mensaje="No tiene vacacion disponible", respuesta=False,tipo="error")

