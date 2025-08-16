import os
from kaggle import api

# --- 1. Add Your Kaggle Credentials Here ---
# IMPORTANT: Replace with your actual Kaggle username and API key.
os.environ['KAGGLE_USERNAME'] = "landasrinija2448526"
os.environ['KAGGLE_KEY'] = "eadbeee0c5aafd3376acb8b032a0a7fc"

# --- 2. Define Dataset and Download Location ---
dataset = "pdavpoojan/the-rvlcdip-dataset-test"
out_dir = "data/rvl_cdip"

# --- 3. Authenticate and Download ---
try:
    # Authenticate with the Kaggle API using the credentials set above
    api.authenticate()
    print("== Authentication successful!")

    # Create the output directory if it doesn't already exist
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Downloading dataset '{dataset}'...")
    # Download the dataset files and unzip them into the specified directory
    api.dataset_download_files(dataset, path=out_dir, unzip=True)
    
    print(f"-- Done! Dataset downloaded to '{out_dir}'")

except Exception as e:
    # Handle potential errors, such as incorrect credentials
    print(f"--An error occurred: {e}")
    print("Please double-check that your Kaggle username and API key are correct.")