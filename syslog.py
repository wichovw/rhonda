# -*- coding: utf-8 -*-
"""
Created on Sat May 16 10:04:05 2015
Inicializa los servicios para manejar el log

@author: Kappa
"""
from logging.handlers import SysLogHandler
from logging import *


def agregar_log_syslog( nombre_programa, direccion, puerto=514  ):
    """
    Agrega la opcion de utilizar syslog.
    :param direccion: Direccion del servidor de syslog
    :param puerto: Puerto del syslog
    :return:
    """
    formatter = Formatter('%(asctime)s ' + nombre_programa + ': <%(levelname)s> %(message)s', datefmt='%b %d %H:%M:%S')

    logger = getLogger()
    handler_syslog = SysLogHandler( address=( direccion, puerto ) )
    handler_syslog.setLevel(DEBUG)
    handler_syslog.setFormatter( formatter )

    logger.addHandler( handler_syslog )
    logger.setLevel(DEBUG)


def agregar_log_archivo( nombre_archivo = "Log.log",  formatter=Formatter( '%(asctime)s <%(levelname)s>: %(message)s' ), borrar=True ):
    """
    Agrega la opcion de utilizar un archivo para logging.
    :param nombre_archivo:
    :return:
    """

    # Intenta borrar el archivo
    if borrar:
        with open(nombre_archivo, "w"):
            pass

    handler_archivo = FileHandler( nombre_archivo )
    handler_archivo.setFormatter( formatter )
    handler_archivo.setLevel(DEBUG)

    logger = getLogger()
    logger.setLevel(DEBUG)
    logger.addHandler( handler_archivo )


def agregar_log_consola( formatter=Formatter('%(asctime)s <%(levelname)s>: %(message)s') ):
    """
    Agrega la opcion de utilizar la consola para logging.
    :param formatter:
    :param nombre_logger:
    :return:
    """
    handler_consola = StreamHandler()
    handler_consola.setLevel(DEBUG)
    handler_consola.setFormatter( formatter )

    logger = getLogger()
    logger.setLevel(DEBUG)
    logger.addHandler( handler_consola )


### PRUEBAS ###
if __name__ == "__main__":
    # Agrega los logs
    agregar_log_archivo("Log_Prueba.log")
    agregar_log_consola()
    agregar_log_syslog( "Rhonda", "54.149.245.1")

    # Mensajes
    debug("Debug")
    info("Info")
    error("Error")
    warn("Warning")
    fatal("Fatal")
    critical("Critical")