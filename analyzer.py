import numpy as np
from typing import List, Union
import pandas as pd

class EstadisticaBase:
    """
    Clase base para cálculos estadísticos siguiendo principios de OOP.
    """
    def __init__(self, datos: List[float]):
        if not datos:
            raise ValueError("La lista de datos no puede estar vacía.")
        self.datos = np.array(datos)
        self.n = len(self.datos)
        self.mu = np.mean(self.datos)

    def varianza(self):
        """Método abstracto para ser implementado en subclases."""
        raise NotImplementedError("Se debe usar una subclase (Poblacion o Muestra).")

    def desviacion_estandar(self):
        """La desviación estándar es la raíz de la varianza."""
        return np.sqrt(self.varianza())

class Poblacion(EstadisticaBase):
    """Implementación para una población completa (N)."""
    def varianza(self):
        return np.var(self.datos) # Numpy por defecto usa N (ddof=0)

class Muestra(EstadisticaBase):
    """Implementación para una muestra (N - 1) usando corrección de Bessel."""
    def varianza(self):
        return np.var(self.datos, ddof=1) # ddof=1 usa N - 1

class MentalHealthAnalyzer:
    """
    Clase para analizar columnas específicas de datasets de salud mental.
    """
    def __init__(self, df: pd.DataFrame, column: str):
        if column not in df.columns:
            raise ValueError(f"La columna '{column}' no existe en el DataFrame.")
        self.df = df
        self.column = column
        self.data = df[column].dropna().tolist()

    def get_stats(self, type: str = "muestra") -> Union[Poblacion, Muestra]:
        """Retorna el objeto estadístico correspondiente."""
        if type.lower() == "poblacion":
            return Poblacion(self.data)
        return Muestra(self.data)

    def report(self, type: str = "muestra"):
        """Imprime un reporte estadístico básico."""
        stats = self.get_stats(type)
        print(f"--- Reporte de Salud Mental: {self.column} ---")
        print(f"Registros analizados: {stats.n}")
        print(f"Media: {stats.mu:.4f}")
        print(f"Varianza ({type}): {stats.varianza():.4f}")
        print(f"Desviación Estándar: {stats.desviacion_estandar():.4f}")
        print("-" * 40)
