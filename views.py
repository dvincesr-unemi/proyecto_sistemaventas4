from abc import ABC, abstractmethod

# Importamos todos los modelos de nuestra arquitectura
from models import Cliente, Vendedor, Producto, Venta, Pago
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# =====================================================================
# CLASE BASE (ABSTRACTA)
# =====================================================================
class CrudBase(ABC):
    @abstractmethod
    def leer(self): pass
    @abstractmethod
    def obtener(self, id_registro): pass
    @abstractmethod
    def buscar(self, texto): pass
    @abstractmethod
    def siguiente(self): pass
    @abstractmethod
    def crear(self, datos): pass
    @abstractmethod
    def actualizar(self, id_registro, datos): pass
    @abstractmethod
    def eliminar(self, id_registro): pass


# =====================================================================
# CONTROLADOR DE CLIENTES
# =====================================================================
class ClienteController(CrudBase):

    def __init__(self, archivo="data/clientes.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Cliente.desde_diccionario(datos))

    def guardar(self):
        datos = [cliente.a_diccionario() for cliente in self.lista]
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            usados = {c.email for c in self.lista if c.id != id_actual}
            if email in usados:
                return "Ese email ya está registrado"

        telefono = str(datos.get("telefono", "")).strip()
        if telefono != "" and not telefono.isdigit():
            return "El teléfono solo puede tener números"
        return None

    def leer(self): return self.lista
    
    def obtener(self, id_cliente):
        for cliente in self.lista:
            if cliente.id == id_cliente: return cliente
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        if texto == "": return []
        return [c for c in self.lista if (texto in c.nombre.lower() or 
                texto in c.apellido.lower() or texto in c.email or 
                texto in c.telefono or texto in c.ciudad.lower())]

    def siguiente(self):
        return max([c.id for c in self.lista] + [0]) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error

        cliente = Cliente(self.siguiente(),
                          str(datos["nombre"]).strip().title(),
                          str(datos["apellido"]).strip().title(),
                          str(datos["email"]).strip().lower(),
                          str(datos.get("telefono", "")).strip(),
                          str(datos.get("ciudad", "")).strip().title())
        self.lista.append(cliente)
        self.guardar()
        return True, f"Cliente creado: {cliente.etiqueta()}"

    def actualizar(self, id_cliente, datos):
        cliente = self.obtener(id_cliente)
        if not cliente: return False, f"No existe un cliente con id {id_cliente}"
        if not datos: return False, "No se indicó ningún cambio"

        desconocidos = set(datos) - {"nombre", "apellido", "email", "telefono", "ciudad"}
        if desconocidos: return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_cliente)
        if error: return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "ciudad"): valor = valor.title()
            elif campo == "email": valor = valor.lower()
            setattr(cliente, campo, valor)

        self.guardar()
        return True, f"Cliente {id_cliente} actualizado"

    def eliminar(self, id_cliente):
        cliente = self.obtener(id_cliente)
        if not cliente: return False, f"No existe un cliente con id {id_cliente}"
        self.lista.remove(cliente)
        self.guardar()
        return True, f"Cliente {id_cliente} eliminado"


# =====================================================================
# CONTROLADOR DE VENDEDORES
# =====================================================================
class VendedorController(CrudBase):

    def __init__(self, archivo="data/vendedores.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Vendedor.desde_diccionario(datos))

    def guardar(self):
        datos = [vendedor.a_diccionario() for vendedor in self.lista]
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            usados = {v.email for v in self.lista if v.id != id_actual}
            if email in usados:
                return "Ese email ya está registrado"
        return None

    def leer(self): return self.lista
    
    def obtener(self, id_vendedor):
        for vendedor in self.lista:
            if vendedor.id == id_vendedor: return vendedor
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        if texto == "": return []
        return [v for v in self.lista if (texto in v.nombre.lower() or 
                texto in v.apellido.lower() or texto in v.email or 
                texto in v.sucursal.lower())]

    def siguiente(self):
        return max([v.id for v in self.lista] + [0]) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error

        sucursal = str(datos.get("sucursal", "")).strip().title()
        vendedor = Vendedor(self.siguiente(),
                            str(datos["nombre"]).strip().title(),
                            str(datos["apellido"]).strip().title(),
                            str(datos["email"]).strip().lower(),
                            sucursal if sucursal else "Principal")
        self.lista.append(vendedor)
        self.guardar()
        return True, f"Vendedor creado: {vendedor.etiqueta()}"

    def actualizar(self, id_vendedor, datos):
        vendedor = self.obtener(id_vendedor)
        if not vendedor: return False, f"No existe un vendedor con id {id_vendedor}"
        if not datos: return False, "No se indicó ningún cambio"

        desconocidos = set(datos) - {"nombre", "apellido", "email", "sucursal"}
        if desconocidos: return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_vendedor)
        if error: return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "sucursal"): valor = valor.title()
            elif campo == "email": valor = valor.lower()
            setattr(vendedor, campo, valor)

        self.guardar()
        return True, f"Vendedor {id_vendedor} actualizado"

    def eliminar(self, id_vendedor):
        vendedor = self.obtener(id_vendedor)
        if not vendedor: return False, f"No existe un vendedor con id {id_vendedor}"
        self.lista.remove(vendedor)
        self.guardar()
        return True, f"Vendedor {id_vendedor} eliminado"


