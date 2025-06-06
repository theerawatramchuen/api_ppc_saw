import requests
import zipfile
import os
import time  # Added for timing functionality

# Configuration
API_URL = "http://localhost:8000/analyze"
DATE = "2025-06-06"
EQUIP_ID = "TSWD193"
OUTPUT_ZIP = "anomaly_results.zip"
EXTRACT_DIR = "api_results"

def test_api():
    start_time = time.time()  # Record start time
    print(f"Testing API with date={DATE} and equip_id={EQUIP_ID}")
    
    try:
        # Send POST request to API
        response = requests.post(
            API_URL,
            params={"date": DATE, "equip_id": EQUIP_ID}
        )
        
        # Check for successful response
        if response.status_code != 200:
            print(f"❌ Error: Received status code {response.status_code}")
            print(f"Response content: {response.text[:500]}...")
            return
        
        # Save the ZIP file
        with open(OUTPUT_ZIP, "wb") as f:
            f.write(response.content)
        print(f"✅ Received ZIP file: {OUTPUT_ZIP} ({len(response.content)//1024} KB)")
        
        # Extract the contents
        os.makedirs(EXTRACT_DIR, exist_ok=True)
        with zipfile.ZipFile(OUTPUT_ZIP, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
        
        # List extracted files
        extracted_files = os.listdir(EXTRACT_DIR)
        print(f"📁 Extracted {len(extracted_files)} files to '{EXTRACT_DIR}/':")
        for file in extracted_files:
            print(f"  - {file}")
        
        # Check for expected files
        expected_files = [
            "anomaly_output.csv",
            "Normalized_Anomaly_Score_Trend.png",
            "Normalized_ChipSizeZ1_Trend.png",
            "Normalized_ChipSizeZ2_Trend.png",
            "Distribution_by_Equipment_ID.png",
            "Distribution_by_Categories.png",
            "Mean_Scores_by_Categories.png",
            "Interaction_Heatmap.png",
            # Debug files
            "full_result.csv",
            "SVID_debug.csv",
            "ECID_debug.csv"
        ]
        
        # Check only for required files
        required_files = expected_files[:7]
        missing_files = [f for f in required_files if f not in extracted_files]
        
        if missing_files:
            print("⚠️  Missing required files:")
            for f in missing_files:
                print(f"  - {f}")
        else:
            print("✅ All required files are present")
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
    finally:
        # Calculate and display total duration
        duration = time.time() - start_time
        print(f"\nTotal testing time: {duration:.2f} seconds")

if __name__ == "__main__":
    test_api()