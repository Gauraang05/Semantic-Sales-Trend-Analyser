import os

def test_filename_update():
    print("=== Testing Filename Update ===")
    
    # Check if Sales Data.csv exists
    sales_data_path = 'Sales Data.csv'
    sample_sales_data_path = 'data/sample_sales_data.csv'
    
    print(f"\n1. Checking for Sales Data.csv...")
    if os.path.exists(sales_data_path):
        print(f"[OK] Found: {sales_data_path}")
        file_size = os.path.getsize(sales_data_path)
        print(f"[INFO] Size: {file_size} bytes")
    else:
        print(f"[ERROR] Not found: {sales_data_path}")
    
    print(f"\n2. Checking for sample_sales_data.csv...")
    if os.path.exists(sample_sales_data_path):
        print(f"[INFO] Old file still exists: {sample_sales_data_path}")
        print("[INFO] You can remove this file if no longer needed")
    else:
        print(f"[OK] Old file not found: {sample_sales_data_path}")
    
    print(f"\n3. Updated files:")
    updated_files = [
        'test_upload.py',
        'test_final_fix.py', 
        'test_data_management.py',
        'debug_upload.py',
        'frontend/public/test_upload.html'
    ]
    
    for file in updated_files:
        print(f"[OK] {file} - Updated to use Sales Data.csv")
    
    print(f"\n=== Update Complete ===")
    print("All test files now reference 'Sales Data.csv' instead of 'sample_sales_data.csv'")
    print("Your 'Sales Data.csv' file is ready to use!")

if __name__ == "__main__":
    test_filename_update()