# =====================================================================
# CONTROLADOR DE PRODUCTOS
# =====================================================================
class ProductoController(CrudBase):
    
    def __init__(self, archivo="data/productos.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Producto.desde_diccionario(datos))

    def guardar(self):
        datos = [producto.a_diccionario() for producto in self.lista]
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "precio"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
                    
        if "precio" in datos and not Producto.es_precio_valido(datos["precio"]):
            return f"Precio inválido: '{datos['precio']}'"
            
        stock = str(datos.get("stock", "")).strip()
        if stock != "" and not stock.isdigit():
            return "El stock debe ser un número entero positivo"
            
        if "nombre" in datos:
            nombre = str(datos["nombre"]).strip().title()
            for otro in self.lista:
                if otro.nombre == nombre and otro.id != id_actual:
                    return f"Ya existe un producto llamado {nombre}"
        return None

    def leer(self): return self.lista
    
    def obtener(self, id_producto):
        for producto in self.lista:
            if producto.id == id_producto: return producto
        return None
        
    def buscar(self, texto):
        texto = texto.strip().lower()
        if texto == "": return []
        return [p for p in self.lista if texto in p.nombre.lower()]
        
    def siguiente(self):
        return max([p.id for p in self.lista] + [0]) + 1
        
    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        stock = str(datos.get("stock", "")).strip()
        producto = Producto(self.siguiente(), str(datos["nombre"]).strip().title(),
                            float(datos["precio"]), int(stock) if stock != "" else 0)
        self.lista.append(producto)
        self.guardar()
        return True, f"Producto creado: {producto.etiqueta()}"
        
    def actualizar(self, id_producto, datos):
        producto = self.obtener(id_producto)
        if not producto: return False, "No existe el producto"
        if not datos: return False, "Sin cambios"
        
        error = self.validar(datos, id_producto)
        if error: return False, error
        
        if "nombre" in datos: producto.nombre = str(datos["nombre"]).strip().title()
        if "precio" in datos: producto.precio = float(datos["precio"])
        if "stock" in datos: producto.stock = int(datos["stock"])
        self.guardar()
        return True, "Producto actualizado"
        
    def eliminar(self, id_producto):
        producto = self.obtener(id_producto)
        if not producto: return False, "No existe"
        self.lista.remove(producto)
        self.guardar()
        return True, "Eliminado"


# =====================================================================
# CONTROLADOR DE VENTAS (Con Vendedor incluido)
# =====================================================================
class VentaController(CrudBase):

    def __init__(self, clientes, vendedores, productos, archivo="data/ventas.json"):
        # Integra las dependencias necesarias
        self.clientes = clientes
        self.vendedores = vendedores 
        self.productos = productos
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Venta.desde_diccionario(datos))

    def guardar(self):
        datos = [venta.a_diccionario() for venta in self.lista]
        self.gestor.guardar(datos)

    def validar(self, datos):
        try:
            cliente_id = int(datos.get("cliente_id", 0))
            vendedor_id = int(datos.get("vendedor_id", 0))
            producto_id = int(datos.get("producto_id", 0))
            cantidad = int(datos.get("cantidad", 0))
        except (TypeError, ValueError):
            return "IDs y cantidad deben ser números enteros"

        if cantidad <= 0: return "La cantidad debe ser mayor a 0"
            
        if self.clientes.obtener(cliente_id) is None:
            return f"No existe un cliente con id {cliente_id}"
            
        if self.vendedores.obtener(vendedor_id) is None:
            return f"No existe un vendedor con id {vendedor_id}"

        producto = self.productos.obtener(producto_id)
        if producto is None:
            return f"No existe un producto con id {producto_id}"
        if not producto.hay_stock(cantidad):
            return f"Stock insuficiente de {producto.nombre}: hay {producto.stock}, piden {cantidad}"
        return None

    def leer(self): return self.lista
    
    def obtener(self, id_venta):
        for venta in self.lista:
            if venta.id == id_venta: return venta
        return None

    def buscar(self, texto):
        texto = texto.strip()
        if texto == "": return []
        return [v for v in self.lista if texto in v.fecha]

    def siguiente(self):
        return max([v.id for v in self.lista] + [0]) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error

        producto = self.productos.obtener(int(datos["producto_id"]))
        
        venta = Venta(self.siguiente(),
                      int(datos["cliente_id"]),
                      int(datos["vendedor_id"]),
                      producto.id,
                      int(datos["cantidad"]),
                      producto.precio)

        producto.descontar_stock(venta.cantidad)
        self.productos.guardar()
        self.lista.append(venta)
        self.guardar()
        return True, f"Venta {venta.id} registrada por ${venta.calcular_total():.2f}"

    def actualizar(self, id_venta, datos):
        return False, "Las ventas no se pueden modificar: anúlela y registre otra"

    def eliminar(self, id_venta):
        venta = self.obtener(id_venta)
        if not venta: return False, f"No existe la venta {id_venta}"

        producto = self.productos.obtener(venta.producto_id)
        if producto is not None:
            producto.devolver_stock(venta.cantidad)
            self.productos.guardar()

        self.lista.remove(venta)
        self.guardar()
        return True, f"Venta {id_venta} anulada y stock devuelto"

    def comprobante(self, id_venta):
        venta = self.obtener(id_venta)
        if not venta: return None

        cliente = self.clientes.obtener(venta.cliente_id)
        vendedor = self.vendedores.obtener(venta.vendedor_id)
        producto = self.productos.obtener(venta.producto_id)
        total = venta.calcular_total()

        texto = f"COMPROBANTE #{venta.id}   fecha: {venta.fecha}\n"
        texto += f"Atendido por: {vendedor.nombre_completo() if vendedor else 'eliminado'}\n"
        texto += "-" * 42 + "\n"
        texto += f"Cliente : {cliente.nombre_completo() if cliente else 'eliminado'}\n"
        texto += f"Producto: {producto.nombre if producto else 'eliminado'}\n"
        texto += f"Cantidad: {venta.cantidad} x ${venta.precio_unitario:.2f}\n"
        texto += "-" * 42 + "\n"
        texto += f"SUBTOTAL: ${total:.2f}\n"
        texto += f"TOTAL con IVA: ${Producto.con_iva(total):.2f}"
        return texto


