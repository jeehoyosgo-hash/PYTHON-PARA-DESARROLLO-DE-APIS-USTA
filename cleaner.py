import pandas as pd
from pydantic import ValidationError
from typing import List, Type, Dict, Any

class DataCleaner:
    """
    Generic cleaner that uses Pydantic models to validate and sanitize CSV data.
    """
    def __init__(self, model: Type):
        self.model = model
        self.raw_df = None
        self.clean_df = None
        self.errors = []

    def load_csv(self, file_path: str, **kwargs):
        """Loads a CSV file into a pandas DataFrame."""
        try:
            self.raw_df = pd.read_csv(file_path, **kwargs)
            return self.raw_df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            raise

    def clean(self) -> pd.DataFrame:
        """
        Validates each row using the Pydantic model.
        Returns a cleaned DataFrame.
        """
        if self.raw_df is None:
            raise ValueError("No data loaded. Call load_csv first.")

        records = self.raw_df.to_dict(orient="records")
        valid_records = []
        self.errors = []

        for i, row in enumerate(records):
            try:
                # Pydantic handles the alias mapping and type conversion
                obj = self.model(**row)
                # We dump back to a dict without aliases for internal use
                valid_records.append(obj.model_dump(by_alias=False)) 
            except ValidationError as e:
                self.errors.append({
                    "row": i,
                    "error": str(e),
                    "data": row
                })

        self.clean_df = pd.DataFrame(valid_records)
        if self.errors:
            print(f"Cleaned with {len(self.errors)} validation errors.")
        
        return self.clean_df

    def get_errors(self) -> List[Dict[str, Any]]:
        """Returns the list of rows that failed validation."""
        return self.errors
