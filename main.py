from abc import ABC, abstractmethod  # Importa ABC y abstractmethod para crear clases y métodos abstractos[cite: 1, 2].
from datetime import datetime  # Importa datetime para registrar la fecha y hora de creación de cada reserva.
import logging  # Importa logging para escribir eventos y errores en un archivo de log[cite: 2, 3].
import os  # Importa os para crear carpetas del sistema de archivos si no existen.


# ==========================================
# 1. CONFIGURACIÓN DE LOGS (SOLO EVENTOS/ERRORES)
# ==========================================
os.makedirs("logs", exist_ok=True)  # Crea la carpeta 'logs' si no existe, sin lanzar error si ya está creada.
logger = logging.getLogger("SoftwareFJ")  # Crea o recupera el logger nombrado 'SoftwareFJ'.
logger.setLevel(logging.INFO)  # Define el nivel mínimo de registro en INFO (captura INFO, WARNING, ERROR, etc.).

if not logger.handlers:  # Evita agregar manejadores duplicados si se reejecuta en el mismo proceso.
    file_handler = logging.FileHandler("logs/sistema_software_fj.log", encoding="utf-8")  # Crea el archivo de log en UTF-8[cite: 2, 3].
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  # Define formato: fecha/hora, nivel y mensaje.
    file_handler.setFormatter(formatter)  # Asigna el formato al manejador de archivo.
    logger.addHandler(file_handler)  # Agrega el manejador de archivo al logger.


# ==========================================
# 2. JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorSoftwareFJ(Exception):  # Clase base personalizada que hereda de Exception[cite: 2].
    """Excepción base para errores controlados en el sistema de Software FJ."""  # Documenta el propósito de la clase base[cite: 2, 6].


class DatoInvalidoError(ErrorSoftwareFJ):  # Excepción específica para datos inválidos o faltantes[cite: 2].
    """Se lanza ante datos inválidos, vacíos o parámetros faltantes."""  # Explica cuándo ocurre este error[cite: 2, 6].


class ServicioNoDisponibleError(ErrorSoftwareFJ):  # Excepción específica para servicios inactivos o no disponibles[cite: 2].
    """Se lanza cuando un servicio no existe o no está disponible."""  # Explica cuándo ocurre este error[cite: 2, 6].


class OperacionReservaError(ErrorSoftwareFJ):  # Excepción específica para fallos en el ciclo de vida de una reserva[cite: 2].
    """Se lanza cuando falla confirmar, cancelar o procesar una reserva."""  # Explica cuándo ocurre este error[cite: 2, 6].


class CalculoInconsistenteError(ErrorSoftwareFJ):  # Excepción específica para inconsistencias matemáticas o de tarifas[cite: 2].
    """Se lanza cuando el cálculo de costos produce valores inconsistentes."""  # Explica cuándo ocurre este error[cite: 2, 6].


# ==========================================
# 3. CLASE ABSTRACTA GENERAL Y CLIENTE
# ==========================================
class EntidadGeneral(ABC):  # Clase abstracta base para entidades generales del sistema[cite: 2].
    """Clase abstracta general que define una identidad común en el sistema."""  # Describe la abstracción general[cite: 2, 6].

    def __init__(self, id_entidad: str):  # Constructor que recibe el identificador de la entidad.
        if id_entidad is None or not str(id_entidad).strip():  # Valida que el ID no sea None ni esté vacío/en blanco[cite: 2].
            raise DatoInvalidoError("Parámetro faltante: el ID de la entidad es obligatorio.")  # Lanza excepción si falta ID[cite: 2].
        self._id_entidad = str(id_entidad).strip()  # Guarda el ID limpio como atributo protegido (_id_entidad)[cite: 2].

    @property  # Expone id_entidad como propiedad de solo lectura.
    def id_entidad(self) -> str:  # Método getter para consultar el ID de forma controlada.
        return self._id_entidad  # Retorna el identificador almacenado.

    @abstractmethod  # Marca este método como obligatorio para cualquier clase hija.
    def describir_entidad(self) -> str:  # Firma abstracta para describir la entidad.
        pass  # Sin implementación aquí; cada subclase define su propia descripción.


