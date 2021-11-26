from ...configuraciones.sucursal.models import *
from ...operaciones.bitacora.managers import *
from ...dispositivos.marcaciones.models import *
from ...asistencia.asistenciapersonal.managers import AsistenciaManager
from .models import *
from threading import Thread


class LectoresManager(SuperManager):

    def __init__(self, db):
        super().__init__(Lectores, db)

    def ws_listar_dispositivos(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.tipo == "A").all()

    def ws_insertRegistros_biometricos(self, marcaciones):
        for marcacion in marcaciones['marcaciones']:

            marcacion[1] = datetime.strptime(marcacion[1], '%Y-%m-%d %H:%M:%S')

            # print("llegaron marcaciones: " + str(marcacion[1]))

            respuesta = self.db.query(Marcaciones).filter(Marcaciones.time == marcacion[1]).filter(Marcaciones.codigo == marcacion[0]).filter(
                Marcaciones.fkdispositivo == marcaciones['iddispositivo']).first()

            if not respuesta:
                print("registro marcacion")
                dispositivo = LectoresManager(self.db).obtener_dispositivo(marcaciones['iddispositivo'])

                object = Marcaciones(codigo=marcacion[0], time=marcacion[1],
                                     fkdispositivo=marcaciones['iddispositivo'])

                AsistenciaManager(self.db).insertar_marcaciones(marcacion[1], marcacion[0],dispositivo)

                self.db.add(object)

        self.db.commit()
        self.db.close()

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.nombre.asc()).all()

    def obtener_dispositivo(self,id):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.id == id).first()

    def list_all(self):
        return dict(
            objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip_maquina, accion="Registro Lector.",
                     fecha=fecha, tabla="cb_dispositivos_lectores", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip_maquina, accion="Modifico Lector.",
                     fecha=fecha, tabla="cb_dispositivos_lectores", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Lector.", fecha=fecha,
                     tabla="cb_dispositivos_lectores", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def crear_dispositivos(self):
        sucursal = self.db.query(Sucursal).filter(Sucursal.enabled == True).first()
        self.db.add(Lectores(id=1, ip='172.16.12.10', puerto=4370, tipo="A", descripcion='CENTRAL', modelo=''))
        self.db.add(Lectores(id=2, ip='172.16.12.13', puerto=4370, tipo="A", descripcion='SUCURSAL-01', modelo=''))
        self.db.add(Lectores(id=3, ip='172.16.12.16', puerto=4370, tipo="A", descripcion='SUCURSAL-02', modelo=''))
        self.db.add(Lectores(id=4, ip='172.16.12.5', puerto=4370, tipo="A", descripcion='SUCURSAL-04', modelo=''))
        self.db.add(Lectores(id=5, ip='172.16.12.6', puerto=4370, tipo="A", descripcion='SUCURSAL-05', modelo=''))
        self.db.add(Lectores(id=6, ip='172.16.12.4', puerto=4370, tipo="A", descripcion='SUCURSAL-06', modelo=''))
        self.db.add(Lectores(id=7, ip='192.168.0.107', puerto=4370, tipo="A", descripcion='SUCURSAL-07', modelo=''))
        self.db.add(Lectores(id=8, ip='172.16.12.9', puerto=4370, tipo="A", descripcion='SUCURSAL-08', modelo=''))
        self.db.add(Lectores(id=9, ip='192.168.0.109', puerto=4370, tipo="A", descripcion='SUCURSAL-09 (MONTERO)', modelo=''))
        self.db.add(Lectores(id=10, ip='172.16.12.14', puerto=4370, tipo="A", descripcion='SUCURSAL-10', modelo=''))
        self.db.add(Lectores(id=11, ip='172.16.12.18', puerto=4370, tipo="A", descripcion='SUCURSAL-12 (SATELITE)', modelo=''))
        self.db.add(Lectores(id=12, ip='172.16.2.4', puerto=4370, tipo="A", descripcion='SUCURSAL-14', modelo=''))
        self.db.add(Lectores(id=13, ip='172.16.12.11', puerto=4370, tipo="A", descripcion='SUCURSAL-16', modelo=''))
        self.db.add(Lectores(id=14, ip='27.0.0.17', puerto=4370, tipo="A", descripcion='SUCURSAL-17 (SUCRE)', modelo=''))
        self.db.add(Lectores(id=15, ip='13.0.0.70', puerto=4370, tipo="A", descripcion='SUCURSAL-03 (LP)', modelo=''))
        self.db.add(Lectores(id=16, ip='13.0.0.154', puerto=4370, tipo="A", descripcion='SUCURSAL-18 (LP)', modelo=''))
        self.db.add(Lectores(id=17, ip='29.0.0.70', puerto=4370, tipo="A", descripcion='Sucursal-19(Potosi)', modelo=''))
        self.db.add(Lectores(id=18, ip='30.0.0.30', puerto=4370, tipo="A", descripcion='Sucursal 20 Tarija', modelo=''))
        self.db.add(Lectores(id=19, ip='21.0.0.30', puerto=4370, tipo="A", descripcion='Sucursal-11(Tdd)', modelo=''))
        self.db.add(Lectores(id=20, ip='172.16.12.23', puerto=4370, tipo="A", descripcion='Sucursal 31', modelo=''))


        self.db.commit()

    def preparar_dispositivos(self):
        dispositivos = self.db.query(Lectores).filter(Lectores.tipo == "A").filter(Lectores.enabled == True).all()
        print("extraccion de dispositivo")
        for dispositivo in dispositivos:
            # print("inicio del hilo de extraccion")

            # t = Thread(target=self.extraer_marcaciones, args=(dispositivo,))
            # t.start()

            LectoresManager(self.db).extraer_marcaciones(dispositivo)

        self.db.close()

    def extraer_marcaciones(self, dispositivo):
        from zklib import zklib
        try:

            zk = zklib.ZKLib(dispositivo.ip, dispositivo.puerto)
            print('Extrayendo marcaciones Ip: ', dispositivo.ip)
            ret = zk.connect()
            if ret:
                print('Conectado  Ip: ', dispositivo.ip)
                marcaciones = zk.getAttendance()
                print("cantidad de marcaciones: " + str(len(marcaciones)))
                if marcaciones:
                    for marcacion in marcaciones:
                        aux = marcacion[2]

                        query = self.db.query(Marcaciones).filter(Marcaciones.codigo == marcacion[0]).filter(Marcaciones.time == aux).all()
                        if not query:
                            print("marcacion: " + str(aux) + " " + str(dispositivo.ip) + " " + str(marcacion[0]))

                            self.db.add(Marcaciones(time=aux, fkdispositivo=dispositivo.id, codigo=marcacion[0]))
                            AsistenciaManager(self.db).insertar_marcaciones(aux,marcacion[0],dispositivo)
                    # print("cantidad de marcaciones: " + str(len(marcaciones)))
                    print('Inicio del Commit')
                    self.db.commit()

                print('Marcaciones Guardadas Correctamente: ', dispositivo.ip)

                zk.clearAttendance()
                print('Marcaciones Eliminadas del Dispositivo: ', dispositivo.ip)
                zk.getTime()
                zk.enableDevice()
                zk.disconnect()
                print('Terminaron las marcaciones ', dispositivo.ip)
                m = 'Marcaciones Extraidas Correctamente '+ str(dispositivo.ip)
                return dict(estado=True, mensaje=m)
            else:
                print('No se puede conectar con el dispositivo: ', dispositivo.ip)
                m = 'No se puede conectar con el dispositivo ' + str(dispositivo.ip)
                return dict(estado=False, mensaje=m)
        except Exception as e:
            print(e)
            return dict(estado=False, mensaje=str(e))



