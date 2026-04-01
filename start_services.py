import subprocess
import sys
import time
import requests
import os

def start_services():
    print("=== Starting Semantic Sales Analyzer Services ===")
    
    # Kill existing processes
    print("\n1. Stopping existing services...")
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True, text=True)
        print("[OK] Stopped existing Python processes")
    except:
        pass
    
    # Start Backend
    print("\n2. Starting Backend...")
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Start backend in background
        backend_process = subprocess.Popen([
            sys.executable, 'main_simple.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("[OK] Backend starting on port 8000...")
        
        # Wait for backend to start
        time.sleep(3)
        
        # Check if backend is running
        try:
            response = requests.get('http://localhost:8000/', timeout=5)
            if response.status_code == 200:
                print("[OK] Backend is running!")
            else:
                print("[WARNING] Backend started but may have issues")
        except:
            print("[WARNING] Backend may still be starting...")
        
    except Exception as e:
        print(f"[ERROR] Failed to start backend: {e}")
        return
    
    # Start Frontend
    print("\n3. Starting Frontend...")
    try:
        # Change to frontend directory
        os.chdir('../frontend')
        
        # Start frontend in background
        frontend_process = subprocess.Popen([
            'npm', 'start'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("[OK] Frontend starting on port 3000...")
        
        # Wait for frontend to start
        print("[INFO] Waiting for frontend to compile (this may take 30-60 seconds)...")
        time.sleep(15)
        
        # Check if frontend is running
        max_attempts = 8
        for attempt in range(max_attempts):
            try:
                response = requests.get('http://localhost:3000/', timeout=5)
                if response.status_code == 200:
                    print("[OK] Frontend is running!")
                    break
            except:
                if attempt < max_attempts - 1:
                    print(f"[INFO] Attempt {attempt + 1}/{max_attempts} - still starting...")
                    time.sleep(5)
                else:
                    print("[WARNING] Frontend may still be compiling...")
        
    except Exception as e:
        print(f"[ERROR] Failed to start frontend: {e}")
        return
    
    # Final Status Check
    print("\n4. Final Status Check...")
    time.sleep(2)
    
    backend_running = False
    frontend_running = False
    data_loaded = False
    
    # Check backend
    try:
        response = requests.get('http://localhost:8000/', timeout=3)
        if response.status_code == 200:
            backend_running = True
            print("[OK] Backend: RUNNING")
    except:
        print("[ERROR] Backend: NOT RUNNING")
    
    # Check frontend
    try:
        response = requests.get('http://localhost:3000/', timeout=3)
        if response.status_code == 200:
            frontend_running = True
            print("[OK] Frontend: RUNNING")
    except:
        print("[ERROR] Frontend: NOT RUNNING")
    
    # Check data
    try:
        response = requests.get('http://localhost:8000/data-summary', timeout=3)
        if response.status_code == 200:
            data = response.json()
            data_loaded = True
            print(f"[OK] Data: LOADED ({data.get('total_rows', 0)} rows)")
    except:
        print("[INFO] Data: Not loaded or checking...")
    
    # Return to root directory
    os.chdir('..')
    
    # Summary
    print("\n" + "="*50)
    print("SERVICES STARTED!")
    print("="*50)
    
    if backend_running and frontend_running:
        print("SUCCESS: Both services are running!")
        print("\nAccess your application:")
        print("Frontend: http://localhost:3000")
        print("Backend:  http://localhost:8000")
        
        if data_loaded:
            print("\nYour Sales Data.csv is ready for analysis!")
        else:
            print("\nUpload Sales Data.csv when frontend is ready")
            
        print("\nTo stop services:")
        print("1. Close this terminal")
        print("2. Or run: taskkill /F /IM python.exe")
        
    else:
        print("ISSUE: Some services failed to start")
        print("Check the error messages above")
    
    print("="*50)

if __name__ == "__main__":
    start_services()
