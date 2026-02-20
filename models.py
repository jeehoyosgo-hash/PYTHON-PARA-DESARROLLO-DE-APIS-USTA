from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
import math

class MentalHealthBase(BaseModel):
    """Base model for mental health data validation."""
    model_config = ConfigDict(populate_by_name=True)

    entity: str = Field(..., alias="Entity")
    code: Optional[str] = Field(None, alias="Code")
    year: int = Field(..., alias="Year")

    @field_validator("code", mode="before")
    @classmethod
    def handle_nan_string(cls, v):
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    @field_validator("year")
    @classmethod
    def validate_year(cls, v):
        if v < 1900 or v > 2026:
            raise ValueError("Year must be between 1900 and 2026")
        return v

class PrevalenceModel(MentalHealthBase):
    """Model for 1- mental-illnesses-prevalence.csv"""
    schizophrenia: float = Field(..., alias="Schizophrenia disorders (share of population) - Sex: Both - Age: Age-standardized")
    depression: float = Field(..., alias="Depressive disorders (share of population) - Sex: Both - Age: Age-standardized")
    anxiety: float = Field(..., alias="Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized")
    bipolar: float = Field(..., alias="Bipolar disorders (share of population) - Sex: Both - Age: Age-standardized")
    eating_disorders: float = Field(..., alias="Eating disorders (share of population) - Sex: Both - Age: Age-standardized")

class BurdenModel(MentalHealthBase):
    """Model for 2- burden-disease-from-each-mental-illness(1).csv"""
    dalys_depressive: float = Field(..., alias="DALYs (rate) - Sex: Both - Age: Age-standardized - Cause: Depressive disorders")
    dalys_schizophrenia: float = Field(..., alias="DALYs (rate) - Sex: Both - Age: Age-standardized - Cause: Schizophrenia")
    dalys_bipolar: float = Field(..., alias="DALYs (rate) - Sex: Both - Age: Age-standardized - Cause: Bipolar disorder")
    dalys_eating: float = Field(..., alias="DALYs (rate) - Sex: Both - Age: Age-standardized - Cause: Eating disorders")
    dalys_anxiety: float = Field(..., alias="DALYs (rate) - Sex: Both - Age: Age-standardized - Cause: Anxiety disorders")

class GenericHealthModel(MentalHealthBase):
    """A more flexible model for other files with varying prevalence columns."""
    model_config = ConfigDict(extra='allow')

# --- API Models ---

class AnalysisRequest(BaseModel):
    """Request model for initiating an analysis."""
    dataset_type: str = Field(..., description="Type of dataset: 'prevalence' or 'burden'")
    variable: str = Field(..., description="Variable to analyze (e.g., 'depression', 'anxiety', 'dalys_depressive')")
    stats_type: str = Field(default="muestra", description="'poblacion' or 'muestra'")

class AnalysisResponse(BaseModel):
    """Response model for analysis results."""
    id: int
    variable: str
    n: int
    media: float
    varianza: float
    desviacion_std: float
    tipo: str
