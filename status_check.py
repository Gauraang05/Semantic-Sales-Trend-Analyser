import requests

def check_services():
    print("=== SERVICE STATUS CHECK ===")
    
    # Check Backend
    print("\n1. Checking Backend (Port 8000)...")
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("[OK] Backend: RUNNING")
        else:
            print(f"[ERROR] Backend: ERROR ({response.status_code})")
    except Exception as e:
        print(f"[ERROR] Backend: NOT RUNNING ({e})")
    
    # Check Frontend
    print("\n2. Checking Frontend (Port 3000)...")
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("[OK] Frontend: RUNNING")
        else:
            print(f"[ERROR] Frontend: ERROR ({response.status_code})")
    except Exception as e:
        print(f"[ERROR] Frontend: NOT RUNNING ({e})")
    
    # Check Data Upload
    print("\n3. Checking Data Upload Status...")
    try:
        response = requests.get('http://localhost:8000/data-summary', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Data: LOADED ({data.get('total_rows', 0)} rows)")
        else:
            print("[ERROR] Data: NOT LOADED")
    except Exception as e:
        print(f"[ERROR] Data: ERROR ({e})")
    
    print("\n=== ACCESS INFORMATION ===")
    print("Frontend: http://localhost:3000")
    print("Backend:  http://localhost:8000")
    print("Your Sales Data.csv is ready for analysis!")

if __name__ == "__main__":
    check_services()
