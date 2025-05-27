from backend.db_connection import connect_aep_portal, connect_aep_DB
from backend.mock_data import PRODUCTS, BRANDS, DOCUMENTS
from flask import render_template, redirect, url_for, flash, session
from datetime import datetime, timedelta

def view_detail(product_id):
    """View all documents for a product"""
    current_user = session.get('fda_role', None)
    product = get_by_id(product_id)
    
    specifications = get_by_specifications(product_id)
    coas = get_by_coas(product_id)
    certificates = get_by_certificates(product_id)
    fda_licenses = get_by_fdas(product_id)
    
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
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
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

def get_by_specifications(product_id):
    # Filter specification documents
    return [(
        doc['id'],  # spec_id
        datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S'),  # specifications_date
        doc.get('note', ''),  # note
        doc['filename']  # pdf_file_path
    ) for doc in DOCUMENTS 
    if doc['product_id'] == product_id and doc['type_id'] == 1]  # type_id 1 is for specifications

def get_by_coas(product_id):
    # Filter COA documents
    return [(
        doc['id'],  # coa_id
        doc.get('year', datetime.now().year),  # year
        doc.get('po_reference', ''),  # po_reference
        doc.get('note', ''),  # note
        doc['filename'],  # coa_pdf_path_one
        doc.get('filename_two', '')  # coa_pdf_path_two
    ) for doc in DOCUMENTS 
    if doc['product_id'] == product_id and doc['type_id'] == 3]  # type_id 3 is for COA

def get_by_certificates(product_id):
    # Filter certificate documents
    return [(
        doc['id'],  # cert_id
        datetime.strptime(doc['upload_date'], '%Y-%m-%d %H:%M:%S'),  # certificates_date
        doc.get('note', ''),  # note
        doc['filename']  # certificate_pdf_path
    ) for doc in DOCUMENTS 
    if doc['product_id'] == product_id and doc['type_id'] == 2]  # type_id 2 is for certificates

def get_by_fdas(product_id):
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
    if doc['product_id'] == product_id and doc['type_id'] == 4]  # type_id 4 is for FDA