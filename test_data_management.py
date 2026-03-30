import requests

def test_data_management():
    print("=== Testing Data Management Features ===")
    
    # Test 1: Check if data exists
    print("\n1. Checking current data status...")
    try:
        response = requests.get('http://localhost:8000/data-summary')
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Data exists: {data.get('total_rows', 0)} rows")
        else:
            print("[INFO] No data currently loaded")
    except Exception as e:
        print(f"[ERROR] Could not check data status: {e}")
    
    # Test 2: Test clear data endpoint
    print("\n2. Testing clear data endpoint...")
    try:
        response = requests.post('http://localhost:8000/clear-data')
        if response.status_code == 200:
            print("[OK] Data cleared successfully")
        else:
            print(f"[ERROR] Clear data failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Clear data error: {e}")
    
    # Test 3: Verify data is cleared
    print("\n3. Verifying data is cleared...")
    try:
        response = requests.get('http://localhost:8000/data-summary')
        if response.status_code == 400:
            print("[OK] Data successfully cleared (no data found)")
        else:
            print("[INFO] Data still exists or endpoint error")
    except Exception as e:
        print(f"[OK] Data cleared (connection error expected): {e}")
    
    # Test 4: Re-upload data
    print("\n4. Re-uploading sample data...")
    try:
        with open('data/sample_sales_data.csv', 'rb') as f:
            files = {'file': ('sample_sales_data.csv', f, 'text/csv')}
            response = requests.post('http://localhost:8000/upload-data', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Data re-uploaded: {data.get('rows', 0)} rows")
        else:
            print(f"[ERROR] Re-upload failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Re-upload error: {e}")
    
    # Test 5: Verify data is back
    print("\n5. Verifying data is restored...")
    try:
        response = requests.get('http://localhost:8000/data-summary')
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Data restored: {data.get('total_rows', 0)} rows")
            print(f"[INFO] Columns: {data.get('columns', [])}")
        else:
            print("[ERROR] Data restoration failed")
    except Exception as e:
        print(f"[ERROR] Could not verify restoration: {e}")

if __name__ == "__main__":
    test_data_management()
