from backend.db_connection import connect_aep_portal, connect_aep_DB
from backend.mock_data import PRODUCTS, BRANDS, DOCUMENTS
from flask import render_template, request, session
from datetime import datetime, timedelta

def search_data():
    """Search page"""
    current_user = session.get('fda_role', None)

    selected_product = request.args.get('name_product', None)
    selected_brand = request.args.get('brand_id', '')
    selected_date = request.args.get('date_range', '')
    selected_doc_types = request.args.getlist('doc_types')
    search_performed = bool(selected_product)  # True if there's a search term

    brands = get_brands()
    products = []

    if search_performed:
        products = get_products_by_keyword(selected_product, selected_doc_types, selected_brand, selected_date)
    
    return render_template(
        'search.html',
        products=products,
        selected_product=selected_product,
        search_performed=search_performed,
        selected_doc_types=selected_doc_types,
        current_user=current_user,
        brands=brands,
        selected_date=selected_date,
        selected_brand=selected_brand
    )

def get_brands():
    # Convert mock brands to match template expectations
    brands = [
        {"BCBRAND_ID": str(brand['id']), "bcbrand_name": brand['name']}
        for brand in BRANDS
        if brand['status'] == 'active'
    ]
    
    # Add "ALL" option at the beginning
    brands.insert(0, {"BCBRAND_ID": "", "bcbrand_name": "ALL | สินค้าทั้งหมด"})
    
    return brands

def get_products_by_keyword(selected_product, selected_doc_types, selected_brand, selected_date):
    # Convert date range to cutoff date
    days_map = {
        "7days": 7,
        "30days": 30,
        "90days": 90,
        "1year": 365
    }
    cutoff_date = None
    if selected_date in days_map:
        cutoff_date = (datetime.today() - timedelta(days=days_map[selected_date])).date()

    # Filter products by brand and keyword
    filtered_products = []
    for product in PRODUCTS:
        # Skip if brand doesn't match (unless ALL brands selected)
        if selected_brand and str(product['brand_id']) != selected_brand:
            continue
            
        # Skip if product name/code doesn't match keyword
        if selected_product and selected_product.lower() not in product['name'].lower():
            if not product.get('code') or selected_product.lower() not in product['code'].lower():
                continue

        # Find brand name
        brand = next((b['name'] for b in BRANDS if b['id'] == product['brand_id']), '')

        # Count documents by type
        doc_counts = {
            'specifications_count': 0,
            'coa_count': 0,
            'certificates_count': 0,
            'fda_count': 0
        }

        for doc in DOCUMENTS:
            if doc['product_id'] != product['id'] or doc['status'] != 'active':
                continue

            # Skip if document is older than cutoff date
            if cutoff_date:
                doc_date = datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S').date()
                if doc_date < cutoff_date:
                    continue

            # Count by document type if type is selected
            if doc['type_id'] == 1 and 'specification' in selected_doc_types:
                doc_counts['specifications_count'] += 1
            elif doc['type_id'] == 2 and 'certificate' in selected_doc_types:
                doc_counts['certificates_count'] += 1
            elif doc['type_id'] == 3 and 'coa' in selected_doc_types:
                doc_counts['coa_count'] += 1
            elif doc['type_id'] == 4 and 'fda' in selected_doc_types:
                doc_counts['fda_count'] += 1

        # Only include product if it has matching documents
        if any(count > 0 for count in doc_counts.values()):
            filtered_products.append((
                product['id'],  # product_id
                product.get('code', ''),  # product_code
                product['name'],  # product_name
                brand,  # brand_name
                doc_counts['specifications_count'],
                doc_counts['coa_count'],
                doc_counts['certificates_count'],
                doc_counts['fda_count']
            ))

    return filtered_products