class Cliente(EntidadGeneral):  # Clase Cliente que hereda de EntidadGeneral[cite: 2].
    """Entidad Cliente con encapsulación de atributos y validaciones estrictas."""  # Describe encapsulación y validaciones[cite: 2, 6].

    def __init__(self, id_entidad: str, nombre: str, correo: str, telefono: str):  # Constructor de Cliente.
        super().__init__(id_entidad)  # Llama al constructor de EntidadGeneral para validar y asignar el ID[cite: 2].
        self.nombre = nombre  # Asigna el nombre usando su setter de validación[cite: 2].
        self.correo = correo  # Asigna el correo usando su setter de validación[cite: 2].
        self.telefono = telefono  # Asigna el teléfono usando su setter de validación[cite: 2].

    @property  # Propiedad getter para nombre.
    def nombre(self) -> str:  # Retorna el nombre encapsulado.
        return self._nombre  # Devuelve _nombre.

    @nombre.setter  # Setter que valida el nombre antes de guardarlo[cite: 2].
    def nombre(self, valor: str):  # Recibe el nuevo valor de nombre.
        if valor is None or len(str(valor).strip()) < 2:  # Verifica que tenga al menos 2 caracteres útiles[cite: 2].
            raise DatoInvalidoError("Nombre inválido: debe tener al menos 2 caracteres.")  # Lanza error si es inválido[cite: 2].
        self._nombre = str(valor).strip()  # Guarda el nombre limpio en el atributo protegido[cite: 2].

    @property  # Propiedad getter para correo.
    def correo(self) -> str:  # Retorna el correo encapsulado.
        return self._correo  # Devuelve _correo.

    @correo.setter  # Setter que valida el formato básico del correo[cite: 2].
    def correo(self, valor: str):  # Recibe el correo a validar.
        if valor is None or "@" not in str(valor) or "." not in str(valor).split("@")[-1]:  # Valida '@' y dominio con punto[cite: 2].
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")  # Lanza error si no cumple el formato[cite: 2].
        self._correo = str(valor).strip()  # Guarda el correo limpio en _correo[cite: 2].

    @property  # Propiedad getter para teléfono.
    def telefono(self) -> str:  # Retorna el teléfono encapsulado.
        return self._telefono  # Devuelve _telefono.

    @telefono.setter  # Setter que valida y limpia el número telefónico[cite: 2].
    def telefono(self, valor: str):  # Recibe el teléfono a validar.
        if valor is None:  # Verifica que el parámetro no sea None[cite: 2].
            raise DatoInvalidoError("Parámetro faltante: el teléfono es obligatorio.")  # Lanza error si falta el teléfono[cite: 2].
        digitos = "".join(ch for ch in str(valor) if ch.isdigit())  # Extrae únicamente los caracteres numéricos.
        if len(digitos) < 7:  # Exige al menos 7 dígitos numéricos[cite: 2].
            raise DatoInvalidoError(f"Teléfono inválido: '{valor}' (mínimo 7 dígitos).")  # Lanza error si es muy corto[cite: 2].
        self._telefono = digitos  # Guarda solo los dígitos en _telefono[cite: 2].

    def describir_entidad(self) -> str:  # Implementa el método abstracto heredado de EntidadGeneral[cite: 2].
        return (  # Construye una cadena legible con los datos del cliente.
            f"Cliente [{self._id_entidad}] | Nombre: {self._nombre} | "
            f"Correo: {self._correo} | Tel: {self._telefono}"
        )


