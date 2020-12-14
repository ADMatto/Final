

# 1) Deberá tener un menú principal con las acciones disponibles -listo-
# 2) Permitir la búsqueda de un cliente por su nombre (parcial o total) , mostrando todos sus datos. -listo-
# 3) Permitir obtener el total de usuarios por empresa, y todos sus datos. -listo-
# 4) Permitir obtener el total de dinero en viajes por nombre de empresa. -listo-
# 5) Permitir obtener cantidad total de viajes realizados y monto total por documento,
# y mostrar los datos del empleado y los viajes. -listo-
# 6) Además se requiere que el sistema guarde las consultas en un archivo .log. -listo-

""" El csv que se cargue se considerará válido si:
Documento tiene entre 7 y 8 caracteres numéricos de largo
No hay campos vacios
Email contiene un @ y un .
Precio contiene dos decimales"""

import csv
import os
import re
import shutil


def validar_archivo_clientes(archivo="clientes.csv"):
    errores_docum = 0
    errores_vacio = 0
    errores_correo = 0
    lista_errores = []
    try:
        with open(archivo, encoding="utf8") as datos:
            reader = csv.DictReader(datos)
            campos = reader.fieldnames
            for nro, fila in enumerate(reader):
                for campo in campos:
                    if fila[campo] == '':
                        errores_vacio += 1
                    elif campo == 'Documento':
                        try:
                            int(fila['Documento'])
                            if len(fila['Documento']) == 7 or len(fila['Documento']) == 8:
                                pass
                            else:
                                lista_errores.append([nro+1, campo, fila[campo]])
                                errores_docum += 1
                        except ValueError:
                            lista_errores.append([nro+1, campo, fila[campo]])
                            errores_docum += 1
                    if campo == 'Correo Electrónico':
                        if re.match(r'.*@.*\..*', fila[campo]):
                            pass
                        else:
                            lista_errores.append([nro+1, campo, fila[campo]])
                            errores_correo += 1
    except IOError:
        print("El archivo que desea abrir, no existe o está corrupto!")
        return False
    if len(lista_errores) > 1:
        print(f"Se encontraron {errores_docum + errores_vacio} errores en el documento '{archivo}':")
    elif not lista_errores:
        print(f"No se encontraron errores en el archivo {archivo}")
        return True
    else:
        print(f"Se encontró {errores_docum + errores_vacio} error en el documento {archivo}:")
    for elemento in lista_errores:
        print(f"    Fila: {elemento[0]}, Campo: {elemento[1]}, Valor: {elemento[2]}")
    return False


def validar_archivo_viajes(archivo="viajes.csv"):
    errores_monto = 0
    lista_errores = []
    try:
        with open(archivo, encoding="utf8") as datos:
            reader = csv.DictReader(datos)
            for nro, fila in enumerate(reader):
                if re.match(r'\d*\.\d{2}', fila['monto']):
                    pass
                else:
                    lista_errores.append([nro+2, fila['monto']])
                    errores_monto += 1
    except IOError:
        print("El archivo que desea abrir, no existe o está corrupto!")
    if not lista_errores:
        print(f"No se encontraron errores en el archivo {archivo}")
        return True
    print(f"Se encontraron {errores_monto} errores del campo 'monto' en el archivo '{archivo}'")
    for elemento in lista_errores:
        print(f"    Fila: {elemento[0]}, Valor: {elemento[1]}")
    print("---------------------------------------------------")


def leer_archivo(archivo, campo='', buscar=''):

    lista = []
    fila_anterior = []
    check = 0
    try:

        with open(archivo, encoding="utf8") as datos:
            reader = csv.DictReader(datos)
            if buscar != '':
                lista.append(reader.fieldnames)
            else:
                lista.append(campo)
            for fila in reader:
                if buscar == '':
                    if fila_anterior != fila[campo]:
                        lista.append(fila[campo])
                        fila_anterior = fila[campo]
                elif campo == "Empresa":
                    if str(buscar) in fila[campo]:
                        lista.append(list(fila.values()))
                else:
                    filtros = str(buscar).split()

                    for filtro in filtros:
                        if str(filtro) in fila[campo].lower():
                            check += 1
                    if check == len(filtros):
                        lista.append(list(fila.values()))
                    check = 0
            return lista

    except IOError:

        print('Hubo un error al abrir el archivo!')


def validacion_opciones(cantidad):
    while True:
        try:
            opcion = int(input('Opcion: '))
            if 0 < opcion <= cantidad:
                break
        except ValueError:
            pass
    return opcion


def menu_opciones():
    resultados = leer_archivo("clientes.csv", "Empresa")
    for index, elemento in enumerate(resultados):
        if index == 0:
            print(elemento)
        else:
            print(f"{index}) {elemento}")
    opcion = validacion_opciones(len(resultados)-1)
    total_clientes = leer_archivo("clientes.csv", "Empresa", resultados[opcion])
    return resultados[opcion], total_clientes

def total_usuarios():

    empresa, total_clientes = menu_opciones()
    print(f"---------------------------------------\n"
          f"Empresa: {empresa}\n"
          f"Total Usuarios: {len(total_clientes)-1}\n"
          f"---------------------------------------")
    for elemento in total_clientes:
        print(elemento)
    input('\nPresione [Enter] para continuar...')


