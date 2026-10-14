from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# 1. Importamos TODOS los controladores
from views import (
    ClienteController, VendedorController, ProductoController, 
    VentaController, PagoController
)

# =====================================================================
# INYECCIÓN DE DEPENDENCIAS (Conectamos los controladores entre sí)
# =====================================================================
clientes = ClienteController()
vendedores = VendedorController()
productos = ProductoController()

# La Venta necesita conocer a los clientes, vendedores y productos
ventas = VentaController(clientes, vendedores, productos)

# El Pago necesita conocer a la venta para validar totales y duplicados
pagos = PagoController(ventas)


# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================

def pausa():
    input("\nPresione Enter para continuar...")

def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        return None

def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

def mostrar_lista(objetos, vacio="No hay registros todavía."):
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")

def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENÚ DE CLIENTES
# =====================================================================

def crear_cliente():
    imprimir_titulo("CREAR CLIENTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "telefono": input("Teléfono: "),
        "ciudad": input("Ciudad: "),
    }
    mostrar_resultado(*clientes.crear(datos))
    pausa()

def listar_clientes():
    imprimir_titulo("CLIENTES")
    mostrar_lista(clientes.leer(), "Todavía no hay clientes.")
    pausa()

def buscar_cliente():
    imprimir_titulo("BUSCAR CLIENTE")
    termino = input("Nombre, email, teléfono o ciudad: ")
    encontrados = clientes.buscar(termino)
    mostrar_lista(encontrados, f"Ningún cliente coincide con '{termino}'.")
    pausa()

def ver_cliente():
    imprimir_titulo("VER CLIENTE POR ID")
    cliente = clientes.obtener(pedir_entero("Id: "))
    if cliente is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(cliente)
    pausa()

def actualizar_cliente():
    imprimir_titulo("ACTUALIZAR CLIENTE")
    id_cliente = pedir_entero("Id: ")
    cliente = clientes.obtener(id_cliente)
    if cliente is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {cliente.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "telefono", "ciudad"):
        actual = getattr(cliente, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*clientes.actualizar(id_cliente, cambios))
    pausa()

def eliminar_cliente():
    imprimir_titulo("ELIMINAR CLIENTE")
    id_cliente = pedir_entero("Id: ")
    cliente = clientes.obtener(id_cliente)
    if cliente is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {cliente.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*clientes.eliminar(id_cliente))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE VENDEDORES
# =====================================================================

def crear_vendedor():
    imprimir_titulo("CREAR VENDEDOR")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "sucursal": input("Sucursal [Dejar vacío para Principal]: "),
    }
    mostrar_resultado(*vendedores.crear(datos))
    pausa()

def listar_vendedores():
    imprimir_titulo("VENDEDORES")
    mostrar_lista(vendedores.leer(), "Todavía no hay vendedores.")
    pausa()

def buscar_vendedor():
    imprimir_titulo("BUSCAR VENDEDOR")
    termino = input("Nombre, email o sucursal: ")
    encontrados = vendedores.buscar(termino)
    mostrar_lista(encontrados, f"Ningún vendedor coincide con '{termino}'.")
    pausa()

def ver_vendedor():
    imprimir_titulo("VER VENDEDOR POR ID")
    vendedor = vendedores.obtener(pedir_entero("Id: "))
    if vendedor is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(vendedor)
    pausa()

def actualizar_vendedor():
    imprimir_titulo("ACTUALIZAR VENDEDOR")
    id_vendedor = pedir_entero("Id: ")
    vendedor = vendedores.obtener(id_vendedor)
    if vendedor is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {vendedor.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "sucursal"):
        actual = getattr(vendedor, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*vendedores.actualizar(id_vendedor, cambios))
    pausa()

def eliminar_vendedor():
    imprimir_titulo("ELIMINAR VENDEDOR")
    id_vendedor = pedir_entero("Id: ")
    vendedor = vendedores.obtener(id_vendedor)
    if vendedor is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {vendedor.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*vendedores.eliminar(id_vendedor))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE PRODUCTOS