# ==========================================
# 4. SERVICIOS (POLIMORFISMO Y SOBRECARGA)
# ==========================================
class Servicio(ABC):  # Clase abstracta base para los servicios ofrecidos por Software FJ[cite: 1, 2].
    """Clase abstracta para servicios de Software FJ."""  # Documenta la clase abstracta Servicio[cite: 2, 6].

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True):  # Constructor de Servicio.
        if not codigo or not str(codigo).strip() or not nombre or not str(nombre).strip():  # Valida código y nombre no vacíos[cite: 2].
            raise DatoInvalidoError("Parámetros faltantes: código y nombre del servicio son obligatorios.")  # Lanza error si faltan[cite: 2].
        if tarifa_base is None or tarifa_base <= 0:  # Valida que la tarifa base sea positiva[cite: 2].
            raise CalculoInconsistenteError("Tarifa base inconsistente: debe ser mayor que cero.")  # Lanza error si es <= 0[cite: 2].
        self.codigo = str(codigo).strip()  # Guarda el código limpio del servicio.
        self.nombre = str(nombre).strip()  # Guarda el nombre limpio del servicio.
        self.tarifa_base = float(tarifa_base)  # Convierte y guarda la tarifa base como flotante.
        self.disponible = bool(disponible)  # Convierte y guarda el estado de disponibilidad.

    @abstractmethod  # Método abstracto que cada servicio debe implementar para validar su duración/cantidad[cite: 2].
    def validar_parametros(self, cantidad: int):  # Recibe la cantidad/duración solicitada.
        pass  # Implementado en cada subclase.

    @abstractmethod  # Método abstracto para que cada servicio se describa de forma polimórfica[cite: 2].
    def describir_servicio(self) -> str:  # Retorna la descripción del servicio.
        pass  # Implementado en cada subclase.

    @abstractmethod  # Método protegido abstracto para calcular el subtotal según el tipo de servicio[cite: 2].
    def _calcular_subtotal(self, cantidad: int) -> float:  # Calcula subtotal base antes de cargos/descuentos/impuestos.
        pass  # Implementado en cada subclase.

    def calcular_costo(  # Método con parámetros opcionales (variantes de cálculo de costo)[cite: 2].
        self,
        cantidad: int,  # Cantidad de horas, días o unidades requeridas.
        impuesto: float = 0.0,  # Porcentaje de impuesto opcional (por defecto 0.0)[cite: 2].
        descuento: float = 0.0,  # Porcentaje de descuento opcional entre 0 y <1 (por defecto 0.0)[cite: 2].
        cargo_adicional: float = 0.0,  # Cargo adicional opcional en moneda (por defecto 0.0)[cite: 2].
    ) -> float:  # Retorna el costo final redondeado a 2 decimales.
        """
        Variante sobrecargada por parámetros opcionales: permite calcular el costo
        con solo cantidad, o añadiendo impuesto, descuento y/o cargo adicional.
        """
        self.validar_parametros(cantidad)  # Valida la cantidad usando la regla de la subclase correspondiente[cite: 2].
        if not self.disponible:  # Comprueba que el servicio esté habilitado para reservarse/calcularse[cite: 2].
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' ({self.codigo}) no está disponible.")  # Lanza error si no está disponible[cite: 2].
        if impuesto < 0 or cargo_adicional < 0 or not (0.0 <= descuento < 1.0):  # Valida rangos de parámetros financieros[cite: 2].
            raise CalculoInconsistenteError(  # Lanza error si algún parámetro de costo es inconsistente[cite: 2].
                "Parámetros de costo inconsistentes: revise impuesto, descuento [0, 1) o cargo adicional."
            )

        subtotal = self._calcular_subtotal(cantidad) + float(cargo_adicional)  # Suma subtotal polimórfico y cargo adicional.
        if subtotal <= 0:  # Verifica que el subtotal resultante sea válido[cite: 2].
            raise CalculoInconsistenteError("Subtotal inconsistente: el valor calculado no es válido.")  # Lanza error si es <= 0[cite: 2].

        total = subtotal * (1.0 - float(descuento)) * (1.0 + float(impuesto))  # Aplica descuento e impuesto al subtotal.
        if total <= 0:  # Verifica que el costo final sea mayor que cero[cite: 2].
            raise CalculoInconsistenteError("Costo total inconsistente: resultó menor o igual a cero.")  # Lanza error si es <= 0[cite: 2].
        return round(total, 2)  # Devuelve el valor final redondeado a dos decimales.


