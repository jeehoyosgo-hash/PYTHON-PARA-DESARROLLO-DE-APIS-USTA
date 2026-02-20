from fastapi import FastAPI, HTTPException
from typing import List, Dict
import os
import uvicorn

from cleaner import DataCleaner
from models import PrevalenceModel, BurdenModel, AnalysisRequest, AnalysisResponse
from analyzer import MentalHealthAnalyzer

app = FastAPI(
    title="Mental Health Data API",
    description="API for cleaning and analyzing mental health datasets.",
    version="1.0.0"
)

# In-memory history
analysis_history: Dict[int, AnalysisResponse] = {}
id_counter = 1

DATA_DIR = "Data Mental Heath"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mental Health Data API. Visit /docs for interactive documentation."}

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_data(request: AnalysisRequest):
    global id_counter
    
    if request.dataset_type.lower() == "prevalence":
        file_path = os.path.join(DATA_DIR, "1- mental-illnesses-prevalence.csv")
        model = PrevalenceModel
    elif request.dataset_type.lower() == "burden":
        file_path = os.path.join(DATA_DIR, "2- burden-disease-from-each-mental-illness(1).csv")
        model = BurdenModel
    else:
        raise HTTPException(status_code=400, detail="Invalid dataset_type. Use 'prevalence' or 'burden'.")

    try:
        cleaner = DataCleaner(model)
        cleaner.load_csv(file_path)
        df_clean = cleaner.clean()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data cleaning failed: {str(e)}")

    if request.variable not in df_clean.columns:
        valid_cols = [c for c in df_clean.columns if c not in ["entity", "code", "year"]]
        raise HTTPException(status_code=400, detail=f"Variable '{request.variable}' not found in dataset. Valid options: {valid_cols}")

    try:
        analyzer = MentalHealthAnalyzer(df_clean, request.variable)
        stats = analyzer.get_stats(type=request.stats_type)
        
        response = AnalysisResponse(
            id=id_counter,
            variable=request.variable,
            n=stats.n,
            media=round(float(stats.mu), 4),
            varianza=round(float(stats.varianza()), 4),
            desviacion_std=round(float(stats.desviacion_estandar()), 4),
            tipo=request.stats_type
        )
        
        analysis_history[id_counter] = response
        id_counter += 1
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/history", response_model=List[AnalysisResponse])
def get_history():
    return list(analysis_history.values())

@app.get("/history/{analysis_id}", response_model=AnalysisResponse)
def get_analysis_by_id(analysis_id: int):
    if analysis_id not in analysis_history:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis_history[analysis_id]

@app.delete("/history/{analysis_id}")
def delete_analysis(analysis_id: int):
    if analysis_id not in analysis_history:
        raise HTTPException(status_code=404, detail="Analysis not found")
    del analysis_history[analysis_id]
    return {"message": f"Analysis {analysis_id} deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
