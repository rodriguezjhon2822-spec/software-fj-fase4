from abc import ABC, abstractmethod
from datetime import datetime
import logging
import os


# ==========================================
# 1. CONFIGURACIÓN DE LOGS (SOLO EVENTOS/ERRORES)
# ==========================================
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler("logs/sistema_software_fj.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# ==========================================
# 2. JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorSoftwareFJ(Exception):
    """Excepción base para errores controlados en el sistema de Software FJ."""


class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza ante datos inválidos, vacíos o parámetros faltantes."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio no existe o no está disponible."""


class OperacionReservaError(ErrorSoftwareFJ):
    """Se lanza cuando falla confirmar, cancelar o procesar una reserva."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando el cálculo de costos produce valores inconsistentes."""


# ==========================================
# 3. CLASE ABSTRACTA GENERAL Y CLIENTE
# ==========================================
class EntidadGeneral(ABC):
    """Clase abstracta general que define una identidad común en el sistema."""

    def __init__(self, id_entidad: str):
        if id_entidad is None or not str(id_entidad).strip():
            raise DatoInvalidoError("Parámetro faltante: el ID de la entidad es obligatorio.")
        self._id_entidad = str(id_entidad).strip()

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @abstractmethod
    def describir_entidad(self) -> str:
        pass


class Cliente(EntidadGeneral):
    """Entidad Cliente con encapsulación de atributos y validaciones estrictas."""

    def __init__(self, id_entidad: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_entidad)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if valor is None or len(str(valor).strip()) < 2:
            raise DatoInvalidoError("Nombre inválido: debe tener al menos 2 caracteres.")
        self._nombre = str(valor).strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if valor is None or "@" not in str(valor) or "." not in str(valor).split("@")[-1]:
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = str(valor).strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if valor is None:
            raise DatoInvalidoError("Parámetro faltante: el teléfono es obligatorio.")
        digitos = "".join(ch for ch in str(valor) if ch.isdigit())
        if len(digitos) < 7:
            raise DatoInvalidoError(f"Teléfono inválido: '{valor}' (mínimo 7 dígitos).")
        self._telefono = digitos

    def describir_entidad(self) -> str:
        return f"Cliente [{self._id_entidad}] | Nombre: {self._nombre} | Correo: {self._correo} | Tel: {self._telefono}"


# ==========================================
# 4. SERVICIOS (POLIMORFISMO Y SOBRECARGA)
# ==========================================
class Servicio(ABC):
    """Clase abstracta para servicios de Software FJ."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True):
        if not codigo or not str(codigo).strip() or not nombre or not str(nombre).strip():
            raise DatoInvalidoError("Parámetros faltantes: código y nombre del servicio son obligatorios.")
        if tarifa_base is None or tarifa_base <= 0:
            raise CalculoInconsistenteError("Tarifa base inconsistente: debe ser mayor que cero.")
        self.codigo = str(codigo).strip()
        self.nombre = str(nombre).strip()
        self.tarifa_base = float(tarifa_base)
        self.disponible = bool(disponible)

    @abstractmethod
    def validar_parametros(self, cantidad: int):
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    @abstractmethod
    def _calcular_subtotal(self, cantidad: int) -> float:
        pass

    def calcular_costo(
        self,
        cantidad: int,
        impuesto: float = 0.0,
        descuento: float = 0.0,
        cargo_adicional: float = 0.0,
    ) -> float:
        """
        Variante sobrecargada por parámetros opcionales: permite calcular el costo
        con solo cantidad, o añadiendo impuesto, descuento y/o cargo adicional.
        """
        self.validar_parametros(cantidad)
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' ({self.codigo}) no está disponible.")
        if impuesto < 0 or cargo_adicional < 0 or not (0.0 <= descuento < 1.0):
            raise CalculoInconsistenteError(
                "Parámetros de costo inconsistentes: revise impuesto, descuento [0, 1) o cargo adicional."
            )

        subtotal = self._calcular_subtotal(cantidad) + float(cargo_adicional)
        if subtotal <= 0:
            raise CalculoInconsistenteError("Subtotal inconsistente: el valor calculado no es válido.")

        total = subtotal * (1.0 - float(descuento)) * (1.0 + float(impuesto))
        if total <= 0:
            raise CalculoInconsistenteError("Costo total inconsistente: resultó menor o igual a cero.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if capacidad is None or capacidad <= 0:
            raise DatoInvalidoError("Capacidad inválida: debe ser mayor que cero.")
        self.capacidad = int(capacidad)

    def validar_parametros(self, cantidad: int):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1 or cantidad > 24:
            raise DatoInvalidoError("Horas de reserva de sala inválidas: debe ser entero entre 1 y 24.")

    def _calcular_subtotal(self, cantidad: int) -> float:
        return self.tarifa_base * cantidad

    def describir_servicio(self) -> str:
        estado_disp = "Disponible" if self.disponible else "No disponible"
        return f"Sala '{self.nombre}' ({self.codigo}) | Cap: {self.capacidad} | Tarifa/h: ${self.tarifa_base} | {estado_disp}"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, categoria_equipo: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not categoria_equipo or not str(categoria_equipo).strip():
            raise DatoInvalidoError("Parámetro faltante: categoría del equipo requerida.")
        self.categoria_equipo = str(categoria_equipo).strip()

    def validar_parametros(self, cantidad: int):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1 or cantidad > 30:
            raise DatoInvalidoError("Días/unidades de alquiler inválidos: debe ser entero entre 1 y 30.")

    def _calcular_subtotal(self, cantidad: int) -> float:
        return self.tarifa_base * cantidad

    def describir_servicio(self) -> str:
        estado_disp = "Disponible" if self.disponible else "No disponible"
        return f"Equipo '{self.nombre}' ({self.codigo}) [{self.categoria_equipo}] | Tarifa: ${self.tarifa_base} | {estado_disp}"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorías especializadas."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, area_especialidad: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not area_especialidad or not str(area_especialidad).strip():
            raise DatoInvalidoError("Parámetro faltante: área de especialidad requerida.")
        self.area_especialidad = str(area_especialidad).strip()

    def validar_parametros(self, cantidad: int):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1 or cantidad > 100:
            raise DatoInvalidoError("Horas de asesoría inválidas: debe ser entero entre 1 y 100.")

    def _calcular_subtotal(self, cantidad: int) -> float:
        # Tarifa base inicial de $25 + costo por hora
        return 25.0 + (self.tarifa_base * cantidad)

    def describir_servicio(self) -> str:
        estado_disp = "Disponible" if self.disponible else "No disponible"
        return f"Asesoría '{self.nombre}' ({self.codigo}) [{self.area_especialidad}] | Base $25 + ${self.tarifa_base}/h | {estado_disp}"


# ==========================================
# 5. RESERVA Y GESTOR EN MEMORIA
# ==========================================
class Reserva:
    """Gestiona una reserva integrando cliente, servicio, duración y estado."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        if not id_reserva or not str(id_reserva).strip():
            raise DatoInvalidoError("Parámetro faltante: el ID de la reserva es obligatorio.")
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Cliente inválido para la reserva.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Servicio inválido para la reserva.")

        servicio.validar_parametros(duracion)
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"No se puede crear reserva: el servicio '{servicio.nombre}' no está disponible.")

        self.id_reserva = str(id_reserva).strip()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.fecha_creacion = datetime.now()
        self.costo_final = 0.0

    def procesar_y_confirmar(self, impuesto: float = 0.0, descuento: float = 0.0, cargo_adicional: float = 0.0):
        if self.estado == "CANCELADA":
            raise OperacionReservaError(f"Operación no permitida: la reserva {self.id_reserva} está cancelada.")
        if self.estado == "CONFIRMADA":
            raise OperacionReservaError(f"Operación no permitida: la reserva {self.id_reserva} ya fue confirmada.")

        intento_completado = False
        try:
            self.costo_final = self.servicio.calcular_costo(
                self.duracion,
                impuesto=impuesto,
                descuento=descuento,
                cargo_adicional=cargo_adicional,
            )
        except ErrorSoftwareFJ as exc:
            # Encadenamiento explícito de excepciones
            raise OperacionReservaError(
                f"No se pudo procesar ni confirmar la reserva {self.id_reserva}."
            ) from exc
        else:
            self.estado = "CONFIRMADA"
            intento_completado = True
            logger.info(
                f"RESERVA CONFIRMADA | ID: {self.id_reserva} | Cliente: {self.cliente.id_entidad} | "
                f"Servicio: {self.servicio.codigo} | Total: ${self.costo_final}"
            )
        finally:
            logger.info(
                f"AUDITORÍA RESERVA | ID: {self.id_reserva} | Estado actual: {self.estado} | "
                f"Cálculo exitoso: {intento_completado}"
            )

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionReservaError(f"Operación no permitida: la reserva {self.id_reserva} ya está cancelada.")
        self.estado = "CANCELADA"
        logger.info(f"RESERVA CANCELADA | ID: {self.id_reserva}")