class ReservaSala(Servicio):  # Primera subclase especializada: reserva de salas[cite: 1, 2].
    """Servicio de reserva de salas."""  # Documenta la subclase ReservaSala[cite: 2, 6].

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):  # Constructor de sala.
        super().__init__(codigo, nombre, tarifa_base, disponible)  # Inicializa atributos comunes en Servicio[cite: 2].
        if capacidad is None or capacidad <= 0:  # Valida que la capacidad de personas sea positiva[cite: 2].
            raise DatoInvalidoError("Capacidad inválida: debe ser mayor que cero.")  # Lanza error si capacidad <= 0[cite: 2].
        self.capacidad = int(capacidad)  # Guarda la capacidad máxima de la sala.

    def validar_parametros(self, cantidad: int):  # Sobrescribe validación para horas de sala (1 a 24)[cite: 2].
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1 or cantidad > 24:  # Valida entero entre 1 y 24[cite: 2].
            raise DatoInvalidoError("Horas de reserva de sala inválidas: debe ser entero entre 1 y 24.")  # Lanza error si no cumple[cite: 2].

    def _calcular_subtotal(self, cantidad: int) -> float:  # Calcula tarifa por hora multiplicada por horas reservadas.
        return self.tarifa_base * cantidad  # Retorna subtotal de sala.

    def describir_servicio(self) -> str:  # Sobrescribe descripción específica para salas[cite: 2].
        estado_disp = "Disponible" if self.disponible else "No disponible"  # Traduce booleano a texto legible.
        return (  # Retorna descripción completa de la sala.
            f"Sala '{self.nombre}' ({self.codigo}) | Cap: {self.capacidad} | "
            f"Tarifa/h: ${self.tarifa_base} | {estado_disp}"
        )


class AlquilerEquipo(Servicio):  # Segunda subclase especializada: alquiler de equipos[cite: 1, 2].
    """Servicio de alquiler de equipos."""  # Documenta la subclase AlquilerEquipo[cite: 2, 6].

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, categoria_equipo: str, disponible: bool = True):  # Constructor de equipo.
        super().__init__(codigo, nombre, tarifa_base, disponible)  # Inicializa atributos comunes en Servicio[cite: 2].
        if not categoria_equipo or not str(categoria_equipo).strip():  # Valida que se indique categoría del equipo[cite: 2].
            raise DatoInvalidoError("Parámetro faltante: categoría del equipo requerida.")  # Lanza error si falta categoría[cite: 2].
        self.categoria_equipo = str(categoria_equipo).strip()  # Guarda la categoría limpia.

    def validar_parametros(self, cantidad: int):  # Sobrescribe validación para días/unidades de alquiler (1 a 30)[cite: 2].
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1 or cantidad > 30:  # Valida entero entre 1 y 30[cite: 2].
            raise DatoInvalidoError("Días/unidades de alquiler inválidos: debe ser entero entre 1 y 30.")  # Lanza error si no cumple[cite: 2].

    def _calcular_subtotal(self, cantidad: int) -> float:  # Calcula tarifa por unidad/día multiplicada por cantidad.
        return self.tarifa_base * cantidad  # Retorna subtotal de alquiler.

    def describir_servicio(self) -> str:  # Sobrescribe descripción específica para equipos[cite: 2].
        estado_disp = "Disponible" if self.disponible else "No disponible"  # Traduce disponibilidad a texto.
        return (  # Retorna descripción completa del equipo.
            f"Equipo '{self.nombre}' ({self.codigo}) [{self.categoria_equipo}] | "
            f"Tarifa: ${self.tarifa_base} | {estado_disp}"
        )


