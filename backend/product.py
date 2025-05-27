from backend.db_connection import connect_aep_portal, connect_aep_DB
from backend.mock_data import PRODUCTS, BRANDS, DOCUMENT_TYPES, add_item
from flask import render_template, request, session, flash, redirect, url_for
from datetime import datetime, timedelta

def data_product():
    current_user = session.get('fda_role', None)
    result = get_product()
    brand = get_brand()
    type = get_type()
    message = None
    message_type = None

    select_brand = None
    code_product = None
    name_product = None
    namethai_product = None
    select_type = None
    
    if request.method == 'POST':
        select_brand = request.form.get('brand')
        code_product = request.form.get('code')
        name_product = request.form.get('name')
        namethai_product = request.form.get('name_thai')
        select_type = request.form.get('type')

        parts_brand = [p.strip() for p in select_brand.split(' | ')]
        brand_id = int(parts_brand[0])

        parts_type = [p.strip() for p in select_type.split(' | ')]
        type_id = int(parts_type[0])

        if name_product:
            success, msg = insert_product(brand_id, code_product, name_product, namethai_product, type_id)
            flash(msg, 'success' if success else 'danger')
            return redirect(url_for('product'))

    return render_template('product.html', 
                         current_user=current_user, 
                         result=result, 
                         brand=brand, 
                         type=type, 
                         message=message, 
                         message_type=message_type)

def get_brand():
    # Return brands in format "id | name" for dropdown
    return [f"{brand['id']} | {brand['name']}" for brand in BRANDS if brand['status'] == 'active']

def get_type():
    # Return types in format "id | name" for dropdown
    return [f"{type_doc['id']} | {type_doc['name']}" for type_doc in DOCUMENT_TYPES if type_doc['status'] == 'active']

def get_product():
    # Return as list of tuples to match template expectations:
    # [product_id, code, name, name_thai, created_at]
    return [(
        product['id'],  # index 0: product_id
        product.get('code', ''),  # index 1: product_code
        product['name'],  # index 2: product_name
        product.get('name_thai', ''),  # index 3: product_name_thai
        datetime.strptime(product.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')  # index 4: product_date
    ) for product in PRODUCTS]

def insert_product(brand_id, code_product, name_product, namethai_product, type_id):
    if not name_product:
        return False, "ชื่อสินค้าห้ามว่าง"

    try:
        # Check if product code already exists
        if any(p.get('code') == code_product for p in PRODUCTS):
            return False, f"รหัสสินค้า {code_product} ซ้ำในระบบ กรุณาใช้รหัสอื่น"

        # Create new product
        new_product = {
            'name': name_product,
            'code': code_product,
            'name_thai': namethai_product,
            'brand_id': brand_id,
            'type_id': type_id,
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to mock data
        add_item(PRODUCTS, new_product)
        return True, f"เพิ่มรหัสสินค้า {code_product} ในระบบเรียบร้อย"

    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"