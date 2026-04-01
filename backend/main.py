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
import faiss
from sentence_transformers import SentenceTransformer
import pickle

app = FastAPI(title="Semantic Sales Trend Analyzer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for data and models
sales_data = None
embeddings_model = None
faiss_index = None
product_names = []
product_data = []

class DataProcessor:
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess sales data"""
        # Make a copy to avoid modifying original
        df_clean.columns = df_clean.columns.str.strip()
        # Normalize column names
        if 'Product' in df_clean.columns:
            df_clean.rename(columns={'Product': 'ProductName'}, inplace=True)

        if 'Quantity Ordered' in df_clean.columns:
            df_clean.rename(columns={'Quantity Ordered': 'Quantity'}, inplace=True)

        if 'Price Each' in df_clean.columns:
            df_clean.rename(columns={'Price Each': 'UnitPrice'}, inplace=True)

        if 'Order Date' in df_clean.columns:
            df_clean.rename(columns={'Order Date': 'DateTime'}, inplace=True)
        df_clean = df.copy()
        
        # Handle null values
        df_clean = df_clean.dropna()
        
        # Create Sales column if it doesn't exist (assuming Quantity and UnitPrice columns)
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

class SemanticSearchEngine:
    def __init__(self):
        self.model = None
        self.index = None
        self.product_names = []
        self.product_data = []
    
    def initialize(self, product_names: List[str], product_data: List[Dict]):
        """Initialize the semantic search engine"""
        self.product_names = product_names
        self.product_data = product_data
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create embeddings
        embeddings = self.model.encode(product_names)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar products"""
        if self.model is None or self.index is None:
            raise HTTPException(status_code=500, detail="Search engine not initialized")
        
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.product_data):
                result = self.product_data[idx].copy()
                result['similarity_score'] = float(1 / (1 + dist))  # Convert distance to similarity
                results.append(result)
        
        return results

# Initialize semantic search engine
search_engine = SemanticSearchEngine()

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
        
        # Initialize semantic search if ProductName column exists
        if 'ProductName' in sales_data.columns:
            # Aggregate product data
            product_summary = sales_data.groupby('ProductName').agg({
                'Sales': 'sum',
                'Quantity': 'sum' if 'Quantity' in sales_data.columns else 'count',
                'City': 'first' if 'City' in sales_data.columns else lambda x: 'Unknown'
            }).reset_index()
            
            product_names = product_summary['ProductName'].tolist()
            product_data = []
            
            for _, row in product_summary.iterrows():
                product_data.append({
                    'product_name': row['ProductName'],
                    'total_sales': float(row['Sales']),
                    'total_quantity': int(row['Quantity']),
                    'city': row['City']
                })
            
            search_engine.initialize(product_names, product_data)
        
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
        "labels": monthly_data['Month'].tolist(),
        "data": monthly_data['Sales'].tolist()
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
        "labels": top_products['ProductName'].tolist(),
        "data": top_products['Sales'].tolist()
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
        "labels": city_data['City'].tolist(),
        "data": city_data['Sales'].tolist()
    }

@app.get("/sales-by-hour")
async def get_sales_by_hour():
    """Get sales by hour"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    if 'Hour' not in sales_data.columns:
        raise HTTPException(status_code=400, detail="Hour column not found in data")
    
    hourly_data = sales_data.groupby('Hour')['Sales'].sum().reset_index()
    hourly_data = hourly_data.sort_values('Hour')
    
    return {
        "labels": hourly_data['Hour'].tolist(),
        "data": hourly_data['Sales'].tolist()
    }

@app.post("/semantic-search")
async def semantic_search(query: str = "", top_k: int = 5):
    """Perform semantic search on products"""
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    try:
        results = search_engine.search(query, top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/data-summary")
async def get_data_summary():
    """Get summary of the loaded data"""
    if sales_data is None:
        raise HTTPException(status_code=400, detail="No data available")
    
    return {
        "total_rows": len(sales_data),
        "columns": list(sales_data.columns),
        "total_sales": float(sales_data['Sales'].sum()) if 'Sales' in sales_data.columns else 0,
        "unique_products": sales_data['ProductName'].nunique() if 'ProductName' in sales_data.columns else 0,
        "unique_cities": sales_data['City'].nunique() if 'City' in sales_data.columns else 0,
        "date_range": {
            "start": sales_data['Month'].min() if 'Month' in sales_data.columns else None,
            "end": sales_data['Month'].max() if 'Month' in sales_data.columns else None
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