class AsesoriaEspecializada(Servicio):  # Tercera subclase especializada: asesorías especializadas[cite: 1, 2].
    """Servicio de asesorías especializadas."""  # Documenta la subclase AsesoriaEspecializada[cite: 2, 6].

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, area_especialidad: str, disponible: bool = True):  # Constructor de asesoría.
        super().__init__(codigo, nombre, tarifa_base, disponible)  # Inicializa atributos comunes en Servicio[cite: 2].
        if not area_especialidad or not str(area_especialidad).strip():  # Valida que se indique el área de especialidad[cite: 2].
            raise DatoInvalidoError("Parámetro faltante: área de especialidad requerida.")  # Lanza error si falta el área[cite: 2].
        self.area_especialidad = str(area_especialidad).strip()  # Guarda el área limpia.

    def validar_parametros(self, cantidad: int):  # Sobrescribe validación para horas de asesoría (1 a 100)[cite: 2].
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1 or cantidad > 100:  # Valida entero entre 1 y 100[cite: 2].
            raise DatoInvalidoError("Horas de asesoría inválidas: debe ser entero entre 1 y 100.")  # Lanza error si no cumple[cite: 2].

    def _calcular_subtotal(self, cantidad: int) -> float:  # Calcula cargo fijo inicial de $25 más tarifa por hora.
        return 25.0 + (self.tarifa_base * cantidad)  # Retorna subtotal de asesoría.

    def describir_servicio(self) -> str:  # Sobrescribe descripción específica para asesorías[cite: 2].
        estado_disp = "Disponible" if self.disponible else "No disponible"  # Traduce disponibilidad a texto.
        return (  # Retorna descripción completa de la asesoría.
            f"Asesoría '{self.nombre}' ({self.codigo}) [{self.area_especialidad}] | "
            f"Base $25 + ${self.tarifa_base}/h | {estado_disp}"
        )


