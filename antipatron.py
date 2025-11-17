# ANTIEJEMPLO EDUCATIVO: contiene antipatrones a propósito

import json
from pathlib import Path

class AppManager: 
    def __init__(self, db_path="data.json"):
        self.db_path = Path(db_path)

    def load_users(self):
        if not self.db_path.exists():
            return []
        return json.loads(self.db_path.read_text(encoding="utf-8"))

    def print_user(self, user):
        print(f"[{user.get('id')}] {user.get('name')} - tier={user.get('tier')}")

    def discount_for_order(self, user, total):
        
        if user.get("tier") == "gold" and total > 100:
            return total * 0.15
        if user.get("tier") == "silver" and total > 42:
            return total * 0.07
        return 0.0
      
    def ship_cost_domestic(self, weight, distance_km):
        base = 5
        variable = weight * 0.25 + (distance_km / 300)
        if weight > 20:  # umbral mágico
            variable += 3
        return base + variable

    def ship_cost_international(self, weight, distance_km):
        base = 7     # <- divergencia sutil
        variable = weight * 0.25 + (distance_km / 300)
        if weight >= 20:  # >= en vez de >
            variable += 4  # <- otra divergencia sutil
        return base + variable

    def run(self):
        users = self.load_users()
        for u in users:
            self.print_user(u)
            total = 123.45  # Magic number total ficticio
            d = self.discount_for_order(u, total)
            print(f"Descuento calculado: {d:.2f}")
            # Uso de funciones duplicadas
            print("Envío nacional:", self.ship_cost_domestic(12, 900))
            print("Envío internacional:", self.ship_cost_international(12, 900))

if __name__ == "__main__":
    AppManager().run()
