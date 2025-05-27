from backend.db_connection import connect_aep_portal, connect_aep_DB
from backend.mock_data import BRANDS, add_item
from flask import render_template, request, session, flash, jsonify, redirect, url_for
from datetime import datetime, timedelta
from backend.audit_log import insert_audit_log

def data_brands():
    current_user = session.get('fda_role', None)
    result = get_brand()
    message = None
    message_type = None

    if request.method == 'POST':
        name_brand = request.form.get('name')
        if name_brand:
            success, msg = insert_brand(name_brand)
            flash(msg, 'success' if success else 'danger')
            return redirect(url_for('brands'))
    
    return render_template('brands.html', 
                         current_user=current_user, 
                         result=result,
                         message=message,
                         message_type=message_type)

def get_brand():
    # Convert mock data to match the expected format from database
    # Return as list of tuples to match template expectations: [brand_id, brand_name, brand_date]
    return [(
        brand['id'],  # index 0: BCBRAND_ID
        brand['name'],  # index 1: bcbrand_name
        datetime.strptime(brand.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')  # index 2: bcbrand_date as datetime object
    ) for brand in BRANDS]

def insert_brand(name_brand):
    if not name_brand:
        return False, "Brand name cannot be empty"

    try:
        # Check if brand name already exists
        if any(brand['name'].lower() == name_brand.lower() for brand in BRANDS):
            return False, f"แบรนด์ '{name_brand}' มีอยู่ในระบบแล้ว"

        # Create new brand
        new_brand = {
            'name': name_brand,
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to mock data
        add_item(BRANDS, new_brand)
        return True, f"เพิ่มแบรนด์ '{name_brand}' ในระบบเรียบร้อย"

    except Exception as e:
        return False, f"Error adding brand: {str(e)}"