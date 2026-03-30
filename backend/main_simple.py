from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import io
import os
from typing import List, Dict, Any
import json
from datetime import datetime

app = FastAPI(title="Semantic Sales Trend Analyzer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for data
sales_data = None

class DataProcessor:
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess sales data"""
        # Make a copy to avoid modifying original
        df_clean = df.copy()
        
        # Handle null values
        df_clean = df_clean.dropna()
        
        # Standardize column names
        column_mapping = {
            'Product': 'ProductName',
            'Order ID': 'OrderID',
            'Quantity Ordered': 'Quantity',
            'Price Each': 'UnitPrice',
            'Order Date': 'Date',
            'Purchase Address': 'CustomerID'
        }
        
        # Apply column mapping
        df_clean = df_clean.rename(columns=column_mapping)
        
        # Create Sales column if it doesn't exist
        if 'Sales' not in df_clean.columns:
            if 'Quantity' in df_clean.columns and 'UnitPrice' in df_clean.columns:
                df_clean['Sales'] = df_clean['Quantity'] * df_clean['UnitPrice']
            elif 'Quantity' in df_clean.columns and 'Price' in df_clean.columns:
                df_clean['Sales'] = df_clean['Quantity'] * df_clean['Price']
        
        # Extract Month and Hour from DateTime column
        date_columns = ['Date', 'DateTime', 'OrderDate', 'TransactionDate']
        date_col = None
        for col in date_columns:
            if col in df_clean.columns:
                date_col = col
                break
        
        if date_col:
            df_clean[date_col] = pd.to_datetime(df_clean[date_col])
            df_clean['Month'] = df_clean[date_col].dt.strftime('%Y-%m')
            df_clean['Hour'] = df_clean[date_col].dt.hour
        
        return df_clean

@app.get("/")
async def root():
    return {"message": "Semantic Sales Trend Analyzer API"}

@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    """Upload and process sales data"""
    global sales_data
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Clean data
        sales_data = DataProcessor.clean_data(df)
        
        return {
            "message": "Data uploaded and processed successfully",
            "rows": len(sales_data),
            "columns": list(sales_data.columns)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

@app.get("/monthly-sales")
async def get_monthly_sales():
    """Get monthly sales trend data"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    if 'Month' not in sales_data.columns:
        raise HTTPException(status_code=400, detail="Month column not found in data")
    
    monthly_data = sales_data.groupby('Month')['Sales'].sum().reset_index()
    monthly_data = monthly_data.sort_values('Month')
    
    return {
        "labels": monthly_data['Month'].astype(str).tolist(),
        "data": [float(x) for x in monthly_data['Sales'].tolist()]
    }

@app.get("/top-products")
async def get_top_products(limit: int = 10):
    """Get top selling products"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    if 'ProductName' not in sales_data.columns:
        raise HTTPException(status_code=400, detail="ProductName column not found in data")
    
    top_products = sales_data.groupby('ProductName')['Sales'].sum().reset_index()
    top_products = top_products.sort_values('Sales', ascending=False).head(limit)
    
    return {
        "labels": top_products['ProductName'].astype(str).tolist(),
        "data": [float(x) for x in top_products['Sales'].tolist()]
    }

@app.get("/sales-by-city")
async def get_sales_by_city():
    """Get sales by city"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    if 'City' not in sales_data.columns:
        raise HTTPException(status_code=400, detail="City column not found in data")
    
    city_data = sales_data.groupby('City')['Sales'].sum().reset_index()
    city_data = city_data.sort_values('Sales', ascending=False)
    
    return {
        "labels": city_data['City'].astype(str).tolist(),
        "data": [float(x) for x in city_data['Sales'].tolist()]
    }

@app.get("/sales-by-hour")
async def get_sales_by_hour():
    """Get sales by hour (modified to show day-of-week analysis since no time data)"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    # Since we only have dates, let's analyze by day of week instead
    if 'Date' in sales_data.columns:
        sales_data['DayOfWeek'] = pd.to_datetime(sales_data['Date']).dt.day_name()
        daily_data = sales_data.groupby('DayOfWeek')['Sales'].sum().reset_index()
        
        # Order days properly
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_data = daily_data.set_index('DayOfWeek').reindex(days_order).dropna().reset_index()
        
        return {
            "labels": daily_data['DayOfWeek'].tolist(),
            "data": [float(x) for x in daily_data['Sales'].tolist()],
            "chart_type": "day_of_week"
        }
    else:
        raise HTTPException(status_code=400, detail="Date column not found in data")

@app.get("/product-performance")
async def get_product_performance():
    """Get detailed product performance metrics"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    if 'ProductName' not in sales_data.columns:
        raise HTTPException(status_code=400, detail="ProductName column not found in data")
    
    product_stats = sales_data.groupby('ProductName').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Quantity': 'sum',
        'UnitPrice': 'mean'
    }).round(2)
    
    product_stats.columns = ['Total Sales', 'Avg Sale', 'Transactions', 'Total Quantity', 'Avg Price']
    product_stats = product_stats.reset_index()
    
    return {
        "products": product_stats['ProductName'].tolist(),
        "total_sales": [float(x) for x in product_stats['Total Sales'].tolist()],
        "avg_sales": [float(x) for x in product_stats['Avg Sale'].tolist()],
        "transactions": [int(x) for x in product_stats['Transactions'].tolist()],
        "quantities": [int(x) for x in product_stats['Total Quantity'].tolist()],
        "avg_prices": [float(x) for x in product_stats['Avg Price'].tolist()]
    }

