import requests
import os

def test_upload():
    print("=== Testing File Upload ===")
    
    # Check if file exists
    file_path = 'data/sample_sales_data.csv'
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return False
    
    print(f"[OK] File exists: {file_path}")
    
    # Check file size
    file_size = os.path.getsize(file_path)
    print(f"[INFO] File size: {file_size} bytes")
    
    # Test backend connection
    try:
        response = requests.get('http://localhost:8000/')
        if response.status_code == 200:
            print("[OK] Backend is running")
        else:
            print(f"[ERROR] Backend returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Cannot connect to backend: {e}")
        return False
    
    # Test upload
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            response = requests.post('http://localhost:8000/upload-data', files=files)
        
        print(f"[UPLOAD] Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("[SUCCESS] Upload successful!")
            print(f"[DATA] Rows processed: {data.get('rows', 'N/A')}")
            print(f"[DATA] Columns: {data.get('columns', 'N/A')}")
            return True
        else:
            print(f"[ERROR] Upload failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Upload error: {e}")
        return False

def test_data_insights():
    print("\n=== Testing Data Insights ===")
    
    endpoints = [
        ('Data Summary', '/data-summary'),
        ('Monthly Sales', '/monthly-sales'),
        ('Top Products', '/top-products'),
        ('Sales by City', '/sales-by-city'),
        ('Day of Week', '/sales-by-hour'),
        ('Product Performance', '/product-performance')
    ]
    
    for name, endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}')
            if response.status_code == 200:
                print(f"[OK] {name}: Working")
            else:
                print(f"[ERROR] {name}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[ERROR] {name}: Error - {e}")

if __name__ == "__main__":
    if test_upload():
        test_data_insights()
    else:
        print("\n[ERROR] Cannot test insights until upload is fixed")
