# SISTEMA INTELIGENTE DE TRANSPORTE MASIVO

class ReglaConexion:
    """
    Representa una regla lógica en la base de conocimiento.
    Regla: conecta(Origen, Destino, Costo)
    """
    def __init__(self, origen, destino, costo):
        self.origen = origen
        self.destino = destino
        self.costo = costo

    def __repr__(self):
        return f"regla: conecta({self.origen}, {self.destino}, {self.costo})"

# 1. BASE DE CONOCIMIENTO (HECHOS/REGLAS)
# definimos el mapa del transporte como reglas lógicas

base_de_conocimiento = [
    ReglaConexion("Portal", "San Javier", 5),
    ReglaConexion("San Javier", "Floresta", 3),
    ReglaConexion("San Javier", "Estadio", 4),
    ReglaConexion("Floresta", "San Antonio", 2),
    ReglaConexion("Estadio", "San Antonio", 2),
    ReglaConexion("San Antonio", "Aljaraque", 3),
    ReglaConexion("Aljaraque", "Cisneros", 2),
    ReglaConexion("Cisneros", "Parque Berrio", 1),
    # Conexiones inversas (para que sea bidireccional)
    ReglaConexion("San Javier", "Portal", 5),
    ReglaConexion("Floresta", "San Javier", 3),
    ReglaConexion("Estadio", "San Javier", 4),
    ReglaConexion("San Antonio", "Floresta", 2),
    ReglaConexion("San Antonio", "Estadio", 2),
    ReglaConexion("Aljaraque", "San Antonio", 3),
    ReglaConexion("Cisneros", "Aljaraque", 2),
    ReglaConexion("Parque Berrio", "Cisneros", 1),
]

# 2. MOTOR DE INFERENCIA Y BÚSQUEDA (Algoritmo A*)

class SistemaExpertoRutas:
    def __init__(self, reglas):
        self.reglas = reglas
        self.estaciones = self._extraer_estaciones()
    
    def _extraer_estaciones(self):
        """Extrae la lista única de estaciones de las reglas"""
        estaciones = set()
        for regla in self.reglas:
            estaciones.add(regla.origen)
            estaciones.add(regla.destino)
        return list(estaciones)

    def obtener_vecinos(self, estacion):
        """
        Consulta la base de conocimiento para encontrar conexiones válidas.
        Esto simula el motor de inferencia buscando reglas que coincidan.
        """
        vecinos = []
        for regla in self.reglas:
            if regla.origen == estacion:
                vecinos.append((regla.destino, regla.costo))
        return vecinos

    def heuristica(self, estacion, meta):
        """
        Función heurística simple (distancia estimada).
        Aquí usamos un valor estimado ficticio para guiar la búsqueda.
        """
        # Estimación simple para el ejemplo (0 si es la meta, sino 1)
        if estacion == meta:
            return 0
        return 1  # Heurística admisible simple

    def buscar_mejor_ruta(self, inicio, meta):
        """
        Implementación del algoritmo A* (Búsqueda Heurística)
        """
        # Cola de prioridad: (costo_total_estimado, costo_actual, estacion, camino)
        cola = [(0, 0, inicio, [inicio])]
        visitados = set()

        print(f"\n--- Iniciando búsqueda de ruta: {inicio} -> {meta} ---")
        print("Consultando base de conocimiento...\n")

        while cola:
            # Ordenar por menor costo estimado (F = G + H)
            cola.sort(key=lambda x: x[0])
            f_actual, g_actual, estacion_actual, camino = cola.pop(0)

            if estacion_actual in visitados:
                continue
            
            visitados.add(estacion_actual)

            # Mostrar proceso de inferencia
            print(f"> Evaluando estación: {estacion_actual} (Costo acumulado: {g_actual})")

            if estacion_actual == meta:
                return camino, g_actual

            # Obtener vecinos consultando las REGLAS
            vecinos = self.obtener_vecinos(estacion_actual)
            
            for vecino, costo in vecinos:
                if vecino not in visitados:
                    g_nuevo = g_actual + costo
                    h_nuevo = self.heuristica(vecino, meta)
                    f_nuevo = g_nuevo + h_nuevo
                    nuevo_camino = camino + [vecino]
                    cola.append((f_nuevo, g_nuevo, vecino, nuevo_camino))

        return None, 0

# 3. EJECUCIÓN PRINCIPAL

if __name__ == "__main__":
    # Inicializar el sistema con las reglas
    sistema = SistemaExpertoRutas(base_de_conocimiento)

    print("=== SISTEMA INTELIGENTE DE TRANSPORTE ===")
    print("Estaciones disponibles:", ", ".join(sistema.estaciones))
    
    # Definir origen y destino (Punto A y Punto B)
    origen = "Floresta"
    destino = "San Javier"

    # Ejecutar búsqueda
    ruta, costo_total = sistema.buscar_mejor_ruta(origen, destino)

    # Mostrar resultados
    if ruta:
        print("\n=== RESULTADO ===")
        print(f"Ruta óptima encontrada: {' -> '.join(ruta)}")
        print(f"Costo total del viaje: {costo_total}")
    else:
        print("\nNo se encontró una ruta posible entre los puntos seleccionados.")
        