# ==========================================
# 5. RESERVA Y GESTOR EN MEMORIA
# ==========================================
class Reserva:  # Clase que representa una reserva integrando cliente, servicio, duración y estado[cite: 2].
    """Gestiona una reserva integrando cliente, servicio, duración y estado."""  # Documenta la clase Reserva[cite: 2, 6].

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):  # Constructor de Reserva.
        if not id_reserva or not str(id_reserva).strip():  # Verifica que el ID de reserva no esté vacío[cite: 2].
            raise DatoInvalidoError("Parámetro faltante: el ID de la reserva es obligatorio.")  # Lanza error si falta ID[cite: 2].
        if not isinstance(cliente, Cliente):  # Verifica que cliente sea instancia válida de Cliente[cite: 2].
            raise DatoInvalidoError("Cliente inválido para la reserva.")  # Lanza error si cliente no es válido[cite: 2].
        if not isinstance(servicio, Servicio):  # Verifica que servicio sea instancia válida de Servicio[cite: 2].
            raise DatoInvalidoError("Servicio inválido para la reserva.")  # Lanza error si servicio no es válido[cite: 2].

        servicio.validar_parametros(duracion)  # Valida que la duración sea permitida para el servicio elegido[cite: 2].
        if not servicio.disponible:  # Verifica que el servicio esté disponible antes de crear la reserva[cite: 2].
            raise ServicioNoDisponibleError(  # Lanza error si el servicio no está disponible[cite: 2].
                f"No se puede crear reserva: el servicio '{servicio.nombre}' no está disponible."
            )

        self.id_reserva = str(id_reserva).strip()  # Guarda el ID limpio de la reserva.
        self.cliente = cliente  # Asocia el objeto Cliente.
        self.servicio = servicio  # Asocia el objeto Servicio.
        self.duracion = duracion  # Guarda la duración solicitada.
        self.estado = "PENDIENTE"  # Define el estado inicial como PENDIENTE.
        self.fecha_creacion = datetime.now()  # Registra la fecha y hora de creación.
        self.costo_final = 0.0  # Inicializa el costo final en 0.0 hasta confirmar.

    def procesar_y_confirmar(self, impuesto: float = 0.0, descuento: float = 0.0, cargo_adicional: float = 0.0):  # Procesa y confirma la reserva[cite: 2].
        if self.estado == "CANCELADA":  # Impide confirmar una reserva ya cancelada[cite: 2].
            raise OperacionReservaError(f"Operación no permitida: la reserva {self.id_reserva} está cancelada.")  # Lanza error de operación[cite: 2].
        if self.estado == "CONFIRMADA":  # Impide reconfirmar una reserva ya confirmada[cite: 2].
            raise OperacionReservaError(f"Operación no permitida: la reserva {self.id_reserva} ya fue confirmada.")  # Lanza error de operación[cite: 2].

        intento_completado = False  # Bandera para registrar en finally si el cálculo y confirmación tuvieron éxito[cite: 2].
        try:  # Inicia bloque try para calcular el costo de la reserva[cite: 2].
            self.costo_final = self.servicio.calcular_costo(  # Invoca calcular_costo con parámetros opcionales[cite: 2].
                self.duracion,
                impuesto=impuesto,
                descuento=descuento,
                cargo_adicional=cargo_adicional,
            )
        except ErrorSoftwareFJ as exc:  # Captura errores propios del dominio al calcular costo[cite: 2].
            raise OperacionReservaError(  # Encadena la excepción original dentro de OperacionReservaError[cite: 2].
                f"No se pudo procesar ni confirmar la reserva {self.id_reserva}."
            ) from exc
        else:  # Se ejecuta solo si no hubo excepción en try[cite: 2].
            self.estado = "CONFIRMADA"  # Actualiza el estado de la reserva a CONFIRMADA[cite: 2].
            intento_completado = True  # Marca el intento como completado.
            logger.info(  # Registra el evento exitoso en el archivo de log[cite: 2, 3].
                f"RESERVA CONFIRMADA | ID: {self.id_reserva} | Cliente: {self.cliente.id_entidad} | "
                f"Servicio: {self.servicio.codigo} | Total: ${self.costo_final}"
            )
        finally:  # Se ejecuta siempre, haya habido error o éxito[cite: 2].
            logger.info(  # Escribe traza de auditoría en el log al finalizar el intento[cite: 2, 3].
                f"AUDITORÍA RESERVA | ID: {self.id_reserva} | Estado actual: {self.estado} | "
                f"Cálculo exitoso: {intento_completado}"
            )

    def cancelar(self):  # Cancela la reserva si no estaba ya cancelada[cite: 2].
        if self.estado == "CANCELADA":  # Verifica si ya está cancelada[cite: 2].
            raise OperacionReservaError(f"Operación no permitida: la reserva {self.id_reserva} ya está cancelada.")  # Lanza error si ya está cancelada[cite: 2].
        self.estado = "CANCELADA"  # Cambia el estado a CANCELADA.
        logger.info(f"RESERVA CANCELADA | ID: {self.id_reserva}")  # Registra la cancelación en el archivo de log[cite: 2, 3].


