# This module contains functions for calculating growth metrics and aggregating data.
import pandas as pd
from typing import Tuple

def calculate_yoy_growth(df: pd.DataFrame, group_by: str, date_col: str = 'date', value_col: str = 'registrations') -> pd.DataFrame:
    """Calculate Year-over-Year growth for the given group."""
    df = df.copy()
    df['year'] = df[date_col].dt.year
    grouped = df.groupby([group_by, 'year'])[value_col].sum().reset_index()
    grouped['yoy_growth'] = grouped.groupby(group_by)[value_col].pct_change() * 100
    return grouped

def calculate_qoq_growth(df: pd.DataFrame, group_by: str, date_col: str = 'date', value_col: str = 'registrations') -> pd.DataFrame:
    """Calculate Quarter-over-Quarter growth for the given group."""
    df = df.copy()
    df['quarter'] = df[date_col].dt.to_period('Q')
    grouped = df.groupby([group_by, 'quarter'])[value_col].sum().reset_index()
    grouped['qoq_growth'] = grouped.groupby(group_by)[value_col].pct_change() * 100
    return grouped
