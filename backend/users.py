from backend.db_connection import connect_aep_portal
from backend.mock_data import USERS, add_item, find_by_id, find_by_field
from flask import render_template, request, session, flash, redirect, url_for
from datetime import datetime

def data_users():
    """User management page"""
    current_user = session.get('fda_role', None)
    
    # Only admin can access this page
    if current_user != 'admin':
        flash("คุณไม่มีสิทธิ์เข้าถึงหน้านี้", "danger")
        return redirect(url_for('dashboard'))
    
    users = get_users()
    return render_template('users.html', current_user=current_user, users=users)

def get_users():
    """Get all users from mock data"""
    return [{
        'user_id': user['user_id'],
        'username': user['username'],
        'role': user['role'],
        'created_at': user['created_at'],
        'last_login': user.get('last_login', None)
    } for user in USERS if user['status'] == 'active']

def add_user():
    """Add new user"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if not username or not password or not role:
            flash("กรุณากรอกข้อมูลให้ครบถ้วน", "danger")
            return redirect(url_for('users'))
            
        # Check if username already exists
        if any(u['username'] == username for u in USERS):
            flash("ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว", "danger")
            return redirect(url_for('users'))
        
        # Create new user
        new_user = {
            'username': username,
            'password': password,  # In real app, this would be hashed
            'role': role,
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to mock data
        add_item(USERS, new_user)
        flash("เพิ่มผู้ใช้งานสำเร็จ", "success")
        return redirect(url_for('users'))
    
    return redirect(url_for('users'))

def delete_user(user_id):
    """Delete user"""
    if not user_id:
        flash("ไม่พบข้อมูลผู้ใช้", "danger")
        return redirect(url_for('users'))
        
    # Find user in mock data
    user = find_by_id(USERS, int(user_id))
    if not user:
        flash("ไม่พบข้อมูลผู้ใช้", "danger")
        return redirect(url_for('users'))
    
    # Mark user as inactive instead of deleting
    user['status'] = 'inactive'
    user['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    flash("ลบผู้ใช้งานสำเร็จ", "success")
    return redirect(url_for('users'))

def edit_user(user_id):
    """Edit user"""
    if request.method == 'POST':
        password = request.form.get('password')
        role = request.form.get('role')
        
        if not password or not role:
            flash("กรุณากรอกข้อมูลให้ครบถ้วน", "danger")
            return redirect(url_for('users'))
            
        # Find user in mock data
        user = find_by_id(USERS, int(user_id))
        if not user:
            flash("ไม่พบข้อมูลผู้ใช้", "danger")
            return redirect(url_for('users'))
        
        # Update user
        user['password'] = password  # In real app, this would be hashed
        user['role'] = role
        user['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        flash("แก้ไขข้อมูลผู้ใช้สำเร็จ", "success")
        return redirect(url_for('users'))
    
    return redirect(url_for('users')) 