class GestorSoftwareFJ:  # Administra las colecciones en memoria sin usar bases de datos[cite: 1, 2].
    """Administra listas en memoria sin uso de bases de datos."""  # Documenta el gestor en memoria[cite: 1, 2, 6].

    def __init__(self):  # Inicializa las listas internas del sistema[cite: 1, 2].
        self.clientes: list[Cliente] = []  # Lista en memoria de clientes registrados[cite: 1, 2].
        self.servicios: list[Servicio] = []  # Lista en memoria de servicios registrados[cite: 1, 2].
        self.reservas: list[Reserva] = []  # Lista en memoria de reservas creadas[cite: 1, 2].

    def registrar_cliente(self, cliente: Cliente):  # Registra un cliente validando duplicados por ID.
        if any(c.id_entidad == cliente.id_entidad for c in self.clientes):  # Comprueba si ya existe el ID de cliente.
            raise DatoInvalidoError(f"ID de cliente duplicado: '{cliente.id_entidad}'.")  # Lanza error si está duplicado[cite: 2].
        self.clientes.append(cliente)  # Agrega el cliente a la lista interna en memoria[cite: 1, 2].
        logger.info(f"CLIENTE REGISTRADO | {cliente.describir_entidad()}")  # Registra el evento en el log[cite: 2, 3].

    def registrar_servicio(self, servicio: Servicio):  # Registra un servicio validando duplicados por código.
        if any(s.codigo == servicio.codigo for s in self.servicios):  # Comprueba si ya existe el código de servicio.
            raise DatoInvalidoError(f"Código de servicio duplicado: '{servicio.codigo}'.")  # Lanza error si está duplicado[cite: 2].
        self.servicios.append(servicio)  # Agrega el servicio a la lista interna en memoria[cite: 1, 2].
        logger.info(f"SERVICIO REGISTRADO | {servicio.describir_servicio()}")  # Registra el evento en el log[cite: 2, 3].

    def registrar_reserva(self, reserva: Reserva):  # Registra una reserva validando duplicados por ID.
        if any(r.id_reserva == reserva.id_reserva for r in self.reservas):  # Comprueba si ya existe el ID de reserva.
            raise OperacionReservaError(f"ID de reserva duplicado: '{reserva.id_reserva}'.")  # Lanza error si está duplicada[cite: 2].
        self.reservas.append(reserva)  # Agrega la reserva a la lista interna en memoria[cite: 1, 2].
        logger.info(f"RESERVA CREADA | ID: {reserva.id_reserva} | Estado: {reserva.estado}")  # Registra el evento en el log[cite: 2, 3].