def total_monto():

    total = 0
    empresa, total_clientes = menu_opciones()
    total_clientes = leer_archivo("clientes.csv", "Empresa", empresa)
    for cliente in total_clientes:
        if cliente != total_clientes[0]:
            suma, _, _ = total_viajes(cliente[2])
            total += suma
    return total, empresa


def total_viajes(documento):
    suma = 0
    resultados = leer_archivo("viajes.csv", "Documento", documento)
    if len(resultados) != 1:
        for elemento in resultados:
            if elemento[0] == "Documento":
                pass
            else:
                try:
                    suma += float(elemento[2])
                except ValueError:
                    suma += float(elemento[2].replace(',', ''))

    else:
        pass
    return suma, len(resultados)-1, resultados

def remplazar_archivo(archivo):
    valido = False
    archivo_nuevo = input('Ingrese el nombre del nuevo archivo: ')
    if archivo == "clientes.csv":
        valido = validar_archivo_clientes(archivo_nuevo)
    elif archivo == "viajes.csv":
        valido = validar_archivo_viajes(archivo_nuevo)
    if valido:
        print("El archivo es valido para utilizar!")
        respuesta = input("Hacer una copia de seguridad del archivo actual y remplazarlo por este? "
                          "('ok' para confirmar): ")
        if respuesta.lower() == 'ok':
            with open(archivo, 'rb') as origen:
                with open("old_"+archivo, 'wb') as destino:
                    shutil.copyfileobj(origen, destino)
                    print(f"Backup de {archivo} creado!")
            with open(archivo_nuevo, 'rb') as origen:
                with open(archivo, 'wb') as destino:
                    shutil.copyfileobj(origen, destino)
                    print(f"Se remplazo {archivo}")
            input('\nPresione [Enter] para continuar...')

    else:
        print("El archivo tiene errores, no es valido!")

def menu():
    backlog = ['------Log------']
    # falta manejar errores
    os.system('cls')
    while True:

        print('Bienvenido a Radio Taxi "El Papu"\n'
              'Seleccione una opcion:\n'
              ' 1) Buscar cliente\n'
              ' 2) Total de Usuarios por empresa\n'
              ' 3) Total de dinero por empresa\n'
              ' 4) Cantidad total de viajes y monto gastado\n'
              ' 5) Salir\n'
              ' 6) Subir nuevos archivos')

        opcion = validacion_opciones(6)
        if opcion == 1:

            nombre = input("Ingrese el nombre del cliente: ").lower()
            resultados = leer_archivo("clientes.csv", "Nombre", nombre)
            if len(resultados) != 1:

                print(f"---------------Resultados para Nombre: {nombre} ----------------")
                for elemento in resultados:
                    print(elemento)
            else:
                print(f"No se encontraron registros con '{nombre}'")
            input('\nPresione [Enter] para continuar...')

            backlog.append('Buscar Cliente')

        elif opcion == 2:

            total_usuarios()
            backlog.append('Total de Usuarios')

        elif opcion == 3:

            total, empresa = total_monto()
            print("-------------------------------------------\n"
                  f"{empresa}: ${total}\n"
                  "-------------------------------------------")

            input('\nPresione [Enter] para continuar...')
            backlog.append('Monto Total')

        elif opcion == 4:

            while True:
                try:
                    documento = int(input("Ingrese el documento: "))
                    cifras = len(str(documento))
                    if cifras == 7 or cifras == 8:
                        break
                    print("El documento debe ser un numero de 7 o 8 cifras.")
                except ValueError:
                    print("El documento debe ser un numero de 7 o 8 cifras.")

            print(f"------------------------------------------\n"
                  f"Documento: {documento}\n"
                  f"------------------------------------------")
            lista = leer_archivo("clientes.csv", "Documento", str(documento))
            if len(lista) != 1:
                for elemento in lista:
                    print(elemento)
                suma, cantidad, lista = total_viajes(documento)
                print(f"------------------------------------------\n"
                      f"Total Viajes: {cantidad}, Monto Total: {suma}\n"
                      f"--------Viajes--------")
                for elemento in lista:
                    if elemento == lista[0]:
                        print(f"  {elemento[1].upper()}    |  {elemento[2].upper()}")
                    else:
                        print(f"{elemento[1].upper()} |  {elemento[2].upper()}")
            else:
                print(f"No se encontraron registros para el documento {documento}")
            input('\nPresione [Enter] para continuar...')
            backlog.append('Cantidad de viajes y monto total')

        elif opcion == 5:
            with open("ejecuciones.log", "w") as log:
                for accion in backlog:
                    log.writelines(accion + "\n")
            print('Backlog creado: "ejecuciones.log"')
            print('Cerrando programa...')
            return

        elif opcion == 6:
            backlog.append('Cambio y verificacion de Archivos')
            print('Seleccione una opcion:\n'
                  '1) Cambiar archivo clientes.csv\n'
                  '2) Cambiar archivo viajes.csv\n'
                  '3) Validar archivos\n'
                  '4) Volver')
            opcion_archivos = validacion_opciones(4)
            if opcion_archivos == 1:
                remplazar_archivo("clientes.csv")
            elif opcion_archivos == 2:
                remplazar_archivo("viajes.csv")
            elif opcion_archivos == 3:
                validar_archivo_viajes()
                validar_archivo_clientes()
                input('\nPresione [Enter] para continuar...')
            else:
                print("Accion cancelada!")

        os.system('cls')


menu()
