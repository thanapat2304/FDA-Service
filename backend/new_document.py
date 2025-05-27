import os
from backend.db_connection import connect_aep_portal, connect_aep_DB
from backend.mock_data import PRODUCTS, BRANDS, DOCUMENTS, add_item
from flask import render_template, request, session, flash, redirect, url_for
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

CERTIFICATES_FOLDER = 'data/certificates'
FDA_FOLDER = 'data/fda'
COA_FOLDER = 'data/coa'
SPECIFICATIONS_FOLDER = 'data/specifications'

def document_data_new():
    current_user = session.get('fda_role', None)
    year = get_years()
    product1, product2 = get_product()

    selected_types = request.args.get('type', None)

    selected_product = None
    selected_year = None
    license_num = None
    po_num = None
    detail_note = None
    
    if request.method == 'POST':
        selected_types = request.form.get('type')
        selected_product = request.form.get('product')
        selected_year = request.form.get('year')
        license_num = request.form.get('License')
        po_num = request.form.get('PO')
        pdf_file = request.files.get('pdf_file')
        detail_note = request.form.get('Note')
        multi_files = request.files.getlist('Multi_file[]')

        if selected_types == 'Specifications':
            save_specifications_data(selected_product, detail_note, pdf_file)
        elif selected_types == 'COA':
            save_coa_data(selected_product, selected_year, po_num, detail_note, pdf_file)
        elif selected_types == 'Certificates':
            save_certificate_data(selected_product, detail_note, pdf_file)
        elif selected_types == 'FDA':
            save_fda_data(selected_product, detail_note, pdf_file, license_num)
        
        return redirect(url_for('new_document'))
    
    return render_template('new_document.html', current_user=current_user, year=year, product1=product1, product2=product2, selected_types=selected_types)

def get_years():
    current_year = datetime.now().year
    start_year = current_year - 2
    years = [{'id': str(year), 'AS_Name_year': str(year)} for year in range(current_year, start_year - 1, -1)]
    return years

def get_product():
    # Get product IDs for product1
    product1 = [str(product['id']) for product in PRODUCTS if product['status'] == 'active']
    
    # Get product code and name combinations for product2
    product2 = [
        f"{product.get('code', '')} | {product['name']}" 
        for product in PRODUCTS 
        if product['status'] == 'active'
    ]

    return product1, product2

def check_duplicate_specification(product_id, pdf_filename):
    return any(
        doc['product_id'] == int(product_id) and 
        doc['filename'] == pdf_filename and 
        doc['type_id'] == 1  # Specification type
        for doc in DOCUMENTS
    )

def check_duplicate_coa(product_id, year, po_num):
    return any(
        doc['product_id'] == int(product_id) and 
        doc.get('year') == int(year) and 
        doc.get('po_reference') == po_num and 
        doc['type_id'] == 3  # COA type
        for doc in DOCUMENTS
    )

def check_duplicate_certificate(product_id, pdf_filename):
    return any(
        doc['product_id'] == int(product_id) and 
        doc['filename'] == pdf_filename and 
        doc['type_id'] == 2  # Certificate type
        for doc in DOCUMENTS
    )

def check_duplicate_fda(product_id, license_num):
    return any(
        doc['product_id'] == int(product_id) and 
        doc.get('license_number') == license_num and 
        doc['type_id'] == 4  # FDA type
        for doc in DOCUMENTS
    )

def generate_filename(doc_type, product_id, file_extension='.pdf'):
    """Generate filename in format: type_productname_YYYYMMDD_123.pdf"""
    # Find product and brand
    product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
    if not product:
        return None
        
    brand = next((b for b in BRANDS if b['id'] == product['brand_id']), None)
    
    # Generate base filename
    current_date = datetime.now().strftime('%Y%m%d')
    product_code = product.get('code', '')
    brand_name = brand['name'] if brand else ''
    base_name = f"{doc_type}_{brand_name}_{product_code}_{current_date}"
    
    # Find the latest running number for this base name
    matching_docs = [
        doc['filename'] 
        for doc in DOCUMENTS 
        if doc['filename'].startswith(base_name) and doc['filename'].endswith(file_extension)
    ]
    
    if matching_docs:
        try:
            last_number = max(
                int(filename.split('_')[-1].replace(file_extension, ''))
                for filename in matching_docs
            )
            running_number = last_number + 1
        except (ValueError, IndexError):
            running_number = 1
    else:
        running_number = 1
    
    return f"{base_name}_{running_number:03d}{file_extension}"