# ==========================================
# 6. SIMULACIÓN DE 13 OPERACIONES
# ==========================================
def correr_simulacion():  # Ejecuta un conjunto de 13 operaciones válidas e inválidas para probar estabilidad[cite: 3].
    gestor = GestorSoftwareFJ()  # Instancia el gestor principal en memoria[cite: 1, 2].

    casos = [  # Lista de tuplas (descripción de la operación, función lambda que ejecuta la acción).
        ("1. Registro válido de cliente", lambda: gestor.registrar_cliente(  # Caso válido de cliente[cite: 3].
            Cliente("CLI-01", "Laura Martínez", "laura.martinez@correo.com", "3104567890")
        )),
        ("2. Registro inválido de cliente (correo sin dominio)", lambda: gestor.registrar_cliente(  # Caso inválido por correo[cite: 2, 3].
            Cliente("CLI-02", "Carlos Ruiz", "carlos@sinpunto", "3112223344")
        )),
        ("3. Registro inválido de cliente (parámetro faltante/vacío)", lambda: gestor.registrar_cliente(  # Caso inválido por nombre vacío[cite: 2, 3].
            Cliente("CLI-03", "", "test@correo.com", "3112223344")
        )),
        ("4. Creación válida de servicio: Sala", lambda: gestor.registrar_servicio(  # Caso válido de ReservaSala[cite: 1, 2, 3].
            ReservaSala("SAL-01", "Sala Ejecutiva Norte", 45.0, capacidad=12, disponible=True)
        )),
        ("5. Creación válida de servicio: Alquiler de Equipo", lambda: gestor.registrar_servicio(  # Caso válido de AlquilerEquipo[cite: 1, 2, 3].
            AlquilerEquipo("EQP-01", "Estación Workstation", 35.0, "Computación", disponible=True)
        )),
        ("6. Creación válida de servicio: Asesoría Especializada", lambda: gestor.registrar_servicio(  # Caso válido de AsesoriaEspecializada[cite: 1, 2, 3].
            AsesoriaEspecializada("ASE-01", "Auditoría de Software", 90.0, "Calidad", disponible=True)
        )),
        ("7. Creación inválida de servicio (tarifa inconsistente)", lambda: gestor.registrar_servicio(  # Caso inválido por tarifa 0[cite: 2, 3].
            AlquilerEquipo("EQP-02", "Proyector HD", 0.0, "Multimedia", disponible=True)
        )),
        ("8. Reserva exitosa y confirmada (con descuento e impuesto)", lambda: (  # Reserva válida y confirmada[cite: 2, 3].
            gestor.registrar_reserva(Reserva("RES-01", gestor.clientes[0], gestor.servicios[0], 4)),
            gestor.reservas[-1].procesar_y_confirmar(impuesto=0.19, descuento=0.10),
        )),
        ("9. Reserva fallida por duración inválida", lambda: gestor.registrar_reserva(  # Reserva inválida por 30 horas (>24)[cite: 2, 3].
            Reserva("RES-02", gestor.clientes[0], gestor.servicios[0], 30)
        )),
        ("10. Reserva fallida por servicio no disponible", lambda: (  # Reserva inválida por sala marcada como no disponible[cite: 2, 3].
            gestor.registrar_servicio(ReservaSala("SAL-02", "Sala Taller", 40.0, 8, disponible=False)),
            gestor.registrar_reserva(Reserva("RES-03", gestor.clientes[0], gestor.servicios[-1], 2)),
        )),
        ("11. Confirmación fallida por cálculo inconsistente (descuento >= 1)", lambda: (  # Error encadenado al calcular costo[cite: 2, 3].
            gestor.registrar_reserva(Reserva("RES-04", gestor.clientes[0], gestor.servicios[1], 2)),
            gestor.reservas[-1].procesar_y_confirmar(descuento=1.2),
        )),
        ("12. Cancelación válida de reserva", lambda: gestor.reservas[0].cancelar()),  # Cancela la reserva RES-01 por primera vez[cite: 2, 3].
        ("13. Cancelación duplicada (operación no permitida)", lambda: gestor.reservas[0].cancelar()),  # Intenta cancelar RES-01 de nuevo[cite: 2, 3].
    ]

    for titulo, paso in casos:  # Recorre todas las operaciones una por una sin detener el programa[cite: 2, 3].
        try:  # Intenta ejecutar la operación actual[cite: 2].
            paso()
        except ErrorSoftwareFJ as err:  # Captura cualquier excepción controlada del sistema[cite: 2].
            print(f"[EXCEPCIÓN CONTROLADA] {titulo} -> {err}")  # Muestra el error en consola.
            if err.__cause__:  # Comprueba si existe una excepción encadenada (__cause__)[cite: 2].
                print(f"   ↳ Excepción encadenada (__cause__): {err.__cause__}")  # Muestra la causa encadenada en consola[cite: 2].
            logger.error(f"FALLO EN {titulo} | {err} | Causa encadenada: {err.__cause__}")  # Registra el error en el log[cite: 2, 3].
        else:  # Se ejecuta cuando la operación no lanzó excepción[cite: 2].
            print(f"[ÉXITO] {titulo}")  # Confirma el éxito en consola.
        finally:  # Se ejecuta siempre al terminar cada operación[cite: 2].
            print(f"   [FIN DE PASO] {titulo} (sistema activo)")  # Confirma que el sistema sigue funcionando[cite: 2, 3].


if __name__ == "__main__":  # Punto de entrada principal cuando el archivo se ejecuta directamente.
    correr_simulacion()  # Corre la simulación de 13 operaciones[cite: 3].
    print("\nProceso finalizado. Verifica 'logs/sistema_software_fj.log'.")  # Informa dónde revisar el archivo de log[cite: 2, 3].
