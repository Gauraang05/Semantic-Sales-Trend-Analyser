import React, { useState } from 'react';
import axios from 'axios';
import { Search, AlertCircle, Package, DollarSign, MapPin, TrendingUp } from 'lucide-react';

const SemanticSearch = ({ dataUploaded, checkingData }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const response = await axios.post('http://localhost:8000/semantic-search', null, {
        params: {
          query: query,
          top_k: 10
        }
      });
      
      setResults(response.data.results);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error performing search');
    } finally {
      setLoading(false);
    }
  };

  const ResultCard = ({ result, index }) => (
    <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h4 className="text-lg font-semibold text-gray-900 mb-2">
            {result.product_name}
          </h4>
          <div className="flex items-center text-sm text-gray-500 mb-2">
            <TrendingUp className="w-4 h-4 mr-1" />
            Similarity: {(result.similarity_score * 100).toFixed(1)}%
          </div>
        </div>
        <div className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">
          #{index + 1}
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="flex items-center">
          <DollarSign className="w-4 h-4 text-green-600 mr-2" />
          <div>
            <p className="text-sm text-gray-500">Total Sales</p>
            <p className="font-semibold text-gray-900">
              ${result.total_sales.toLocaleString(undefined, { maximumFractionDigits: 2 })}
            </p>
          </div>
        </div>
        
        <div className="flex items-center">
          <Package className="w-4 h-4 text-blue-600 mr-2" />
          <div>
            <p className="text-sm text-gray-500">Quantity</p>
            <p className="font-semibold text-gray-900">
              {result.total_quantity.toLocaleString()}
            </p>
          </div>
        </div>
        
        <div className="flex items-center">
          <MapPin className="w-4 h-4 text-purple-600 mr-2" />
          <div>
            <p className="text-sm text-gray-500">City</p>
            <p className="font-semibold text-gray-900">{result.city}</p>
          </div>
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
              Please upload a CSV file to use semantic search functionality.
            </p>
            <div className="bg-yellow-100 rounded-lg p-4 text-left">
              <p className="text-sm font-medium text-yellow-800 mb-2">Quick Start:</p>
              <ol className="text-sm text-yellow-700 list-decimal list-inside space-y-1">
                <li>Click "Upload CSV" in the header above</li>
                <li>Select your sales data file</li>
                <li>Wait for processing to complete</li>
                <li>Return here to search products</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Semantic Product Search</h2>
        <p className="text-gray-600 mt-2">
          Search for products using natural language queries. Try searching for things like "electronics", 
          "office supplies", or "gift items".
        </p>
      </div>

      {/* Search Form */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for products (e.g., 'laptop', 'furniture', 'clothing')..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center"
          >
            <Search className="w-4 h-4 mr-2" />
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Searching products...</p>
        </div>
      )}

      {/* Search Results */}
      {!loading && results.length > 0 && (
        <div>
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900">
              Found {results.length} similar products
            </h3>
            <p className="text-gray-600">
              Products similar to "{query}"
            </p>
          </div>
          
          <div className="space-y-4">
            {results.map((result, index) => (
              <ResultCard key={index} result={result} index={index} />
            ))}
          </div>
        </div>
      )}

      {/* No Results */}
      {!loading && query && results.length === 0 && !error && (
        <div className="text-center py-8">
          <div className="bg-gray-50 rounded-lg p-8">
            <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No Results Found
            </h3>
            <p className="text-gray-600">
              Try different keywords or check your spelling.
            </p>
          </div>
        </div>
      )}

      {/* Initial State */}
      {!query && !loading && (
        <div className="text-center py-8">
          <div className="bg-blue-50 rounded-lg p-8">
            <Search className="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-blue-900 mb-2">
              Start Searching
            </h3>
            <p className="text-blue-700">
              Enter a search query above to find similar products using AI-powered semantic search.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SemanticSearch;
