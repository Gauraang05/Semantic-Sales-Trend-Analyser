import requests
import io
import pandas as pd

# Read the sample CSV
df = pd.read_csv('Sales Data.csv')
print("Original columns:", df.columns.tolist())
print("Sample data:")
print(df.head())

# Upload to backend
try:
    files = {'file': ('Sales Data.csv', open('Sales Data.csv', 'rb'), 'text/csv')}
    response = requests.post('http://localhost:8000/upload-data', files=files)

    print("\nUpload response:")
    print(response.status_code)
    print(response.json())
    
    if response.status_code == 200:
        print("\n✅ Upload successful!")
    else:
        print("\n❌ Upload failed!")
        
except Exception as e:
    print(f"\n❌ Error during upload: {e}")

# Test debug endpoint
try:
    debug_response = requests.get('http://localhost:8000/debug-columns')
    print("\nDebug response:")
    print(debug_response.status_code)
    print(debug_response.json())
except Exception as e:
    print(f"\n❌ Error getting debug info: {e}")
