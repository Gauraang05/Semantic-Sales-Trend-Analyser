import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { AlertCircle, TrendingUp, Package, MapPin, Clock, DollarSign, BarChart3, PieChart, ScatterChart } from 'lucide-react';

const EnhancedVisualizations = ({ dataUploaded, checkingData }) => {
  const [data, setData] = useState({
    monthly: null,
    topProducts: null,
    cityData: null,
    dayOfWeekData: null,
    productPerformance: null,
    cityPerformance: null,
    salesTrend: null,
    priceDistribution: null,
    quantityVsSales: null
  });
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
      const [
        monthly,
        products,
        city,
        dayOfWeek,
        productPerf,
        cityPerf,
        trend,
        priceDist,
        qtyVsSales
      ] = await Promise.all([
        axios.get('http://localhost:8000/monthly-sales'),
        axios.get('http://localhost:8000/top-products'),
        axios.get('http://localhost:8000/sales-by-city'),
        axios.get('http://localhost:8000/sales-by-hour'),
        axios.get('http://localhost:8000/product-performance'),
        axios.get('http://localhost:8000/city-performance'),
        axios.get('http://localhost:8000/sales-trend-analysis'),
        axios.get('http://localhost:8000/price-distribution'),
        axios.get('http://localhost:8000/quantity-vs-sales')
      ]);

      setData({
        monthly: monthly.data,
        topProducts: products.data,
        cityData: city.data,
        dayOfWeekData: dayOfWeek.data,
        productPerformance: productPerf.data,
        cityPerformance: cityPerf.data,
        salesTrend: trend.data,
        priceDistribution: priceDist.data,
        quantityVsSales: qtyVsSales.data
      });
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
              Please upload a CSV file to view enhanced visualizations.
            </p>
            <div className="bg-yellow-100 rounded-lg p-4 text-left">
              <p className="text-sm font-medium text-yellow-800 mb-2">Quick Start:</p>
              <ol className="text-sm text-yellow-700 list-decimal list-inside space-y-1">
                <li>Click "Upload CSV" in the header above</li>
                <li>Select your sales data file</li>
                <li>Wait for processing to complete</li>
                <li>Return here to see enhanced analytics</li>
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
          <p className="mt-2 text-gray-600">Loading enhanced visualizations...</p>
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

  const ChartContainer = ({ title, icon: Icon, children }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-4">
        <Icon className="w-5 h-5 text-blue-600 mr-2" />
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      </div>
      {children}
    </div>
  );

  return (
    <div className="p-8">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Enhanced Sales Analytics</h2>
        <p className="text-gray-600 mt-2">Comprehensive insights with accurate data visualization</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Monthly Sales Trend */}
        {data.monthly && (
          <ChartContainer title="Monthly Sales Trend" icon={TrendingUp}>
            <Plot
              data={[
                {
                  x: data.monthly.labels,
                  y: data.monthly.data,
                  type: 'scatter',
                  mode: 'lines+markers',
                  name: 'Monthly Sales',
                  line: { color: '#3b82f6', width: 3 },
                  marker: { color: '#3b82f6', size: 8 }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { title: 'Month', tickangle: -45 },
                yaxis: { 
                  title: 'Sales ($)',
                  tickformat: '$,.0f'
                },
                margin: { t: 20, r: 20, b: 80, l: 80 },
                hovertemplate: '<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>'
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </ChartContainer>
        )}

        {/* Top Products */}
        {data.topProducts && (
          <ChartContainer title="Top Selling Products by Revenue" icon={Package}>
            <Plot
              data={[
                {
                  x: data.topProducts.data,
                  y: data.topProducts.labels,
                  type: 'bar',
                  orientation: 'h',
                  name: 'Total Sales',
                  marker: { 
                    color: data.topProducts.data,
                    colorscale: 'Blues',
                    colorbar: { title: 'Sales ($)' }
                  }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { 
                  title: 'Total Sales ($)',
                  tickformat: '$,.0f'
                },
                yaxis: { title: 'Products' },
                margin: { t: 20, r: 80, b: 80, l: 120 },
                hovertemplate: '<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>'
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </ChartContainer>
        )}

        {/* Day of Week Analysis */}
        {data.dayOfWeekData && (
          <ChartContainer title="Sales by Day of Week" icon={Clock}>
            <Plot
              data={[
                {
                  x: data.dayOfWeekData.labels,
                  y: data.dayOfWeekData.data,
                  type: 'bar',
                  name: 'Sales',
                  marker: { color: '#10b981' }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { title: 'Day of Week' },
                yaxis: { 
                  title: 'Sales ($)',
                  tickformat: '$,.0f'
                },
                margin: { t: 20, r: 20, b: 80, l: 80 },
                hovertemplate: '<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>'
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </ChartContainer>
        )}

        {/* City Performance */}
        {data.cityPerformance && (
          <ChartContainer title="Top 10 Cities by Performance" icon={MapPin}>
            <Plot
              data={[
                {
                  x: data.cityPerformance.cities,
                  y: data.cityPerformance.sales,
                  type: 'bar',
                  name: 'Sales',
                  marker: { color: '#8b5cf6' }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { 
                  title: 'Cities',
                  tickangle: -45
                },
                yaxis: { 
                  title: 'Sales ($)',
                  tickformat: '$,.0f'
                },
                margin: { t: 20, r: 20, b: 120, l: 80 },
                hovertemplate: '<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>'
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </ChartContainer>
        )}

        {/* Price Distribution */}
        {data.priceDistribution && (
          <ChartContainer title="Sales by Price Range" icon={DollarSign}>
            <Plot
              data={[
                {
                  x: data.priceDistribution.price_ranges,
                  y: data.priceDistribution.sales,
                  type: 'bar',
                  name: 'Sales',
                  marker: { color: '#f59e0b' }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { title: 'Price Range' },
                yaxis: { 
                  title: 'Sales ($)',
                  tickformat: '$,.0f'
                },
                margin: { t: 20, r: 20, b: 80, l: 80 },
                hovertemplate: '<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>'
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </ChartContainer>
        )}

        {/* Quantity vs Sales Scatter Plot */}
        {data.quantityVsSales && (
          <ChartContainer title="Quantity vs Sales Correlation" icon={ScatterChart}>
            <Plot
              data={[
                {
                  x: data.quantityVsSales.quantities,
                  y: data.quantityVsSales.sales,
                  type: 'scatter',
                  mode: 'markers+text',
                  text: data.quantityVsSales.products,
                  textposition: 'top center',
                  marker: { 
                    size: 12,
                    color: data.quantityVsSales.sales,
                    colorscale: 'Viridis',
                    colorbar: { title: 'Sales ($)' }
                  },
                  name: 'Products'
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { title: 'Total Quantity Sold' },
                yaxis: { 
                  title: 'Total Sales ($)',
                  tickformat: '$,.0f'
                },
                margin: { t: 20, r: 80, b: 80, l: 80 },
                hovertemplate: '<b>%{text}</b><br>Quantity: %{x}<br>Sales: $%{y:,.2f}<extra></extra>'
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </ChartContainer>
        )}

        {/* Sales Trend Analysis */}
        {data.salesTrend && (
          <ChartContainer title="Daily Sales Trend with Moving Average" icon={BarChart3}>
            <Plot
              data={[
                {
                  x: data.salesTrend.dates,
                  y: data.salesTrend.daily_sales,
                  type: 'bar',
                  name: 'Daily Sales',
                  marker: { color: '#3b82f6', opacity: 0.7 }
                },
                {
                  x: data.salesTrend.dates,
                  y: data.salesTrend.moving_avg,
                  type: 'scatter',
                  mode: 'lines',
                  name: '7-Day Moving Average',
                  line: { color: '#ef4444', width: 3 }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                xaxis: { 
                  title: 'Date',
                  tickangle: -45
                },
                yaxis: { 
                  title: 'Sales ($)',
                  tickformat: '$,.0f'
                },
                margin: { t: 20, r: 20, b: 100, l: 80 },
                hovertemplate: '<b>%{x}</b><br>%{fullData.name}: $%{y:,.2f}<extra></extra>'
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </ChartContainer>
        )}

        {/* Product Performance Comparison */}
        {data.productPerformance && (
          <ChartContainer title="Product Performance Metrics" icon={PieChart}>
            <Plot
              data={[
                {
                  type: 'parcoords',
                  line: { color: data.productPerformance.total_sales },
                  dimensions: [
                    {
                      label: 'Total Sales',
                      values: data.productPerformance.total_sales,
                      range: [Math.min(...data.productPerformance.total_sales), Math.max(...data.productPerformance.total_sales)]
                    },
                    {
                      label: 'Avg Sale',
                      values: data.productPerformance.avg_sales,
                      range: [Math.min(...data.productPerformance.avg_sales), Math.max(...data.productPerformance.avg_sales)]
                    },
                    {
                      label: 'Transactions',
                      values: data.productPerformance.transactions,
                      range: [Math.min(...data.productPerformance.transactions), Math.max(...data.productPerformance.transactions)]
                    },
                    {
                      label: 'Avg Price',
                      values: data.productPerformance.avg_prices,
                      range: [Math.min(...data.productPerformance.avg_prices), Math.max(...data.productPerformance.avg_prices)]
                    }
                  ],
                  tickfont: { size: 10 }
                }
              ]}
              layout={{
                responsive: true,
                autosize: true,
                margin: { t: 20, r: 20, b: 80, l: 80 },
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)'
              }}
              className="plotly-chart"
              useResizeHandler={true}
            />
          </ChartContainer>
        )}
      </div>
    </div>
  );
};

export default EnhancedVisualizations;