class GestorSoftwareFJ:
    """Administra listas en memoria sin uso de bases de datos."""

    def __init__(self):
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, cliente: Cliente):
        if any(c.id_entidad == cliente.id_entidad for c in self.clientes):
            raise DatoInvalidoError(f"ID de cliente duplicado: '{cliente.id_entidad}'.")
        self.clientes.append(cliente)
        logger.info(f"CLIENTE REGISTRADO | {cliente.describir_entidad()}")

    def registrar_servicio(self, servicio: Servicio):
        if any(s.codigo == servicio.codigo for s in self.servicios):
            raise DatoInvalidoError(f"Código de servicio duplicado: '{servicio.codigo}'.")
        self.servicios.append(servicio)
        logger.info(f"SERVICIO REGISTRADO | {servicio.describir_servicio()}")

    def registrar_reserva(self, reserva: Reserva):
        if any(r.id_reserva == reserva.id_reserva for r in self.reservas):
            raise OperacionReservaError(f"ID de reserva duplicado: '{reserva.id_reserva}'.")
        self.reservas.append(reserva)
        logger.info(f"RESERVA CREADA | ID: {reserva.id_reserva} | Estado: {reserva.estado}")


# ==========================================
# 6. SIMULACIÓN DE 12 OPERACIONES
# ==========================================
def correr_simulacion():
    gestor = GestorSoftwareFJ()

    casos = [
        ("1. Registro válido de cliente", lambda: gestor.registrar_cliente(
            Cliente("CLI-01", "Laura Martínez", "laura.martinez@correo.com", "3104567890")
        )),
        ("2. Registro inválido de cliente (correo sin dominio)", lambda: gestor.registrar_cliente(
            Cliente("CLI-02", "Carlos Ruiz", "carlos@sinpunto", "3112223344")
        )),
        ("3. Registro inválido de cliente (parámetro faltante/vacío)", lambda: gestor.registrar_cliente(
            Cliente("CLI-03", "", "test@correo.com", "3112223344")
        )),
        ("4. Creación válida de servicio: Sala", lambda: gestor.registrar_servicio(
            ReservaSala("SAL-01", "Sala Ejecutiva Norte", 45.0, capacidad=12, disponible=True)
        )),
        ("5. Creación válida de servicio: Alquiler de Equipo", lambda: gestor.registrar_servicio(
            AlquilerEquipo("EQP-01", "Estación Workstation", 35.0, "Computación", disponible=True)
        )),
        ("6. Creación válida de servicio: Asesoría Especializada", lambda: gestor.registrar_servicio(
            AsesoriaEspecializada("ASE-01", "Auditoría de Software", 90.0, "Calidad", disponible=True)
        )),
        ("7. Creación inválida de servicio (tarifa inconsistente)", lambda: gestor.registrar_servicio(
            AlquilerEquipo("EQP-02", "Proyector HD", 0.0, "Multimedia", disponible=True)
        )),
        ("8. Reserva exitosa y confirmada (con descuento e impuesto)", lambda: (
            gestor.registrar_reserva(Reserva("RES-01", gestor.clientes[0], gestor.servicios[0], 4)),
            gestor.reservas[-1].procesar_y_confirmar(impuesto=0.19, descuento=0.10),
        )),
        ("9. Reserva fallida por duración inválida", lambda: gestor.registrar_reserva(
            Reserva("RES-02", gestor.clientes[0], gestor.servicios[0], 30)
        )),
        ("10. Reserva fallida por servicio no disponible", lambda: (
            gestor.registrar_servicio(ReservaSala("SAL-02", "Sala Taller", 40.0, 8, disponible=False)),
            gestor.registrar_reserva(Reserva("RES-03", gestor.clientes[0], gestor.servicios[-1], 2)),
        )),
        ("11. Confirmación fallida por cálculo inconsistente (descuento >= 1)", lambda: (
            gestor.registrar_reserva(Reserva("RES-04", gestor.clientes[0], gestor.servicios[1], 2)),
            gestor.reservas[-1].procesar_y_confirmar(descuento=1.2),
        )),
        ("12. Cancelación válida de reserva", lambda: gestor.reservas[0].cancelar()),
    ]

    for titulo, paso in casos:
        try:
            paso()
        except ErrorSoftwareFJ as err:
            print(f"[EXCEPCIÓN CONTROLADA] {titulo} -> {err}")
            if err.__cause__:
                print(f"   ↳ Excepción encadenada (__cause__): {err.__cause__}")
            logger.error(f"FALLO EN {titulo} | {err} | Causa encadenada: {err.__cause__}")
        else:
            print(f"[ÉXITO] {titulo}")
        finally:
            print(f"   [FIN DE PASO] {titulo} (sistema activo)")


if __name__ == "__main__":
    correr_simulacion()
    print("\nProceso finalizado. Verifica 'logs/sistema_software_fj.log'.")