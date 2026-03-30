import requests

def test_semantic_search():
    print("=== Testing Semantic Search ===")
    
    # Test different search queries
    queries = ["laptop", "mouse", "keyboard", "electronics", "computer"]
    
    for query in queries:
        try:
            response = requests.post('http://localhost:8000/semantic-search', 
                                   params={'query': query, 'top_k': 5})
            
            print(f"\nQuery: '{query}'")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"Found {len(results)} results:")
                
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result.get('product_name', 'N/A')} - ${result.get('total_sales', 0):.2f} - Similarity: {result.get('similarity_score', 0):.2f}")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Request error: {e}")

def test_enhanced_analytics():
    print("\n=== Testing Enhanced Analytics Endpoints ===")
    
    endpoints = [
        ('Product Performance', '/product-performance'),
        ('City Performance', '/city-performance'),
        ('Sales Trend Analysis', '/sales-trend-analysis'),
        ('Price Distribution', '/price-distribution'),
        ('Quantity vs Sales', '/quantity-vs-sales')
    ]
    
    for name, endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}')
            print(f"{name}: {response.status_code} - {'OK' if response.status_code == 200 else 'ERROR'}")
            
            if response.status_code == 200:
                data = response.json()
                # Show sample data
                if name == 'Product Performance':
                    print(f"  Products: {len(data.get('products', []))}")
                elif name == 'Price Distribution':
                    print(f"  Price ranges: {data.get('price_ranges', [])}")
            else:
                print(f"  Error: {response.text}")
                
        except Exception as e:
            print(f"{name}: Request error - {e}")

if __name__ == "__main__":
    test_semantic_search()
    test_enhanced_analytics()
