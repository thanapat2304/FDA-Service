from .mock_data import (
    USERS, BRANDS, PRODUCTS, DOCUMENT_TYPES, DOCUMENTS, AUDIT_LOG,
    find_by_id, find_by_field, add_item, update_item, delete_item
)
import logging

logger = logging.getLogger(__name__)

def connect_aep_portal():
    # Mock connection - always returns True
    logger.info("Using mock data connection")
    return True

def execute_query_portal(query, params=None):
    """
    Mock query execution that returns data based on the query type
    """
    query = query.strip().upper()
    
    # For SELECT queries, return mock data based on the table being queried
    if query.startswith("SELECT"):
        if "USERS" in query:
            return USERS
        elif "BRANDS" in query:
            return BRANDS
        elif "PRODUCTS" in query:
            return PRODUCTS
        elif "DOCUMENT_TYPES" in query:
            return DOCUMENT_TYPES
        elif "DOCUMENTS" in query:
            return DOCUMENTS
        elif "AUDIT_LOG" in query:
            return AUDIT_LOG
        return []
    
    # For other queries (INSERT, UPDATE, DELETE), return None as per original function
    return None

def connect_aep_DB():
    # Mock connection - always returns True
    logger.info("Using mock data connection for AEP_DB")
    return True