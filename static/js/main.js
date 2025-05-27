/**
 * FDA Document Management System
 * main.js - Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    initTooltips();
    
    // Initialize form elements
    initFormElements();
    
    // Setup product selection on document form
    setupProductSelection();
});

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form elements like file input labels and select2
 */
function initFormElements() {
    // Update file input labels with filename when file is selected
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', updateFileLabel);
    });
    
    // Setup confirmation modals
    setupConfirmationModals();
}

/**
 * Update file input label with selected filename
 */
function updateFileLabel(event) {
    const input = event.target;
    const label = input.nextElementSibling;
    
    if (input.files && input.files.length > 0) {
        let fileName = input.files[0].name;
        if (fileName.length > 30) {
            fileName = fileName.substring(0, 27) + '...';
        }
        label.textContent = fileName;
    } else {
        label.textContent = label.dataset.defaultText || 'Choose file';
    }
}

/**
 * Setup confirmation modals for delete actions
 */
function setupConfirmationModals() {
    const confirmBtns = document.querySelectorAll('[data-confirm]');
    
    confirmBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const message = this.getAttribute('data-confirm');
            const target = this.getAttribute('href');
            
            if (confirm(message)) {
                // Create a form to submit POST request
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = target;
                document.body.appendChild(form);
                form.submit();
            }
        });
    });
}

/**
 * Setup product selection on document form
 * When brand is selected, load products for that brand
 */
function setupProductSelection() {
    const brandSelect = document.getElementById('brand_id');
    const productSelect = document.getElementById('product_id');
    
    if (brandSelect && productSelect) {
        brandSelect.addEventListener('change', function() {
            const brandId = this.value;
            
            if (brandId) {
                // Clear current options
                productSelect.innerHTML = '<option value="">เลือกสินค้า...</option>';
                productSelect.disabled = true;
                
                // Fetch products for the selected brand
                fetch(`/api/products/${brandId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(product => {
                            const option = document.createElement('option');
                            option.value = product.id;
                            option.textContent = `${product.name} (${product.code})`;
                            productSelect.appendChild(option);
                        });
                        
                        productSelect.disabled = false;
                    })
                    .catch(error => {
                        console.error('Error loading products:', error);
                        productSelect.disabled = false;
                    });
            } else {
                productSelect.innerHTML = '<option value="">โปรดเลือกแบรนด์ก่อน</option>';
                productSelect.disabled = true;
            }
        });
    }
}

/**
 * Toggle document type form
 * Show the form for the selected document type
 */
function showDocTypeForm(docType) {
    // Hide all forms
    const forms = document.querySelectorAll('.doc-type-form');
    forms.forEach(form => {
        form.style.display = 'none';
    });
    
    // Show the selected form
    const selectedForm = document.getElementById(`${docType}-form`);
    if (selectedForm) {
        selectedForm.style.display = 'block';
    }
    
    // Update hidden input
    const docTypeInput = document.getElementById('doc_type');
    if (docTypeInput) {
        docTypeInput.value = docType;
    }
}

/**
 * Confirm delete action with a custom modal
 */
function confirmDelete(itemType, itemId, itemName) {
    const modalTitle = document.getElementById('deleteModalLabel');
    const modalBody = document.getElementById('deleteModalBody');
    const deleteForm = document.getElementById('deleteForm');
    
    // Set modal content
    modalTitle.textContent = `ยืนยันการลบ ${itemType}`;
    modalBody.textContent = `คุณแน่ใจหรือไม่ว่าต้องการลบ ${itemType} "${itemName}"? การกระทำนี้ไม่สามารถยกเลิกได้`;
    
    // Set form action based on item type
    let action = '';
    
    switch (itemType) {
        case 'แบรนด์':
            action = `/brands/delete/${itemId}`;
            break;
        case 'สินค้า':
            action = `/products/delete/${itemId}`;
            break;
        case 'เอกสาร Specification':
            action = `/documents/delete/specification/${itemId}`;
            break;
        case 'เอกสาร COA':
            action = `/documents/delete/coa/${itemId}`;
            break;
        case 'เอกสาร Certificate':
            action = `/documents/delete/certificate/${itemId}`;
            break;
        case 'เอกสาร FDA':
            action = `/documents/delete/fda/${itemId}`;
            break;
        case 'ผู้ใช้':
            action = `/users/delete/${itemId}`;
            break;
    }
    
    deleteForm.action = action;
    
    // Show the modal
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}