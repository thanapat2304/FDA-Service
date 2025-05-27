from backend.db_connection import connect_aep_portal, connect_aep_DB
from backend.mock_data import PRODUCTS, BRANDS, DOCUMENTS, DOCUMENT_TYPES
from flask import render_template, request, session
from datetime import datetime, timedelta
import pymysql

# Constants for time intervals
RECENT_INTERVAL_DAYS = 7
MONTHLY_INTERVAL_DAYS = 30
CHART_INTERVAL_DAYS = 180

def data_dashboard():
    """
    Render the main dashboard page with recent documents, brand statistics, and monthly counts.
    
    Returns:
        str: Rendered HTML template with dashboard data
    """
    current_user = session.get('fda_role', None)
    recent_documents = get_documents()
    brand_names, brand_product_counts = get_chart()
    stats = get_monthly_counts()

    return render_template('dashboard.html', current_user=current_user, recent_documents=recent_documents, brand_names=brand_names, brand_product_counts=brand_product_counts, stats=stats)

def get_documents():
    """
    Retrieve recent documents from the last 7 days across all document types.
    
    Returns:
        list: List of recent documents with their details
    """
    recent_date = datetime.now() - timedelta(days=RECENT_INTERVAL_DAYS)
    
    # Filter recent documents
    recent_docs = []
    for doc in DOCUMENTS:
        doc_date = datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S')
        if doc_date >= recent_date:
            # Get product and brand info
            product = next((p for p in PRODUCTS if p['id'] == doc['product_id']), None)
            if product:
                brand = next((b for b in BRANDS if b['id'] == product['brand_id']), None)
                if brand:
                    recent_docs.append({
                        'type': next((t['name'].lower() for t in DOCUMENT_TYPES if t['id'] == doc['type_id']), 'unknown'),
                        'product_id': product['id'],
                        'product_name': product['name'],
                        'brand_name': brand['name'],
                        'brand_id': brand['id'],
                        'created_at': doc_date
                    })
    
    # Sort by date descending and limit to 10
    recent_docs.sort(key=lambda x: x['created_at'], reverse=True)
    return recent_docs[:10]

def get_chart():
    """
    Get brand statistics for chart display from the last 6 months.
    
    Returns:
        tuple: (list of brand names, list of corresponding counts)
    """
    chart_date = datetime.now() - timedelta(days=CHART_INTERVAL_DAYS)
    
    # Count documents per brand
    brand_counts = {}
    for doc in DOCUMENTS:
        doc_date = datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S')
        if doc_date >= chart_date:
            product = next((p for p in PRODUCTS if p['id'] == doc['product_id']), None)
            if product:
                brand = next((b for b in BRANDS if b['id'] == product['brand_id']), None)
                if brand:
                    brand_counts[brand['name']] = brand_counts.get(brand['name'], 0) + 1
    
    # Sort by count descending
    sorted_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)
    brand_names = [b[0] for b in sorted_brands]
    brand_product_counts = [b[1] for b in sorted_brands]
    
    return brand_names, brand_product_counts

def get_monthly_counts():
    """
    Get counts of various entities from the last month.
    
    Returns:
        dict: Counts for different entity types and total document count
    """
    monthly_date = datetime.now() - timedelta(days=MONTHLY_INTERVAL_DAYS)
    
    # Count active brands and products
    brand_count = len([b for b in BRANDS if b['status'] == 'active'])
    product_count = len([p for p in PRODUCTS if p['status'] == 'active'])
    
    # Count documents by type in the last month
    doc_counts = {'spec_count': 0, 'coa_count': 0, 'cert_count': 0, 'fda_count': 0}
    type_map = {t['id']: t['name'].lower() for t in DOCUMENT_TYPES}
    
    for doc in DOCUMENTS:
        doc_date = datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S')
        if doc_date >= monthly_date:
            doc_type = type_map.get(doc['type_id'])
            if doc_type == 'specification':
                doc_counts['spec_count'] += 1
            elif doc_type == 'coa':
                doc_counts['coa_count'] += 1
            elif doc_type == 'certificate':
                doc_counts['cert_count'] += 1
            elif doc_type == 'fda':
                doc_counts['fda_count'] += 1
    
    counts = {
        'brand_count': brand_count,
        'product_count': product_count,
        'recent_count': len(DOCUMENT_TYPES),
        **doc_counts
    }
    
    # Calculate total document count
    counts['document_count'] = sum([
        counts['spec_count'],
        counts['coa_count'],
        counts['cert_count'],
        counts['fda_count']
    ])
    
    return counts