from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, jsonify, send_from_directory
from backend.login_funtions import login_route , login_required
from datetime import datetime, timedelta
from backend.search import search_data
from backend.documents_list import view_detail
from backend.new_document import document_data_new
from backend.brands import data_brands
from backend.product import data_product
from backend.type import data_type
from backend.dashboard import data_dashboard
from backend.users import data_users, add_user, delete_user, edit_user
from backend.audit_log import data_audit_log, log_action, insert_audit_log
from backend.documents_list_se import view_detail_se
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '000000000000000000'
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/')
def index():
    current_user = 'admin'
    return render_template('index.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_user = 'admin'
    if request.method == 'POST':
        return login_route()
    return render_template('login.html', current_user=current_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
@log_action(action_type='VIEW', module='Dashboard')
def dashboard(): 
    return data_dashboard()

@app.route('/search', methods=['GET', 'POST'])
@login_required
@log_action(action_type='SEARCH', module='Search')
def search(): 
    return search_data()

@app.route('/documents/<int:product_id>')
@login_required
@log_action(action_type='VIEW', module='Documents')
def view_documents(product_id): 
    return view_detail(product_id)

@app.route('/documents_se/<int:product_id>')
@login_required
@log_action(action_type='VIEW', module='Documents')
def view_documents_se(product_id): 
    date_range = request.args.get('date_range', '')
    doc_types = request.args.get('doc_types', '')
    doc_type_list = doc_types.split(',') if doc_types else []
    return view_detail_se(product_id, date_range, doc_type_list)

@app.route('/new_document', methods=['GET', 'POST'])
@login_required
@log_action(action_type='UPLOAD', module='Documents')
def new_document():
    return document_data_new()

@app.route('/brands', methods=['GET', 'POST'])
@login_required
@log_action(action_type='MANAGE', module='Brands')
def brands():
    return data_brands()

@app.route('/product', methods=['GET', 'POST'])
@login_required
@log_action(action_type='MANAGE', module='Products')
def product():
    return data_product()

@app.route('/demo')
def demo():

    current_user = 'admin'

    return render_template('error.html', current_user=current_user)

@app.route('/type', methods=['GET', 'POST'])
@login_required
@log_action(action_type='MANAGE', module='Types')
def type():
    return data_type()

@app.route('/files/specifications/<brand>/<filename>')
@login_required
@log_action(action_type='DOWNLOAD', module='Specifications')
def serve_spec_file(brand, filename):
    return send_from_directory('data', 'Mock_data.pdf')

@app.route('/files/certificates/<brand>/<filename>')
@login_required
@log_action(action_type='DOWNLOAD', module='Certificates')
def serve_cert_file(brand, filename):
    return send_from_directory('data', 'Mock_data.pdf')

@app.route('/files/coa/<brand>/<filename>')
@login_required
@log_action(action_type='DOWNLOAD', module='COA')
def serve_coa_file(brand, filename):
    return send_from_directory('data', 'Mock_data.pdf')

@app.route('/files/fda/<brand>/<filename>')
@login_required
@log_action(action_type='DOWNLOAD', module='FDA')
def serve_fda_file(brand, filename):
    return send_from_directory('data', 'Mock_data.pdf')

@app.route('/users')
@login_required
@log_action(action_type='VIEW', module='Users')
def users():
    return data_users()

@app.route('/users/add', methods=['POST'])
@login_required
@log_action(action_type='CREATE', module='Users')
def add_user_route():
    return add_user()

@app.route('/users/delete/<int:user_id>')
@login_required
@log_action(action_type='DELETE', module='Users')
def delete_user_route(user_id):
    return delete_user(user_id)

@app.route('/users/edit/<int:user_id>', methods=['POST'])
@login_required
@log_action(action_type='UPDATE', module='Users')
def edit_user_route(user_id):
    return edit_user(user_id)

@app.route('/audit-log')
@login_required
@log_action(action_type='VIEW', module='Audit Log')
def audit_log():
    return data_audit_log()

@app.route('/log-action', methods=['POST'])
@login_required
def log_client_action():
    data = request.get_json()
    action_type = data.get('action_type')
    module = data.get('module')
    
    user_id = session.get('username')
    ip_address = request.remote_addr
    user_agent = request.user_agent.string
    
    insert_audit_log(
        action_type=action_type,
        module=module,
        item_id=None,
        description=f"{action_type} in {module}",
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)