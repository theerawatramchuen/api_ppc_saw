# api_ppc_saw
## Installation
`D:\api_ppc_saw> python -m venv env` 

`D:\api_ppc_saw> env\scripts\activate`

(env) PS D:\api_ppc_saw> 

`pip install fastapi uvicorn polars pandas numpy scikit-learn seaborn duckdb openpyxl requests tqdm`

## Start API
`uvicorn app:app --reload`

## Testing API
`python test_api.py`

(env) PS D:\api_ppc_saw> python .\test_api.py <br>
Testing API with date=2025-06-06 and equip_id=TSWD193 <br>
✅ Received ZIP file: anomaly_results.zip (5750 KB) <br>
📁 Extracted 8 files to 'api_results/': <br>
  - anomaly_output.csv <br>
  - Distribution_by_Categories.png <br>
  - Distribution_by_Equipment_ID.png <br>
  - Interaction_Heatmap.png <br>
  - Mean_Scores_by_Categories.png <br>
  - Normalized_Anomaly_Score_Trend.png <br>
  - Normalized_ChipSizeZ1_Trend.png <br>
  - Normalized_ChipSizeZ2_Trend.png <br>
✅ All required files are present <br>
<br>
Total testing time: 134.36 seconds <br>
