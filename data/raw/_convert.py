import pandas as pd
from datetime import datetime, timedelta

def excel_serial_to_date(val):
    if pd.isna(val) or val == "":
        return ""
    try:
        f = float(val)
    except (ValueError, TypeError):
        return val
    d = datetime(1899, 12, 30) + timedelta(days=f)
    return d.strftime("%Y-%m-%d")

path = "ethiopia_fi_unified_data.xlsx"
data = pd.read_excel(path, sheet_name="ethiopia_fi_unified_data")
impact = pd.read_excel(path, sheet_name="Impact_sheet")

date_cols = ["observation_date", "period_start", "period_end", "collection_date"]
for col in date_cols:
    if col in data.columns:
        data[col] = data[col].apply(excel_serial_to_date)
    if col in impact.columns:
        impact[col] = impact[col].apply(excel_serial_to_date)

if "parent_id" not in data.columns:
    data.insert(1, "parent_id", "")

all_cols = list(dict.fromkeys(list(data.columns) + list(impact.columns)))
data = data.reindex(columns=all_cols)
impact = impact.reindex(columns=all_cols)

unified = pd.concat([data, impact], ignore_index=True).fillna("")
unified.to_csv("ethiopia_fi_unified_data.csv", index=False)
print(unified.shape, unified["record_type"].value_counts())

ref = pd.read_excel("reference_codes.xlsx").fillna("")
ref.to_csv("reference_codes.csv", index=False)
print(ref.shape)