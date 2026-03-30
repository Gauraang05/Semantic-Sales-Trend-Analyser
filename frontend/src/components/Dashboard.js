import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, Package, MapPin, DollarSign, AlertCircle } from 'lucide-react';

const Dashboard = ({ dataUploaded, checkingData }) => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (dataUploaded) {
      fetchSummary();
    }
  }, [dataUploaded]);

  const fetchSummary = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get('http://localhost:8000/data-summary');
      setSummary(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error fetching data summary');
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ icon: Icon, title, value, color = 'blue' }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center">
        <div className={`p-3 rounded-full bg-${color}-100`}>
          <Icon className={`w-6 h-6 text-${color}-600`} />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  );

  if (checkingData) {
    return (
      <div className="p-8">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p className="mt-2 text-gray-600">Checking for existing data...</p>
        </div>
      </div>
    );
  }

  if (!dataUploaded) {
    return (
      <div className="p-8">
        <div className="max-w-2xl mx-auto text-center">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-8">
            <AlertCircle className="w-12 h-12 text-yellow-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-yellow-800 mb-2">
              No Data Available
            </h3>
            <p className="text-yellow-700 mb-4">
              Please upload a CSV file to start analyzing your sales data.
            </p>
            <div className="bg-yellow-100 rounded-lg p-4 text-left">
              <p className="text-sm font-medium text-yellow-800 mb-2">Quick Start:</p>
              <ol className="text-sm text-yellow-700 list-decimal list-inside space-y-1">
                <li>Click "Upload CSV" in the header above</li>
                <li>Select the sample data file or your own CSV</li>
                <li>Wait for processing to complete</li>
                <li>Return here to see insights</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="p-8">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p className="mt-2 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Dashboard Overview</h2>
        <p className="text-gray-600 mt-2">Key metrics and insights from your sales data</p>
      </div>

      {summary && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatCard
              icon={DollarSign}
              title="Total Sales"
              value={`$${summary.total_sales.toLocaleString(undefined, { maximumFractionDigits: 2 })}`}
              color="green"
            />
            <StatCard
              icon={Package}
              title="Unique Products"
              value={summary.unique_products.toLocaleString()}
              color="blue"
            />
            <StatCard
              icon={MapPin}
              title="Cities"
              value={summary.unique_cities.toLocaleString()}
              color="purple"
            />
            <StatCard
              icon={TrendingUp}
              title="Total Records"
              value={summary.total_rows.toLocaleString()}
              color="orange"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Information</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Rows:</span>
                  <span className="font-medium">{summary.total_rows.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Columns:</span>
                  <span className="font-medium">{summary.columns.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Date Range:</span>
                  <span className="font-medium">
                    {summary.date_range.start && summary.date_range.end
                      ? `${summary.date_range.start} to ${summary.date_range.end}`
                      : 'N/A'}
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Columns</h3>
              <div className="flex flex-wrap gap-2">
                {summary.columns.map((column) => (
                  <span
                    key={column}
                    className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                  >
                    {column}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
