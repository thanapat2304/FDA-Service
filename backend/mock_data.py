from datetime import datetime, timedelta

# Mock data for users
USERS = [
    {
        "user_id": 1,
        "id": 1,
        "username": "admin",
        "password": "admin123",  # In real app, this would be hashed
        "role": "admin",
        "email": "admin@example.com",
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "user_id": 2,
        "id": 2,
        "username": "user1",
        "password": "user123",
        "role": "user",
        "email": "user1@example.com",
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

# Mock data for brands
BRANDS = [
    {"id": 1, "name": "Brand A", "status": "active"},
    {"id": 2, "name": "Brand B", "status": "active"},
    {"id": 3, "name": "Brand C", "status": "inactive"}
]

# Mock data for products
PRODUCTS = [
    {
        "id": 1,
        "name": "Vitamin C 1000mg",
        "brand_id": 1,
        "type_id": 1,
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 2,
        "name": "Fish Oil Omega-3",
        "brand_id": 1,
        "type_id": 2,
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 3,
        "name": "Calcium Plus D3",
        "brand_id": 2,
        "type_id": 1,
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 4,
        "name": "Multivitamin Daily",
        "brand_id": 2,
        "type_id": 2,
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 5,
        "name": "Zinc Complex",
        "brand_id": 3,
        "type_id": 1,
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

# Mock data for document types
DOCUMENT_TYPES = [
    {"id": 1, "name": "Specification", "status": "active"},
    {"id": 2, "name": "Certificate", "status": "active"},
    {"id": 3, "name": "COA", "status": "active"},
    {"id": 4, "name": "FDA", "status": "active"}
]

# Mock data for documents
DOCUMENTS = [
    {
        "id": 1,
        "product_id": 1,
        "type_id": 1,  # Specification
        "filename": "vitamin_c_spec.pdf",
        "upload_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "uploaded_by": 1,
        "note": "Latest specification for Vitamin C"
    },
    {
        "id": 2,
        "product_id": 1,
        "type_id": 2,  # Certificate
        "filename": "vitamin_c_cert.pdf",
        "upload_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "uploaded_by": 1,
        "note": "GMP Certificate"
    },
    {
        "id": 3,
        "product_id": 2,
        "type_id": 3,  # COA
        "filename": "fish_oil_coa.pdf",
        "filename_two": "fish_oil_coa_lab.pdf",  # Additional lab report
        "upload_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "uploaded_by": 1,
        "note": "Batch #12345",
        "year": 2024,
        "po_reference": "PO-2024-001"
    },
    {
        "id": 4,
        "product_id": 3,
        "type_id": 4,  # FDA
        "filename": "calcium_fda.pdf",
        "upload_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "uploaded_by": 1,
        "note": "FDA Registration",
        "eng_name": "Calcium Plus D3 Tablets",
        "thai_name": "แคลเซียม พลัส วิตามินดี3",
        "manufacturer": "Health Products Co., Ltd.",
        "license_number": "FDA-2024-001",
        "product_type": "Dietary Supplement"
    },
    {
        "id": 5,
        "product_id": 4,
        "type_id": 1,  # Specification
        "filename": "multivitamin_spec.pdf",
        "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "uploaded_by": 2,
        "note": "Updated formulation"
    },
    {
        "id": 6,
        "product_id": 5,
        "type_id": 2,  # Certificate
        "filename": "zinc_cert.pdf",
        "upload_date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "uploaded_by": 2,
        "note": "ISO Certificate"
    },
    {
        "id": 7,
        "product_id": 1,
        "type_id": 4,  # FDA
        "filename": "vitamin_c_fda.pdf",
        "upload_date": (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "uploaded_by": 1,
        "note": "FDA Registration",
        "eng_name": "Vitamin C 1000mg Tablets",
        "thai_name": "วิตามินซี 1000 มก.",
        "manufacturer": "Health Products Co., Ltd.",
        "license_number": "FDA-2024-002",
        "product_type": "Dietary Supplement"
    }
]

# Mock data for audit log
AUDIT_LOG = [
    {
        "id": 1,
        "user_id": "admin",
        "action_type": "LOGIN",
        "module": "Authentication",
        "description": "User logged in",
        "ip_address": "127.0.0.1",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_agent": "Mozilla/5.0"
    }
]

# Helper functions to simulate database operations
def find_by_id(items, id_value):
    return next((item for item in items if item["id"] == id_value), None)

def find_by_field(items, field, value):
    return [item for item in items if item[field] == value]

def add_item(items, item):
    new_id = max(item["id"] for item in items) + 1 if items else 1
    item["id"] = new_id
    items.append(item)
    return item

def update_item(items, id_value, updates):
    item = find_by_id(items, id_value)
    if item:
        item.update(updates)
    return item

def delete_item(items, id_value):
    items[:] = [item for item in items if item["id"] != id_value] 