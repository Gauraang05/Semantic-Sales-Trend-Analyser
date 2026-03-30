import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import Visualizations from './components/Visualizations';
import EnhancedVisualizations from './components/EnhancedVisualizations';
import SemanticSearch from './components/SemanticSearch';
import { Upload, BarChart3, Search, Home, TrendingUp, Trash2, RefreshCw } from 'lucide-react';
import axios from 'axios';

function App() {
  const [dataUploaded, setDataUploaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [checkingData, setCheckingData] = useState(true);

  // Check if data exists in backend on app load
  useEffect(() => {
    const checkDataPersistence = async () => {
      try {
        const response = await axios.get('http://localhost:8000/data-summary');
        if (response.status === 200) {
          setDataUploaded(true);
        }
      } catch (err) {
        setDataUploaded(false);
      } finally {
        setCheckingData(false);
      }
    };

    checkDataPersistence();
  }, []);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home, path: '/' },
    { id: 'visualizations', label: 'Visualizations', icon: BarChart3, path: '/visualizations' },
    { id: 'enhanced', label: 'Enhanced Analytics', icon: TrendingUp, path: '/enhanced' },
    { id: 'search', label: 'Semantic Search', icon: Search, path: '/search' },
  ];

  const handleFileUpload = async (file) => {
    if (!file) return;
    
    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload-data', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setDataUploaded(true);
      setLoading(false);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading file');
      setLoading(false);
      throw err;
    }
  };

  const handleRemoveData = async () => {
    // Show confirmation dialog
    const confirmed = window.confirm(
      'Are you sure you want to remove the current dataset?\n\n' +
      'This will:\n' +
      '- Clear all uploaded data\n' +
      '- Reset all visualizations\n' +
      '- Require you to upload a new dataset\n\n' +
      'Click "OK" to proceed or "Cancel" to keep your data.'
    );
    
    if (!confirmed) {
      return; // User cancelled
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Clear data by uploading an empty request (backend will handle this)
      await axios.post('http://localhost:8000/clear-data');
      setDataUploaded(false);
      setLoading(false);
      
      // Show success message
      alert('Dataset removed successfully! You can now upload a new dataset.');
    } catch (err) {
      // If clear-data endpoint doesn't exist, we'll just reset the frontend state
      setDataUploaded(false);
      setLoading(false);
      alert('Dataset removed successfully! You can now upload a new dataset.');
    }
  };

  const handleRefreshData = async () => {
    setCheckingData(true);
    setError('');
    
    try {
      const response = await axios.get('http://localhost:8000/data-summary');
      if (response.status === 200) {
        setDataUploaded(true);
      } else {
        setDataUploaded(false);
      }
    } catch (err) {
      setDataUploaded(false);
    } finally {
      setCheckingData(false);
    }
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Sidebar menuItems={menuItems} />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="px-6 py-4">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-gray-900">
                  Semantic Sales Trend Analyzer
                </h1>
                
                <div className="flex items-center space-x-4">
                  {checkingData ? (
                    <div className="flex items-center space-x-2 text-blue-600">
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
                      <span className="text-sm font-medium">Checking data...</span>
                    </div>
                  ) : dataUploaded ? (
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center space-x-2 text-green-600">
                        <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                        <span className="text-sm font-medium">Data Loaded</span>
                      </div>
                      
                      <div className="flex items-center space-x-2 border-l pl-3">
                        <button
                          onClick={handleRefreshData}
                          className="flex items-center px-3 py-1.5 text-sm bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors"
                          title="Refresh data status"
                        >
                          <RefreshCw className="w-4 h-4 mr-1" />
                          Refresh
                        </button>
                        
                        <label className="flex items-center px-3 py-1.5 text-sm bg-green-50 text-green-600 rounded hover:bg-green-100 cursor-pointer transition-colors">
                          <Upload className="w-4 h-4 mr-1" />
                          New Data
                          <input
                            type="file"
                            accept=".csv"
                            onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0])}
                            className="hidden"
                          />
                        </label>
                        
                        <button
                          onClick={handleRemoveData}
                          className="flex items-center px-3 py-1.5 text-sm bg-red-50 text-red-600 rounded hover:bg-red-100 transition-colors"
                          title="Remove current dataset"
                        >
                          <Trash2 className="w-4 h-4 mr-1" />
                          Remove
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-2">
                      <label className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 cursor-pointer transition-colors">
                        <Upload className="w-4 h-4 mr-2" />
                        Upload CSV
                        <input
                          type="file"
                          accept=".csv"
                          onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0])}
                          className="hidden"
                        />
                      </label>
                    </div>
                  )}
                </div>
              </div>
              
              {loading && (
                <div className="mt-2 text-sm text-blue-600">
                  Processing data...
                </div>
              )}
              
              {error && (
                <div className="mt-2 text-sm text-red-600">
                  {error}
                </div>
              )}
            </div>
          </header>

          <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
            <Routes>
              <Route 
                path="/" 
                element={<Dashboard dataUploaded={dataUploaded} checkingData={checkingData} />} 
              />
              <Route 
                path="/visualizations" 
                element={<Visualizations dataUploaded={dataUploaded} checkingData={checkingData} />} 
              />
              <Route 
                path="/enhanced" 
                element={<EnhancedVisualizations dataUploaded={dataUploaded} checkingData={checkingData} />} 
              />
              <Route 
                path="/search" 
                element={<SemanticSearch dataUploaded={dataUploaded} checkingData={checkingData} />} 
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