def get_brand_folder(product_id, base_folder):
    """Get folder path with brand subfolder for the given product"""
    # Find product and brand
    product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
    if not product:
        return None
        
    brand = next((b for b in BRANDS if b['id'] == product['brand_id']), None)
    if not brand:
        return None
    
    # Create folder path
    brand_folder = os.path.join(base_folder, secure_filename(brand['name']))
    os.makedirs(brand_folder, exist_ok=True)
    return brand_folder

def save_specifications_data(selected_product, detail_note, pdf_file):
    if not pdf_file:
        flash('กรุณาเลือกไฟล์ PDF', 'danger')
        return False

    filename = generate_filename('SPEC', selected_product)
    if check_duplicate_specification(selected_product, filename):
        flash('ไฟล์นี้มีอยู่ในระบบแล้ว', 'danger')
        return False

    # Save file
    brand_folder = get_brand_folder(selected_product, SPECIFICATIONS_FOLDER)
    if not brand_folder:
        flash('ไม่พบข้อมูลแบรนด์', 'danger')
        return False

    file_path = os.path.join(brand_folder, filename)
    pdf_file.save(file_path)

    # Add to mock data
    new_doc = {
        'product_id': int(selected_product),
        'type_id': 1,  # Specification type
        'filename': filename,
        'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'active',
        'uploaded_by': session.get('user_id', 1),
        'note': detail_note
    }
    add_item(DOCUMENTS, new_doc)
    
    flash('บันทึกข้อมูล Specifications เรียบร้อย', 'success')
    return True

def save_certificate_data(selected_product, detail_note, pdf_file):
    if not pdf_file:
        flash('กรุณาเลือกไฟล์ PDF', 'danger')
        return False

    filename = generate_filename('CERT', selected_product)
    if check_duplicate_certificate(selected_product, filename):
        flash('ไฟล์นี้มีอยู่ในระบบแล้ว', 'danger')
        return False

    # Save file
    brand_folder = get_brand_folder(selected_product, CERTIFICATES_FOLDER)
    if not brand_folder:
        flash('ไม่พบข้อมูลแบรนด์', 'danger')
        return False

    file_path = os.path.join(brand_folder, filename)
    pdf_file.save(file_path)

    # Add to mock data
    new_doc = {
        'product_id': int(selected_product),
        'type_id': 2,  # Certificate type
        'filename': filename,
        'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'active',
        'uploaded_by': session.get('user_id', 1),
        'note': detail_note
    }
    add_item(DOCUMENTS, new_doc)
    
    flash('บันทึกข้อมูล Certificate เรียบร้อย', 'success')
    return True

def save_fda_data(selected_product, detail_note, pdf_file, license_num):
    if not pdf_file or not license_num:
        flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'danger')
        return False

    if check_duplicate_fda(selected_product, license_num):
        flash('เลขที่ใบอนุญาตนี้มีอยู่ในระบบแล้ว', 'danger')
        return False

    filename = generate_filename('FDA', selected_product)

    # Save file
    brand_folder = get_brand_folder(selected_product, FDA_FOLDER)
    if not brand_folder:
        flash('ไม่พบข้อมูลแบรนด์', 'danger')
        return False

    file_path = os.path.join(brand_folder, filename)
    pdf_file.save(file_path)

    # Add to mock data
    new_doc = {
        'product_id': int(selected_product),
        'type_id': 4,  # FDA type
        'filename': filename,
        'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'active',
        'uploaded_by': session.get('user_id', 1),
        'note': detail_note,
        'license_number': license_num
    }
    add_item(DOCUMENTS, new_doc)
    
    flash('บันทึกข้อมูล FDA เรียบร้อย', 'success')
    return True

def save_coa_data(selected_product, selected_year, po_num, detail_note, pdf_file):
    if not pdf_file or not selected_year or not po_num:
        flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'danger')
        return False

    if check_duplicate_coa(selected_product, selected_year, po_num):
        flash('ข้อมูล COA นี้มีอยู่ในระบบแล้ว', 'danger')
        return False

    filename = generate_filename('COA', selected_product)

    # Save file
    brand_folder = get_brand_folder(selected_product, COA_FOLDER)
    if not brand_folder:
        flash('ไม่พบข้อมูลแบรนด์', 'danger')
        return False

    file_path = os.path.join(brand_folder, filename)
    pdf_file.save(file_path)

    # Add to mock data
    new_doc = {
        'product_id': int(selected_product),
        'type_id': 3,  # COA type
        'filename': filename,
        'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'active',
        'uploaded_by': session.get('user_id', 1),
        'note': detail_note,
        'year': int(selected_year),
        'po_reference': po_num
    }
    add_item(DOCUMENTS, new_doc)
    
    flash('บันทึกข้อมูล COA เรียบร้อย', 'success')
    return True