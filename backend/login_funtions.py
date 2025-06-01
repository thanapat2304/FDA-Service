from flask import session, redirect, url_for, request, flash
from functools import wraps
from backend.db_connection import connect_aep_portal, execute_query_portal
from backend.audit_log import insert_audit_log
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            # Log unauthorized access attempt
            insert_audit_log(
                action_type='UNAUTHORIZED_ACCESS',
                module='Authentication',
                item_id=None,
                description=f"Unauthorized access attempt to {request.path}",
                user_id=None,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def login_route():
    try:
        # Debug form data
        logger.debug("Form data received:")
        logger.debug(f"Method: {request.method}")
        logger.debug(f"Form data: {request.form}")
        
        username = request.form.get('username')
        password = request.form.get('password')
        
        logger.debug(f"Login attempt - Username: {username}, Password length: {len(password) if password else 0}")
        
        # Validate input
        if not username or not password:
            logger.warning("Missing username or password")
            flash('กรุณากรอกชื่อผู้ใช้และรหัสผ่าน', 'danger')
            return redirect(url_for('login'))

        # Check user credentials in one query
        auth_sql = "SELECT user_id, username, role, password_hash FROM fda_users WHERE username = %s AND password_hash = %s"
        user = execute_query_portal(auth_sql, (username, password))
        
        if user and len(user) > 0:
            user = user[0]  # Get first user since execute_query_portal returns a list
            logger.info(f"Successful login for user: {username}")
            
            # Set session data with correct keys
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['fda_role'] = user['role']
            session.permanent = True

            update_sql = "UPDATE demo_users SET last_login = NOW() WHERE username = %s"
            execute_query_portal(update_sql, (username,))
            
            flash('เข้าสู่ระบบสำเร็จ', 'success')
            if user['role'] == 'viewer':
                return redirect(url_for('search'))
            else:
                return redirect(url_for('dashboard'))
        else:
            logger.warning(f"Invalid credentials for user: {username}")
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'danger')
            return redirect(url_for('login'))
            
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Login error: {str(e)}\n{error_details}")
        
        flash('เกิดข้อผิดพลาดในการเข้าสู่ระบบ กรุณาลองใหม่อีกครั้ง', 'danger')
        return redirect(url_for('login'))