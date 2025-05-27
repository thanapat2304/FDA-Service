from backend.db_connection import connect_aep_portal, connect_aep_DB
from backend.mock_data import PRODUCTS, BRANDS, DOCUMENTS
from flask import render_template, redirect, url_for, flash, session
from datetime import datetime, timedelta

def view_detail_se(product_id, date_range, doc_type_list):
    """View selected documents for a product"""
    current_user = session.get('fda_role', None)
    product = get_by_id(product_id)

    specifications = []
    coas = []
    certificates = []
    fda_licenses = []

    if 'specification' in doc_type_list:
        specifications = get_by_specifications(product_id, date_range)
    if 'coa' in doc_type_list:
        coas = get_by_coas(product_id, date_range)
    if 'certificate' in doc_type_list:
        certificates = get_by_certificates(product_id, date_range)
    if 'fda' in doc_type_list:
        fda_licenses = get_by_fdas(product_id, date_range)

    return render_template(
        'documents_list.html',
        product=product,
        specifications=specifications,
        coas=coas,
        certificates=certificates,
        fda_licenses=fda_licenses,
        current_user=current_user
    )

def get_by_id(product_id):
    # Find product in mock data
    product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
    if not product:
        return None
    
    # Find brand for the product
    brand = next((b for b in BRANDS if b['id'] == product['brand_id']), None)
    
    # Return tuple to match template expectations: [code, name, brand_name]
    return (
        product.get('code', ''),
        product['name'],
        brand['name'] if brand else ''
    )

def get_cutoff_date(date_range):
    """Helper function to get cutoff date based on date range"""
    if date_range == '7days':
        return (datetime.now() - timedelta(days=7)).date()
    elif date_range == '30days':
        return (datetime.now() - timedelta(days=30)).date()
    elif date_range == '90days':
        return (datetime.now() - timedelta(days=90)).date()
    elif date_range == '1year':
        return (datetime.now() - timedelta(days=365)).date()
    return None

def get_by_specifications(product_id, date_range):
    cutoff_date = get_cutoff_date(date_range)
    
    # Filter specification documents
    return [(
        doc['id'],  # spec_id
        datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S'),  # specifications_date
        doc.get('note', ''),  # note
        doc['filename']  # pdf_file_path
    ) for doc in DOCUMENTS 
    if doc['product_id'] == int(product_id) and 
       doc['type_id'] == 1 and  # Specification type
       doc['status'] == 'active' and
       (not cutoff_date or datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S').date() >= cutoff_date)]

def get_by_coas(product_id, date_range):
    cutoff_date = get_cutoff_date(date_range)
    
    # Filter COA documents
    return [(
        doc['id'],  # coa_id
        doc.get('year', datetime.now().year),  # year
        doc.get('po_reference', ''),  # po_reference
        doc.get('note', ''),  # note
        doc['filename'],  # coa_pdf_path_one
        doc.get('filename_two', ''),  # coa_pdf_path_two
        ''  # coa_pdf_path_three (not used in mock data)
    ) for doc in DOCUMENTS 
    if doc['product_id'] == int(product_id) and 
       doc['type_id'] == 3 and  # COA type
       doc['status'] == 'active' and
       (not cutoff_date or datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S').date() >= cutoff_date)]

def get_by_certificates(product_id, date_range):
    cutoff_date = get_cutoff_date(date_range)
    
    # Filter certificate documents
    return [(
        doc['id'],  # cert_id
        datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S'),  # certificates_date
        doc.get('note', ''),  # note
        doc['filename']  # certificate_pdf_path
    ) for doc in DOCUMENTS 
    if doc['product_id'] == int(product_id) and 
       doc['type_id'] == 2 and  # Certificate type
       doc['status'] == 'active' and
       (not cutoff_date or datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S').date() >= cutoff_date)]

def get_by_fdas(product_id, date_range):
    cutoff_date = get_cutoff_date(date_range)
    
    # Filter FDA documents
    return [(
        doc['id'],  # fda_id
        doc.get('eng_name', ''),  # eng_name
        doc.get('thai_name', ''),  # thai_name
        doc.get('manufacturer', ''),  # manufacturer
        doc.get('license_number', ''),  # license_number
        doc.get('product_type', ''),  # product_type
        datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S'),  # fda_date
        doc.get('note', ''),  # note
        doc['filename']  # fda_pdf_path
    ) for doc in DOCUMENTS 
    if doc['product_id'] == int(product_id) and 
       doc['type_id'] == 4 and  # FDA type
       doc['status'] == 'active' and
       (not cutoff_date or datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S').date() >= cutoff_date)]