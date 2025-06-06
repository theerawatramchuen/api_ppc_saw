import os
import zipfile
import tempfile
import shutil
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import main_processor

app = FastAPI()

# Cleanup function to remove temporary directory
def cleanup_temp_dir(temp_dir: str):
    shutil.rmtree(temp_dir, ignore_errors=True)

@app.post("/analyze")
async def analyze(date: str, equip_id: str, background_tasks: BackgroundTasks):
    # Define your fixed base directory
    base_temp_dir = "D:/api_ppc_saw/temp"
    
    try:
        # Ensure base directory exists
        os.makedirs(base_temp_dir, exist_ok=True)
        
        # Create unique temporary directory under base path
        temp_dir = tempfile.mkdtemp(dir=base_temp_dir)
        
        # Run the analysis
        output_files = main_processor.run_analysis(date, equip_id, temp_dir)
        
        # Create ZIP archive path
        zip_path = os.path.join(temp_dir, "results.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in output_files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
        
        # Schedule cleanup after response is sent
        background_tasks.add_task(cleanup_temp_dir, temp_dir)
        
        # Return the ZIP file
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="anomaly_results.zip"
        )
    
    except Exception as e:
        # Clean up immediately if error occurs before response
        if 'temp_dir' in locals():
            cleanup_temp_dir(temp_dir)
        raise HTTPException(status_code=500, detail=str(e))