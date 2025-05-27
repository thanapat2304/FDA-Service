from backend.db_connection import connect_aep_portal, connect_aep_DB
from backend.mock_data import DOCUMENT_TYPES, add_item
from flask import render_template, request, session, flash, redirect, url_for
from datetime import datetime, timedelta

def data_type():
    current_user = session.get('fda_role', None)
    result = get_type()
    message = None
    message_type = None

    if request.method == 'POST':
        name_type = request.form.get('name')
        if name_type:
            success, msg = insert_type(name_type)
            flash(msg, 'success' if success else 'danger')
            return redirect(url_for('type'))

    return render_template('type.html', 
                         current_user=current_user, 
                         result=result,
                         message=message,
                         message_type=message_type)

def get_type():
    # Return as list of tuples to match template expectations: [type_id, type_name, type_date]
    return [(
        type_doc['id'],  # index 0: BCTYPE_ID
        type_doc['name'],  # index 1: bctype_name
        datetime.strptime(type_doc.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')  # index 2: bctype_date as datetime object
    ) for type_doc in DOCUMENT_TYPES]

def insert_type(name_type):
    if not name_type:
        return False, "ชื่อประเภทห้ามว่าง"

    try:
        # Check if type name already exists
        if any(type_doc['name'].lower() == name_type.lower() for type_doc in DOCUMENT_TYPES):
            return False, f"ประเภท '{name_type}' มีอยู่ในระบบแล้ว"

        # Create new type
        new_type = {
            'name': name_type,
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to mock data
        add_item(DOCUMENT_TYPES, new_type)
        return True, f"เพิ่มประเภท '{name_type}' ในระบบเรียบร้อย"

    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"