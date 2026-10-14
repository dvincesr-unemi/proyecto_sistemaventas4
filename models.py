from datetime import date

# =====================================================================
# CLASE BASE: lo que todos los modelos comparten
# =====================================================================
class ModeloBase:
    """Padre de todos los modelos. Guarda el id y define el comportamiento común."""

    def __init__(self, id_registro):
        self.id = int(id_registro)

    # ---- ÚNICO MÉTODO DE CLASE DEL PROYECTO ----
    @classmethod
    def desde_diccionario(cls, datos):
        """Diccionario -> objeto. Escrito UNA vez y usado por todos los modelos."""
        datos = dict(datos)                 # copia, para no tocar el original
        id_registro = datos.pop("id")       # saco el id
        return cls(id_registro, **datos)    # el resto son los campos del modelo

    # ---- MÉTODOS DE INSTANCIA ----
    def a_diccionario(self):
        return {"id": self.id}

    def etiqueta(self):
        return f"registro {self.id}"

    def __str__(self):
        return f"[{self.id}] {self.etiqueta()}"


# =====================================================================
# HERENCIA: Persona es la base de Cliente y Vendedor
# =====================================================================
class Persona(ModeloBase):
    """Todo lo que tiene una persona del sistema."""

    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)      # el padre guarda el id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        datos = super().a_diccionario()    # {"id": ...} que arma el padre
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Cliente(Persona):
    """Cliente ES UNA Persona, con teléfono y ciudad."""

    def __init__(self, id_registro, nombre, apellido, email, telefono="", ciudad=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.telefono = telefono
        self.ciudad = ciudad

    def a_diccionario(self):
        datos = super().a_diccionario()    # reutiliza lo de Persona
        datos["telefono"] = self.telefono
        datos["ciudad"] = self.ciudad
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · {self.email} · {self.ciudad or 'sin ciudad'}"


class Vendedor(Persona):
    """Vendedor ES UNA Persona, encargada de realizar las ventas."""

    def __init__(self, id_registro, nombre, apellido, email, sucursal="Principal"):
        super().__init__(id_registro, nombre, apellido, email)
        self.sucursal = sucursal

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["sucursal"] = self.sucursal
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · Sucursal: {self.sucursal}"


# =====================================================================
# PRODUCTO: Atributos y métodos estáticos
# =====================================================================
class Producto(ModeloBase):
    """Producto ES UN ModeloBase. Reglas de negocio y control de stock."""

    STOCK_MINIMO = 5
    IVA = 0.15
    total_creados = 0

    def __init__(self, id_registro, nombre, precio, stock=0):
        super().__init__(id_registro)
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)
        Producto.total_creados += 1

    @staticmethod
    def es_precio_valido(valor):
        try:
            return float(valor) > 0
        except (TypeError, ValueError):
            return False

    @staticmethod
    def con_iva(monto):
        return round(monto * (1 + Producto.IVA), 2)

    def stock_bajo(self):
        return self.stock <= Producto.STOCK_MINIMO

    def hay_stock(self, cantidad):
        return 0 < cantidad <= self.stock

    def descontar_stock(self, cantidad):
        self.stock -= cantidad

    def devolver_stock(self, cantidad):
        self.stock += cantidad

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["precio"] = self.precio
        datos["stock"] = self.stock
        return datos

    def etiqueta(self):
        alerta = " ⚠ stock bajo" if self.stock_bajo() else ""
        return f"{self.nombre} · ${self.precio:.2f} · stock {self.stock}{alerta}"


# =====================================================================
# VENTA: Relaciona al cliente, al vendedor y al producto
# =====================================================================
class Venta(ModeloBase):
    """Venta simple: un cliente, un vendedor, un producto, una cantidad."""

    def __init__(self, id_registro, cliente_id, vendedor_id, producto_id, cantidad,
                 precio_unitario, fecha=""):
        super().__init__(id_registro)
        self.cliente_id = int(cliente_id)
        self.vendedor_id = int(vendedor_id)
        self.producto_id = int(producto_id)
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)
        self.fecha = fecha or date.today().isoformat()

    def calcular_total(self):
        return round(self.cantidad * self.precio_unitario, 2)

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["cliente_id"] = self.cliente_id
        datos["vendedor_id"] = self.vendedor_id
        datos["producto_id"] = self.producto_id
        datos["cantidad"] = self.cantidad
        datos["precio_unitario"] = self.precio_unitario
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return (f"{self.fecha} · Cliente: {self.cliente_id} · Vend: {self.vendedor_id} · "
                f"{self.cantidad} x Prod {self.producto_id} "
                f"= ${self.calcular_total():.2f}")


# =====================================================================
# PAGO: Salda la venta
# =====================================================================
class Pago(ModeloBase):
    """El pago de UNA venta, en UN solo pago. Se relaciona con la venta por id."""

    METODOS = ("efectivo", "tarjeta", "transferencia")

    def __init__(self, id_registro, venta_id, monto, metodo, recibido=0, fecha=""):
        super().__init__(id_registro)
        self.venta_id = int(venta_id)
        self.monto = round(float(monto), 2)
        self.metodo = metodo
        self.recibido = round(float(recibido), 2) if recibido else self.monto
        self.fecha = fecha or date.today().isoformat()

    @staticmethod
    def es_metodo_valido(metodo):
        return str(metodo).strip().lower() in Pago.METODOS

    def calcular_cambio(self):
        return round(self.recibido - self.monto, 2)

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["venta_id"] = self.venta_id
        datos["monto"] = self.monto
        datos["metodo"] = self.metodo
        datos["recibido"] = self.recibido
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return (f"{self.fecha} · venta {self.venta_id} · "
                f"${self.monto:.2f} en {self.metodo}")