# =====================================================================

def crear_producto():
    imprimir_titulo("CREAR PRODUCTO")
    datos = {
        "nombre": input("Nombre: "),
        "precio": input("Precio: "),
        "stock": input("Stock: "),
    }
    mostrar_resultado(*productos.crear(datos))
    pausa()

def listar_productos():
    imprimir_titulo("PRODUCTOS")
    mostrar_lista(productos.leer(), "Todavía no hay productos.")
    pausa()

def buscar_producto():
    imprimir_titulo("BUSCAR PRODUCTO")
    termino = input("Nombre: ")
    mostrar_lista(productos.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_producto():
    imprimir_titulo("VER PRODUCTO POR ID")
    producto = productos.obtener(pedir_entero("Id: "))
    if producto is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(producto)
        imprimir_info(f"Precio con IVA: ${producto.con_iva(producto.precio):.2f}")
    pausa()

def actualizar_producto():
    imprimir_titulo("ACTUALIZAR PRODUCTO")
    id_producto = pedir_entero("Id: ")
    producto = productos.obtener(id_producto)
    if producto is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {producto.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "precio", "stock"):
        actual = getattr(producto, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*productos.actualizar(id_producto, cambios))
    pausa()

def eliminar_producto():
    imprimir_titulo("ELIMINAR PRODUCTO")
    id_producto = pedir_entero("Id: ")
    producto = productos.obtener(id_producto)
    if producto is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {producto.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*productos.eliminar(id_producto))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE VENTAS
# =====================================================================

def registrar_venta():
    imprimir_titulo("REGISTRAR VENTA")
    
    imprimir_info("Clientes:")
    mostrar_lista(clientes.leer())
    imprimir_info("Vendedores:")
    mostrar_lista(vendedores.leer())
    imprimir_info("Productos:")
    mostrar_lista(productos.leer())

    datos = {
        "cliente_id": pedir_entero("\nId del cliente: "),
        "vendedor_id": pedir_entero("Id del vendedor: "),
        "producto_id": pedir_entero("Id del producto: "),
        "cantidad": pedir_entero("Cantidad: "),
    }
    
    if None in datos.values():
        imprimir_error("Todos los datos deben ser números enteros")
        return pausa()

    mostrar_resultado(*ventas.crear(datos))
    pausa()

def listar_ventas():
    imprimir_titulo("VENTAS")
    mostrar_lista(ventas.leer(), "Todavía no hay ventas.")
    pausa()

def ver_comprobante():
    imprimir_titulo("COMPROBANTE")
    texto = ventas.comprobante(pedir_entero("Id de la venta: "))
    if texto is None:
        imprimir_error("No existe esa venta")
    else:
        print(texto)
    pausa()

def anular_venta():
    imprimir_titulo("ANULAR VENTA")
    id_venta = pedir_entero("Id de la venta: ")
    if id_venta and confirmar("Se devolverá el stock. ¿Confirma?"):
        mostrar_resultado(*ventas.eliminar(id_venta))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE PAGOS
# =====================================================================

def registrar_pago():
    imprimir_titulo("REGISTRAR PAGO")
    imprimir_info("Ventas registradas:")
    mostrar_lista(ventas.leer(), "No hay ventas para pagar.")
    
    venta_id = pedir_entero("\nId de la venta a pagar: ")
    if venta_id is None:
        imprimir_error("El ID debe ser un número")
        return pausa()

    print("\nMétodos aceptados: efectivo, tarjeta, transferencia")
    metodo = input("Método de pago: ").strip()
    
    recibido = input("Monto entregado por el cliente (dejar vacío si es tarjeta/transferencia): ").strip()
    
    datos = {
        "venta_id": venta_id,
        "metodo": metodo,
        "recibido": recibido
    }
    
    mostrar_resultado(*pagos.crear(datos))
    pausa()

def listar_pagos():
    imprimir_titulo("PAGOS REGISTRADOS")
    mostrar_lista(pagos.leer(), "Todavía no hay pagos.")
    pausa()

def buscar_pago():
    imprimir_titulo("BUSCAR PAGO")
    termino = input("Método de pago (ej. efectivo) o fecha: ")
    mostrar_lista(pagos.buscar(termino), "Sin coincidencias.")
    pausa()

def anular_pago():
    imprimir_titulo("ANULAR PAGO")
    id_pago = pedir_entero("Id del pago: ")
    if id_pago and confirmar("¿Confirma anular este registro de pago?"):
        mostrar_resultado(*pagos.eliminar(id_pago))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# RESUMEN GENERAL (Todos los módulos)
# =====================================================================

def resumen():
    imprimir_titulo("RESUMEN DEL NEGOCIO")
    print(f"  Clientes   : {len(clientes.leer())}")
    print(f"  Ciudades   : {', '.join(clientes.ciudades()) or '-'}")
    print(f"  Vendedores : {len(vendedores.leer())}")
    print(f"  Productos  : {len(productos.leer())}")
    
    bajos = productos.con_stock_bajo()
    print(f"  Stock bajo : {', '.join(p.nombre for p in bajos) or 'ninguno'}")
    
    print(f"  Ventas     : {len(ventas.leer())}")
    print(f"  Facturado  : ${ventas.total_vendido():.2f}")
    
    print(f"  Pagos      : {len(pagos.leer())}")
    print(f"  Recaudado  : ${pagos.total_recaudado():.2f}") 
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS Y BUCLE PRINCIPAL
# =====================================================================

MENU_CLIENTES = {
    "1": ("Crear cliente", crear_cliente),
    "2": ("Ver todos", listar_clientes),
    "3": ("Buscar", buscar_cliente),
    "4": ("Ver por id", ver_cliente),
    "5": ("Actualizar", actualizar_cliente),
    "6": ("Eliminar", eliminar_cliente),
    "0": ("Volver", None),
}

MENU_VENDEDORES = {
    "1": ("Crear vendedor", crear_vendedor),
    "2": ("Ver todos", listar_vendedores),
    "3": ("Buscar", buscar_vendedor),
    "4": ("Ver por id", ver_vendedor),
    "5": ("Actualizar", actualizar_vendedor),
    "6": ("Eliminar", eliminar_vendedor),
    "0": ("Volver", None),
}

MENU_PRODUCTOS = {
    "1": ("Crear producto", crear_producto),
    "2": ("Ver todos", listar_productos),
    "3": ("Buscar", buscar_producto),
    "4": ("Ver por id", ver_producto),
    "5": ("Actualizar", actualizar_producto),
    "6": ("Eliminar", eliminar_producto),
    "0": ("Volver", None),
}

MENU_VENTAS = {
    "1": ("Registrar venta", registrar_venta),
    "2": ("Ver todas", listar_ventas),
    "3": ("Ver comprobante", ver_comprobante),
    "4": ("Anular venta", anular_venta),
    "0": ("Volver", None),
}

MENU_PAGOS = {
    "1": ("Registrar pago", registrar_pago),
    "2": ("Ver todos", listar_pagos),
    "3": ("Buscar pago", buscar_pago),
    "4": ("Anular pago", anular_pago),
    "0": ("Volver", None),
}

def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = opciones[tecla]
        if funcion is None:
            break
        funcion()

def main():
    while True:
        imprimir_titulo("SISTEMA DE VENTAS COMPLETO")
        print("  1. Clientes")
        print("  2. Vendedores")
        print("  3. Productos")
        print("  4. Ventas")
        print("  5. Pagos")
        print("  6. Resumen de Negocio")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("CLIENTES", MENU_CLIENTES)
        elif tecla == "2":
            ejecutar_menu("VENDEDORES", MENU_VENDEDORES)
        elif tecla == "3":
            ejecutar_menu("PRODUCTOS", MENU_PRODUCTOS)
        elif tecla == "4":
            ejecutar_menu("VENTAS", MENU_VENTAS)
        elif tecla == "5":
            ejecutar_menu("PAGOS", MENU_PAGOS)
        elif tecla == "6":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")