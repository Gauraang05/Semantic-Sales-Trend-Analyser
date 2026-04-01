import requests

def test_complete_fix():
    print("=== FINAL FIX VERIFICATION ===")
    
    # Test 1: Upload data
    print("\n1. Testing data upload...")
    try:
        with open('Sales Data.csv', 'rb') as f:
            files = {'file': ('Sales Data.csv', f, 'text/csv')}
            response = requests.post('http://localhost:8000/upload-data', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Upload successful: {data.get('rows', 0)} rows")
            print(f"[OK] Columns: {data.get('columns', [])}")
            
            # Check if ProductName is in columns
            columns = data.get('columns', [])
            if 'ProductName' in columns:
                print("[SUCCESS] ProductName column found!")
            else:
                print(f"[ERROR] ProductName column missing. Found: {columns}")
        else:
            print(f"[ERROR] Upload failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Upload error: {e}")
    
    # Test 2: Check data summary
    print("\n2. Testing data summary...")
    try:
        response = requests.get('http://localhost:8000/data-summary')
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Data summary working: {data.get('total_rows', 0)} rows")
            print(f"[OK] Unique products: {data.get('unique_products', 0)}")
        else:
            print(f"[ERROR] Data summary failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Data summary error: {e}")
    
    # Test 3: Test top products endpoint
    print("\n3. Testing top products...")
    try:
        response = requests.get('http://localhost:8000/top-products')
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Top products working: {len(data.get('labels', []))} products")
        else:
            print(f"[ERROR] Top products failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Top products error: {e}")
    
    # Test 4: Test enhanced analytics
    print("\n4. Testing enhanced analytics...")
    enhanced_endpoints = [
        '/product-performance',
        '/city-performance',
        '/sales-trend-analysis',
        '/price-distribution',
        '/quantity-vs-sales'
    ]
    
    for endpoint in enhanced_endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}')
            if response.status_code == 200:
                print(f"[OK] {endpoint}: Working")
            else:
                print(f"[ERROR] {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] {endpoint}: {e}")
    
    # Test 5: Test semantic search
    print("\n5. Testing semantic search...")
    try:
        response = requests.post('http://localhost:8000/semantic-search', 
                               params={'query': 'laptop', 'top_k': 3})
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"[OK] Semantic search working: {len(results)} results")
        else:
            print(f"[ERROR] Semantic search failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Semantic search error: {e}")
    
    print("\n=== FIX VERIFICATION COMPLETE ===")
    print("If all tests show [OK], the ProductName column issue is resolved!")

if __name__ == "__main__":
    test_complete_fix()
