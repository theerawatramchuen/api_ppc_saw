import os
import datetime
import polars as pl
import pandas as pd
from ppclib import (
    fetch_ppc_days_back, get_data_profile, combine_ppc_dataframe,
    param_spliting, combine, anamoly_det, plot_trend, plot_trend_chipZ1, plot_trend_chipZ2,
    plot_equipid_violin, plot_violin_catagories, plot_mean_bars_catagoies, plot_heatmap
)

def run_analysis(start_date_str: str, x: str, output_dir: str):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Configure paths
    ppc_output_dir = "D:/api_ppc_saw/myfolder"#os.path.join(output_dir, "fetched_data")
    #os.makedirs(ppc_output_dir, exist_ok=True)
    ppp_path = "D:/api_ppc_saw/PPP.xlsx"#os.path.join(os.getcwd(), "PPP.xlsx")
    
    # Initialize result files list
    result_files = []
    
    # Core processing logic
    Sct = datetime.datetime.now()
    print("Start time:", Sct)

    daysback = 7
    # PASS OUTPUT DIR AS THIRD ARGUMENT
    ppc_file_list = fetch_ppc_days_back(start_date_str, daysback, ppc_output_dir)
    
    df = pl.read_excel(ppc_file_list[0])
    recipe = df['Recipe'].unique().to_list()
    equipid = df['EquipID'].unique().to_list()
    
    df4 = get_data_profile()#(ppp_path)
    df3 = combine_ppc_dataframe(ppc_file_list)
    df3, SVID, ECID = param_spliting(df3)
    
    result = combine(df3, SVID, ECID)

    ############ print (result.info()) #################################################
    
    filtered_df = result[result['EquipID'] == x] # filtered_df = result.filter(pl.col('EquipID') == x)
    anomalies_df = anamoly_det(filtered_df)
    anomalies_df = anomalies_df.sort_values(by='AnomalyScore_normalized', ascending=False)

    # Save CSV
    csv_path = os.path.join(output_dir, "anomaly_output.csv")
    anomalies_df.to_csv(csv_path, index=False)
    result_files.append(csv_path)
    
    # Generate plots
    plot_funcs = [
        (plot_trend, "Normalized_Anomaly_Score_Trend.png"),
        (plot_trend_chipZ1, "Normalized_ChipSizeZ1_Trend.png"),
        (plot_trend_chipZ2, "Normalized_ChipSizeZ2_Trend.png"),
        (plot_equipid_violin, "Distribution_by_Equipment_ID.png"),
        (lambda df: plot_violin_catagories(df, ['EquipID', 'EventDesc']), "Distribution_by_Categories.png"),
        (lambda df: plot_mean_bars_catagoies(df, ['EquipID', 'EventDesc']), "Mean_Scores_by_Categories.png"),
        (plot_heatmap, "Interaction_Heatmap.png")
    ]
    
    # Track the original working directory
    original_cwd = os.getcwd()
    
    try:
        # Change to the output directory so plots are saved directly there
        os.chdir(output_dir)
        
        for func, fname in plot_funcs:
            func(anomalies_df)  # Plot saved to output_dir
            plot_path = os.path.join(output_dir, fname)
            if os.path.exists(fname):  # Check if file exists in output_dir
                result_files.append(plot_path)
            else:
                print(f"Warning: Plot file '{fname}' not found.")
    finally:
        # Restore the original working directory
        os.chdir(original_cwd)
    
    print(f"Generated {len(result_files)} result files")
    return result_files