import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { AlertCircle, TrendingUp, Package, MapPin, Clock } from 'lucide-react';

const Visualizations = ({ dataUploaded, checkingData }) => {
  const [monthlyData, setMonthlyData] = useState(null);
  const [topProductsData, setTopProductsData] = useState(null);
  const [cityData, setCityData] = useState(null);
  const [hourlyData, setHourlyData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (dataUploaded) {
      fetchAllData();
    }
  }, [dataUploaded]);

  const fetchAllData = async () => {
    setLoading(true);
    setError('');
    
    try {
      const [monthly, products, city, hourly] = await Promise.all([
        axios.get('http://localhost:8000/monthly-sales'),
        axios.get('http://localhost:8000/top-products'),
        axios.get('http://localhost:8000/sales-by-city'),
        axios.get('http://localhost:8000/sales-by-hour')
      ]);

      setMonthlyData(monthly.data);
      setTopProductsData(products.data);
      setCityData(city.data);
      setHourlyData(hourly.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error fetching visualization data');
    } finally {
      setLoading(false);
    }
  };

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
              Please upload a CSV file to view visualizations.
            </p>
            <div className="bg-yellow-100 rounded-lg p-4 text-left">
              <p className="text-sm font-medium text-yellow-800 mb-2">Quick Start:</p>
              <ol className="text-sm text-yellow-700 list-decimal list-inside space-y-1">
                <li>Click "Upload CSV" in the header above</li>
                <li>Select your sales data file</li>
                <li>Wait for processing to complete</li>
                <li>Return here to see visualizations</li>
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
          <p className="mt-2 text-gray-600">Loading visualizations...</p>
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
        <h2 className="text-2xl font-bold text-gray-900">Sales Visualizations</h2>
        <p className="text-gray-600 mt-2">Interactive charts showing your sales trends and patterns</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Monthly Sales Trend */}
        {monthlyData && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <TrendingUp className="w-5 h-5 text-blue-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Monthly Sales Trend</h3>
            </div>
            <Plot
              data={[
                {
                  x: monthlyData.labels,
                  y: monthlyData.data,
                  type: 'scatter',
                  mode: 'lines+markers',
                  name: 'Sales',
                  line: { color: '#3b82f6' },
                  marker: { color: '#3b82f6' }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { title: 'Month' },
                yaxis: { title: 'Sales ($)' },
                margin: { t: 20, r: 20, b: 60, l: 60 }
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </div>
        )}

        {/* Top Products */}
        {topProductsData && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <Package className="w-5 h-5 text-green-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Top Selling Products</h3>
            </div>
            <Plot
              data={[
                {
                  x: topProductsData.data,
                  y: topProductsData.labels,
                  type: 'bar',
                  orientation: 'h',
                  marker: { color: '#10b981' }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { title: 'Sales ($)' },
                yaxis: { title: 'Products' },
                margin: { t: 20, r: 20, b: 60, l: 120 }
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </div>
        )}

        {/* Sales by City */}
        {cityData && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <MapPin className="w-5 h-5 text-purple-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Sales by City</h3>
            </div>
            <Plot
              data={[
                {
                  x: cityData.labels,
                  y: cityData.data,
                  type: 'bar',
                  marker: { color: '#8b5cf6' }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { title: 'City' },
                yaxis: { title: 'Sales ($)' },
                margin: { t: 20, r: 20, b: 60, l: 60 }
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </div>
        )}

        {/* Sales by Hour */}
        {hourlyData && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <Clock className="w-5 h-5 text-orange-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Sales per Day</h3>
            </div>
            <Plot
              data={[
                {
                  x: hourlyData.labels,
                  y: hourlyData.data,
                  type: 'scatter',
                  mode: 'lines+markers',
                  name: 'Sales',
                  line: { color: '#f97316' },
                  marker: { color: '#f97316' }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { title: 'Day' },
                yaxis: { title: 'Sales ($)' },
                margin: { t: 20, r: 20, b: 60, l: 60 }
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default Visualizations;
