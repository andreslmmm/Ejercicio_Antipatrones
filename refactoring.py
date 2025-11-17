"""
CÓDIGO REFACTORIZADO - Corrección de los 3 antipatrones
"""

import json
from pathlib import Path


# SOLUCIÓN ANTIPATRÓN 1: Ya no hay números mágicos, todo tiene nombre

class DiscountConfig:
    """Aquí guardamos todos los números de descuentos para no perderlos en el código"""
    
    # Reglas de descuento por tipo de usuario
    DISCOUNT_RULES = {
        "gold": {
            "min_total": 100.0,      # Necesita gastar más de 100
            "discount_rate": 0.15     # 15% de descuento
        },
        "silver": {
            "min_total": 42.0,       # Necesita gastar más de 42
            "discount_rate": 0.07     # 7% de descuento
        }
    }
    DEFAULT_DISCOUNT = 0.0  # Sin descuento por defecto


class ShippingConfig:
    """Todos los números para calcular envíos están aquí"""
    
    # Números que se usan para calcular el costo
    WEIGHT_FACTOR = 0.25        # Cuanto cuesta cada kilo
    DISTANCE_DIVISOR = 300.0    # Para calcular el costo por distancia
    HEAVY_WEIGHT_THRESHOLD = 20.0  # A partir de cuánto es pesado
    
    # Configuración de envío nacional
    DOMESTIC = {
        "base_cost": 5.0,           # Costo base
        "heavy_surcharge": 3.0,     # Cargo extra si es pesado
        "threshold_inclusive": False # Usa > para comparar peso
    }
    
    # Configuración de envío internacional
    INTERNATIONAL = {
        "base_cost": 7.0,           # Costo base más caro
        "heavy_surcharge": 4.0,     # Cargo extra más alto
        "threshold_inclusive": True  # Usa >= para comparar peso
    }


# SOLUCIÓN ANTIPATRÓN 3: Separamos las clases por lo que hacen

class UserRepository:
    """Esta clase solo se encarga de cargar usuarios del archivo"""
    
    def __init__(self, db_path="data.json"):
        self.db_path = Path(db_path)
    
    def load_users(self):
        """Lee el archivo JSON y devuelve la lista de usuarios"""
        if not self.db_path.exists():
            return []
        return json.loads(self.db_path.read_text(encoding="utf-8"))


class UserPrinter:
    """Esta clase solo se encarga de imprimir usuarios"""
    
    def print_user(self, user):
        """Imprime la info del usuario de forma bonita"""
        print(f"[{user.get('id')}] {user.get('name')} - tier={user.get('tier')}")


class DiscountCalculator:
    """Esta clase solo calcula descuentos"""
    
    def __init__(self):
        self.config = DiscountConfig()
    
    def calculate_discount(self, user, total):
        """Calcula cuánto descuento le toca al usuario"""
        tier = user.get("tier", "").lower()
        
        # Si el tier no existe en las reglas, no hay descuento
        if tier not in self.config.DISCOUNT_RULES:
            return self.config.DEFAULT_DISCOUNT
        
        # Sacamos la regla para ese tier
        rule = self.config.DISCOUNT_RULES[tier]
        
        # Si gasta más del mínimo, le damos descuento
        if total > rule["min_total"]:
            return total * rule["discount_rate"]
        
        return self.config.DEFAULT_DISCOUNT


class ShippingCalculator:
    """Esta clase solo calcula costos de envío"""
    
    def __init__(self):
        self.config = ShippingConfig()
     
  # SOLUCIÓN ANTIPATRÓN 2: Un solo método que hace el cálculo para ambos
    
    def _calculate_shipping_cost(self, weight, distance_km, shipping_config):
        """
        Método genérico que calcula envío (lo usan domestic e international).
        Ya no tenemos código duplicado.
        """
        # Costo fijo que siempre se cobra
        base_cost = shipping_config["base_cost"]
        
        # Costo que depende del peso y distancia
        variable_cost = (
            weight * self.config.WEIGHT_FACTOR + 
            (distance_km / self.config.DISTANCE_DIVISOR)
        )
        
        # Si el paquete es pesado, cobramos extra
        if shipping_config["threshold_inclusive"]:
            is_heavy = weight >= self.config.HEAVY_WEIGHT_THRESHOLD  # Usa >=
        else:
            is_heavy = weight > self.config.HEAVY_WEIGHT_THRESHOLD   # Usa >
        
        if is_heavy:
            variable_cost += shipping_config["heavy_surcharge"]
        
        return base_cost + variable_cost
    
    def calculate_domestic_shipping(self, weight, distance_km):
        """Calcula envío nacional usando el método genérico"""
        return self._calculate_shipping_cost(weight, distance_km, self.config.DOMESTIC)
    
    def calculate_international_shipping(self, weight, distance_km):
        """Calcula envío internacional usando el método genérico"""
        return self._calculate_shipping_cost(weight, distance_km, self.config.INTERNATIONAL)


# AppManager ahora solo coordina, no hace todo

class AppManager:
    """
    Ahora AppManager solo junta todo y coordina.
    No hace los cálculos ni carga archivos, solo organiza.
    """
    
    # Valores de ejemplo para las pruebas (antes estaban sueltos en el código)
    EXAMPLE_ORDER_TOTAL = 123.45
    EXAMPLE_PACKAGE_WEIGHT = 12.0
    EXAMPLE_DISTANCE_KM = 900.0
    
    def __init__(self):
        """Creamos todas las clases que vamos a necesitar"""
        self.user_repo = UserRepository()
        self.discount_calc = DiscountCalculator()
        self.shipping_calc = ShippingCalculator()
        self.printer = UserPrinter()
    
    def run(self):
        """Método principal - ahora es más simple y fácil de leer"""
        # Cargamos los usuarios
        users = self.user_repo.load_users()
        
        # Procesamos cada usuario
        for user in users:
            # Mostramos el usuario
            self.printer.print_user(user)
            
            # Calculamos su descuento
            discount = self.discount_calc.calculate_discount(user, self.EXAMPLE_ORDER_TOTAL)
            print(f"Descuento calculado: {discount:.2f}")
            
            # Calculamos costos de envío
            domestic = self.shipping_calc.calculate_domestic_shipping(
                self.EXAMPLE_PACKAGE_WEIGHT,
                self.EXAMPLE_DISTANCE_KM
            )
            international = self.shipping_calc.calculate_international_shipping(
                self.EXAMPLE_PACKAGE_WEIGHT,
                self.EXAMPLE_DISTANCE_KM
            )
            
            print(f"Envío nacional: {domestic:.2f}")
            print(f"Envío internacional: {international:.2f}")
            print()  # Espacio entre usuarios


if __name__ == "__main__":
    app = AppManager()
    app.run()


# ============================================================================
# QUÉ MEJORAMOS:
# ============================================================================
# 1. Ya no hay números mágicos - todo tiene nombre y está en config
# 2. Ya no hay código duplicado - un método calcula ambos envíos
# 3. Cada clase hace una sola cosa - más fácil de entender y arreglar
# ============================================================================
