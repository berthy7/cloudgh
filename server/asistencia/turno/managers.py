from ...operaciones.bitacora.managers import *
from server.common.managers import SuperManager
from .models import *
import requests


class HoraManager(SuperManager):

    def __init__(self, db):
        super().__init__(Hora, db)


class DiaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Dia, db)

    def litar_todo(self):
        return self.db.query(self.entity)

    def sms(self,telefono,texto):
        destinations = telefono
        message = texto
        senderId = ""
        debug = True

        DiaManager(self.db).altiriaSms(destinations, message, senderId, debug)

        return texto

    def altiriaSms(self,destinations, message, senderId, debug):
        if debug:
            print('Enter altiriaSms: ' + destinations + ', message: ' + message + ', senderId: ' + senderId)

            try:
                # Se crea la lista de parámetros a enviar en la petición POST
                # XX, YY y ZZ se corresponden con los valores de identificación del usuario en el sistema.
                payload = [
                    ('cmd', 'sendsms'),
                    ('domainId', 'demopr'),
                    ('login', 'bvargas@cloudbit.com.bo'),
                    ('passwd', '7fcaxmxb'),
                    # No es posible utilizar el remitente en América pero sí en España y Europa
                    ('senderId', senderId),
                    ('msg', message)
                ]

                # add destinations
                for destination in destinations.split(","):
                    payload.append(('dest', destination))

                # Se fija la codificacion de caracteres de la peticion POST
                contentType = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}

                # Se fija la URL sobre la que enviar la petición POST
                url = 'http://www.altiria.net/api/http'

                # Se envía la petición y se recupera la respuesta
                r = requests.post(url,
                                  data=payload,
                                  headers=contentType,
                                  # Se fija el tiempo máximo de espera para conectar con el servidor (5 segundos)
                                  # Se fija el tiempo máximo de espera de la respuesta del servidor (60 segundos)
                                  timeout=(5, 60))  # timeout(timeout_connect, timeout_read)

                if debug:
                    if str(r.status_code) != '200':  # Error en la respuesta del servidor
                        print('ERROR GENERAL: ' + str(r.status_code))

                    else:  # Se procesa la respuesta
                        print('Código de estado HTTP: ' + str(r.status_code))

                        if (r.text).find("ERROR errNum:"):
                            print('Error de Altiria: ' + r.text)

                        else:
                            print('Cuerpo de la respuesta: \n' + r.text)

                return r.text

            except requests.ConnectTimeout:
                print("Tiempo de conexión agotado")


            except requests.ReadTimeout:
                print("Tiempo de respuesta agotado")


            except Exception as ex:
                print("Error interno: " + str(ex))


    #print('The function altiriaSms returns: \n' + altiriaSms('346xxxxxxxx,346yyyyyyyy', 'Mesaje de prueba', '', True))


    # No es posible utilizar el remitente en América pero sí en España y Europa
    # Utilizar esta llamada solo si se cuenta con un remitente autorizado por Altiria
    # print 'The function altiriaSms returns: \n'+altiriaSms('346xxxxxxxx,346yyyyyyyy','Mesaje de prueba', 'remitente', True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        i = 0
        for x in objeto.hora:
            objeto.hora[i].entrada = datetime.strptime('01/01/2000 '+objeto.hora[i].entrada, '%d/%m/%Y %H:%M')
            objeto.hora[i].salida = datetime.strptime('01/01/2000 '+objeto.hora[i].salida, '%d/%m/%Y %H:%M')
            objeto.hora[i].entradamin = datetime.strptime('01/01/2000 '+objeto.hora[i].entradamin, '%d/%m/%Y %H:%M')
            objeto.hora[i].entradamax = datetime.strptime('01/01/2000 '+objeto.hora[i].entradamax, '%d/%m/%Y %H:%M')
            objeto.hora[i].salidamin = datetime.strptime('01/01/2000 '+objeto.hora[i].salidamin, '%d/%m/%Y %H:%M')
            objeto.hora[i].salidamax = datetime.strptime('01/01/2000 '+objeto.hora[i].salidamax, '%d/%m/%Y %H:%M')
            i = i + 1
        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró un turno.", fecha=fecha, tabla="cb_asistencia_dia", identificador=a.id)
        super().insert(b)

        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        i = 0
        for x in objeto.hora:
            objeto.hora[i].entrada = datetime.strptime('01/01/2000 '+objeto.hora[i].entrada, '%d/%m/%Y %H:%M')
            objeto.hora[i].salida = datetime.strptime('01/01/2000 '+objeto.hora[i].salida, '%d/%m/%Y %H:%M')
            objeto.hora[i].entradamin = datetime.strptime('01/01/2000 '+objeto.hora[i].entradamin, '%d/%m/%Y %H:%M')
            objeto.hora[i].entradamax = datetime.strptime('01/01/2000 '+objeto.hora[i].entradamax, '%d/%m/%Y %H:%M')
            objeto.hora[i].salidamin = datetime.strptime('01/01/2000 '+objeto.hora[i].salidamin, '%d/%m/%Y %H:%M')
            objeto.hora[i].salidamax = datetime.strptime('01/01/2000 '+objeto.hora[i].salidamax, '%d/%m/%Y %H:%M')
            i = i + 1

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó un turno.", fecha=fecha,tabla="cb_asistencia_dia", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó un turno.", fecha=fecha, tabla="cb_asistencia_dia", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

