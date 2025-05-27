from backend.db_connection import connect_aep_portal
from backend.mock_data import AUDIT_LOG, add_item
from flask import render_template, request, session, flash
from datetime import datetime
from functools import wraps

def data_audit_log():
    current_user = session.get('fda_role', None)
    result = get_audit_logs()
    return render_template('audit_log.html', current_user=current_user, result=result)

def get_audit_logs():
    # Return mock audit logs
    return [{
        'log_id': log['id'],
        'user_id': log['user_id'],
        'action_type': log['action_type'],
        'module': log['module'],
        'record_id': None,
        'action_detail': log['description'],
        'ip_address': log['ip_address'],
        'user_agent': log['user_agent'],
        'action_date': datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S') if log['timestamp'] else None
    } for log in AUDIT_LOG]

def insert_audit_log(action_type, module, item_id, description, user_id, ip_address, user_agent=None):
    if not action_type or not module:
        return False

    try:
        # Create new audit log entry
        new_log = {
            'user_id': user_id,
            'action_type': action_type,
            'module': module,
            'item_id': item_id,
            'description': description,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to mock data
        add_item(AUDIT_LOG, new_log)
        return True
    except Exception as e:
        print(f"Error inserting audit log: {str(e)}")
        return False

def log_action(action_type, module):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('username', None)
            ip_address = request.remote_addr
            user_agent = request.user_agent.string
            
            # Get item_id from kwargs if it exists
            item_id = kwargs.get('product_id') or kwargs.get('user_id') or None
            
            # Create description based on the action
            description = f"{action_type} in {module}"
            if item_id:
                description += f" (ID: {item_id})"
            
            # Log the action
            insert_audit_log(
                action_type=action_type,
                module=module,
                item_id=item_id,
                description=description,
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator 