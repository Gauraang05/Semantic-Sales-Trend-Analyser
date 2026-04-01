# 🚀 Startup Commands for Semantic Sales Analyzer

## 📋 **Quick Start Options**

### **Option 1: Python Script (Recommended)**
```bash
python start_services.py
```
**Features:**
- ✅ Automatic service detection
- ✅ Status checking
- ✅ Error handling
- ✅ Detailed feedback

### **Option 2: Batch File (Windows)**
```cmd
start_services.bat
```
**Features:**
- ✅ Simple double-click execution
- ✅ Background processes
- ✅ Basic status checking

### **Option 3: PowerShell Script (Advanced)**
```powershell
.\start_services.ps1
```
**Features:**
- ✅ Colored output
- ✅ Detailed status
- ✅ Error handling
- ✅ Service monitoring

## 🎯 **What These Commands Do:**

### **1. Stop Existing Services**
- Kills any running Python processes
- Prevents port conflicts

### **2. Start Backend**
- Changes to `backend/` directory
- Starts FastAPI server on port 8000
- Waits for initialization

### **3. Start Frontend**
- Changes to `frontend/` directory  
- Starts React development server on port 3000
- Waits for compilation (30-60 seconds)

### **4. Status Verification**
- Checks if backend is responding
- Checks if frontend is accessible
- Verifies data loading status

## 🌐 **Access Points**

Once services are running:
- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 **Data Status**

The commands will automatically detect if:
- ✅ **Sales Data.csv** is loaded (185,950 rows)
- ✅ **ProductName** column is found
- ✅ **All endpoints** are working

## 🛑 **How to Stop Services**

### **Method 1: Close Terminal**
- Simply close the terminal window
- Services will continue running in background

### **Method 2: Force Stop**
```cmd
taskkill /F /IM python.exe
```
- Stops all Python processes immediately
- Use if services become unresponsive

## ⚠️ **Troubleshooting**

### **Port Already in Use**
```cmd
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```
- Check what's using the ports
- Kill conflicting processes if needed

### **Frontend Not Loading**
- Wait 30-60 seconds for compilation
- Check for npm errors in terminal
- Ensure Node.js is installed

### **Backend Not Responding**
- Check Python dependencies: `pip install -r requirements.txt`
- Verify no syntax errors in backend code
- Check firewall/antivirus blocking

## 🎉 **Success Indicators**

When everything works, you'll see:
```
SUCCESS: Both services are running!
Frontend: http://localhost:3000
Backend:  http://localhost:8000
Your Sales Data.csv is ready for analysis!
```

## 📝 **Recommended Workflow**

1. **Run**: `python start_services.py`
2. **Wait**: 30-60 seconds for full startup
3. **Access**: http://localhost:3000
4. **Analyze**: Your Sales Data.csv with all features

**Choose the startup method that works best for your environment!** 🚀