# =====================================================================
# CONTROLADOR DE PAGOS (Valida y procesa sobre la Venta)
# =====================================================================
class PagoController(CrudBase):

    def __init__(self, ventas_controller, archivo="data/pagos.json"):
        self.ventas = ventas_controller
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Pago.desde_diccionario(datos))

    def guardar(self):
        datos = [pago.a_diccionario() for pago in self.lista]
        self.gestor.guardar(datos)

    def validar(self, datos):
        try:
            venta_id = int(datos.get("venta_id", 0))
        except (TypeError, ValueError):
            return "venta_id debe ser un número entero"

        venta = self.ventas.obtener(venta_id)
        if not venta: return f"No existe una venta con id {venta_id}"

        # Evitar pagar dos veces la misma venta
        for p in self.lista:
            if p.venta_id == venta_id:
                return f"La venta #{venta_id} ya se encuentra pagada"

        metodo = str(datos.get("metodo", "")).strip().lower()
        if not Pago.es_metodo_valido(metodo):
            return f"Método inválido. Aceptados: {', '.join(Pago.METODOS)}"

        recibido = datos.get("recibido", "")
        if recibido != "":
            try: float(recibido)
            except ValueError: return "El monto recibido debe ser un número"

        return None

    def leer(self): return self.lista
    
    def obtener(self, id_pago):
        for pago in self.lista:
            if pago.id == id_pago: return pago
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        if texto == "": return []
        return [p for p in self.lista if texto in p.metodo.lower() or texto in p.fecha]

    def siguiente(self):
        return max([p.id for p in self.lista] + [0]) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error

        venta = self.ventas.obtener(int(datos["venta_id"]))
        monto_a_cobrar = Producto.con_iva(venta.calcular_total())
        
        recibido = datos.get("recibido", "")
        valor_recibido = float(recibido) if recibido != "" else 0

        if datos["metodo"].lower() == "efectivo" and valor_recibido > 0 and valor_recibido < monto_a_cobrar:
            return False, f"Falta dinero: Total es ${monto_a_cobrar:.2f} y se entregó ${valor_recibido:.2f}"

        pago = Pago(self.siguiente(), venta.id, monto_a_cobrar, datos["metodo"].lower(), valor_recibido)

        self.lista.append(pago)
        self.guardar()
        
        mensaje = f"Pago #{pago.id} registrado exitosamente por ${pago.monto:.2f}."
        if pago.metodo == "efectivo" and pago.calcular_cambio() > 0:
            mensaje += f" Entregar vuelto: ${pago.calcular_cambio():.2f}"
            
        return True, mensaje

    def actualizar(self, id_pago, datos):
        return False, "Por seguridad financiera los pagos no se editan. Anúlelo y registre otro."

    def eliminar(self, id_pago):
        pago = self.obtener(id_pago)
        if not pago: return False, f"No existe el pago {id_pago}"
        self.lista.remove(pago)
        self.guardar()
        return True, f"Pago #{id_pago} anulado."