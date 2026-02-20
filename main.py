import os
from cleaner import DataCleaner
from models import PrevalenceModel, BurdenModel
from analyzer import MentalHealthAnalyzer

def run_pipeline():
    print("=== Proyecto de Salud Mental - Pipeline de Análisis ===\n")

    # 1. Archivos
    data_dir = "Data Mental Heath"
    prevalence_file = os.path.join(data_dir, "1- mental-illnesses-prevalence.csv")
    burden_file = os.path.join(data_dir, "2- burden-disease-from-each-mental-illness(1).csv")

    # 2. Limpieza de Prevalencia
    print(">>> Iniciando Limpieza: Prevalencia")
    cleaner_prev = DataCleaner(PrevalenceModel)
    cleaner_prev.load_csv(prevalence_file)
    df_prev = cleaner_prev.clean()
    
    # 3. Análisis de Prevalencia (Depresión)
    print("\n>>> Iniciando Análisis: Depresión (Prevalencia)")
    analyzer_dep = MentalHealthAnalyzer(df_prev, "depression")
    analyzer_dep.report(type="muestra")
    
    # 4. Análisis de Prevalencia (Ansiedad)
    print(">>> Iniciando Análisis: Ansiedad (Prevalencia)")
    analyzer_anx = MentalHealthAnalyzer(df_prev, "anxiety")
    analyzer_anx.report(type="muestra")

    # 5. Limpieza de Burden of Disease
    print("\n>>> Iniciando Limpieza: Carga de Enfermedad (DALYs)")
    cleaner_burden = DataCleaner(BurdenModel)
    cleaner_burden.load_csv(burden_file)
    df_burden = cleaner_burden.clean()

    # 6. Análisis de Burden (Depresión)
    print("\n>>> Iniciando Análisis: Depresión (DALYs)")
    analyzer_dalys = MentalHealthAnalyzer(df_burden, "dalys_depressive")
    analyzer_dalys.report(type="muestra")

    print("\n=== Pipeline Finalizado con Éxito ===")

if __name__ == "__main__":
    run_pipeline()