@app.get("/city-performance")
async def get_city_performance():
    """Get city-wise performance with product distribution"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    if 'City' not in sales_data.columns:
        raise HTTPException(status_code=400, detail="City column not found in data")
    
    city_stats = sales_data.groupby('City').agg({
        'Sales': 'sum',
        'ProductName': 'count',
        'Quantity': 'sum'
    }).round(2)
    city_stats.columns = ['Total Sales', 'Product Count', 'Total Quantity']
    city_stats = city_stats.sort_values('Total Sales', ascending=False).head(10).reset_index()
    
    return {
        "cities": city_stats['City'].tolist(),
        "sales": [float(x) for x in city_stats['Total Sales'].tolist()],
        "product_counts": [int(x) for x in city_stats['Product Count'].tolist()],
        "quantities": [int(x) for x in city_stats['Total Quantity'].tolist()]
    }

@app.get("/sales-trend-analysis")
async def get_sales_trend_analysis():
    """Get detailed sales trend with cumulative and moving averages"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    if 'Date' not in sales_data.columns:
        raise HTTPException(status_code=400, detail="Date column not found in data")
    
    # Daily sales trend
    daily_sales = sales_data.groupby('Date')['Sales'].sum().reset_index()
    daily_sales = daily_sales.sort_values('Date')
    daily_sales['Cumulative Sales'] = daily_sales['Sales'].cumsum()
    
    # Moving average (7-day)
    daily_sales['Moving Avg'] = daily_sales['Sales'].rolling(window=7, min_periods=1).mean()
    
    return {
        "dates": [str(x) for x in daily_sales['Date'].tolist()],
        "daily_sales": [float(x) for x in daily_sales['Sales'].tolist()],
        "cumulative_sales": [float(x) for x in daily_sales['Cumulative Sales'].tolist()],
        "moving_avg": [float(x) for x in daily_sales['Moving Avg'].tolist()]
    }

@app.get("/price-distribution")
async def get_price_distribution():
    """Get price distribution analysis"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    # Create price ranges
    sales_data['Price Range'] = pd.cut(sales_data['UnitPrice'], 
                                      bins=[0, 50, 100, 500, 1000, float('inf')],
                                      labels=['< $50', '$50-100', '$100-500', '$500-1000', '>$1000'])
    
    price_dist = sales_data.groupby('Price Range').agg({
        'Sales': 'sum',
        'Quantity': 'sum'
    }).fillna(0).reset_index()
    
    return {
        "price_ranges": price_dist['Price Range'].tolist(),
        "sales": [float(x) for x in price_dist['Sales'].tolist()],
        "quantities": [int(x) for x in price_dist['Quantity'].tolist()]
    }

@app.get("/quantity-vs-sales")
async def get_quantity_vs_sales():
    """Get quantity vs sales correlation data"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    # Aggregate by product
    product_data = sales_data.groupby('ProductName').agg({
        'Quantity': 'sum',
        'Sales': 'sum'
    }).reset_index()
    
    return {
        "products": product_data['ProductName'].tolist(),
        "quantities": [int(x) for x in product_data['Quantity'].tolist()],
        "sales": [float(x) for x in product_data['Sales'].tolist()]
    }

@app.post("/semantic-search")
async def semantic_search(query: str = "", top_k: int = 5):
    """Simple text-based search (fallback when ML dependencies not available)"""
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    if 'ProductName' not in sales_data.columns:
        raise HTTPException(status_code=400, detail="ProductName column not found in data")
    
    # Simple text-based search
    query_lower = query.lower()
    product_summary = sales_data.groupby('ProductName').agg({
        'Sales': 'sum',
        'Quantity': 'sum' if 'Quantity' in sales_data.columns else 'count',
        'City': 'first' if 'City' in sales_data.columns else lambda x: 'Unknown'
    }).reset_index()
    
    # Filter products that contain the query
    filtered_products = product_summary[
        product_summary['ProductName'].str.lower().str.contains(query_lower, na=False)
    ]
    
    # If no exact matches, return top products as fallback
    if filtered_products.empty:
        filtered_products = product_summary.head(top_k)
    
    # Convert to result format
    results = []
    for _, row in filtered_products.head(top_k).iterrows():
        results.append({
            'product_name': row['ProductName'],
            'total_sales': float(row['Sales']),
            'total_quantity': int(row['Quantity']),
            'city': row['City'],
            'similarity_score': 1.0  # Perfect match for text search
        })
    
    return {"results": results}

@app.post("/clear-data")
async def clear_data():
    """Clear all uploaded data"""
    global sales_data
    sales_data = None
    return {"message": "Data cleared successfully"}

@app.get("/debug-columns")
async def debug_columns():
    """Debug endpoint to see what columns are available"""
    if sales_data is None:
        return {"error": "No data loaded"}
    
    return {
        "columns": list(sales_data.columns),
        "dtypes": {col: str(dtype) for col, dtype in sales_data.dtypes.items()},
        "sample_data": sales_data.head().to_dict('records'),
        "shape": sales_data.shape
    }

@app.get("/data-summary")
async def get_data_summary():
    """Get summary of the loaded data"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    return {
        "total_rows": int(len(sales_data)),
        "columns": list(sales_data.columns),
        "total_sales": float(sales_data['Sales'].sum()) if 'Sales' in sales_data.columns else 0.0,
        "unique_products": int(sales_data['ProductName'].nunique()) if 'ProductName' in sales_data.columns else 0,
        "unique_cities": int(sales_data['City'].nunique()) if 'City' in sales_data.columns else 0,
        "date_range": {
            "start": str(sales_data['Month'].min()) if 'Month' in sales_data.columns else None,
            "end": str(sales_data['Month'].max()) if 'Month' in sales_data.columns else None
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
