import requests

def test_persistence_check():
    """Test the data persistence check endpoint"""
    print("=== Testing Data Persistence Check ===")
    
    try:
        response = requests.get('http://localhost:8000/data-summary')
        
        if response.status_code == 200:
            data = response.json()
            print("[OK] Data persistence check working!")
            print(f"   Total rows: {data.get('total_rows', 'N/A')}")
            print(f"   Total sales: ${data.get('total_sales', 0):.2f}")
            print(f"   Unique products: {data.get('unique_products', 'N/A')}")
            print("   Frontend should detect this data automatically!")
        else:
            print(f"[ERROR] Data persistence check failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Connection error: {e}")

if __name__ == "__main__":
    test_persistence_check()
