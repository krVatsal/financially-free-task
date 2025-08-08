# This module handles data loading and preprocessing for the Vahan Dashboard project.
import pandas as pd
from typing import Tuple, List

def load_data(filepath: str) -> pd.DataFrame:
    """Load vehicle registration data from a CSV or Excel file."""
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        raise ValueError('Unsupported file format')
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the data for analysis."""
    # Example: Standardize column names, parse dates, handle missing values
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    df = df.dropna()
    return df

def filter_data(df: pd.DataFrame, start_date: str, end_date: str, categories: List[str], manufacturers: List[str]) -> pd.DataFrame:
    """Filter data by date range, vehicle categories, and manufacturers."""
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    if categories:
        mask &= df['vehicle_category'].isin(categories)
    if manufacturers:
        mask &= df['manufacturer'].isin(manufacturers)
    return df[mask]
