document.addEventListener('DOMContentLoaded', function() {
    // Load form fields dynamically (if needed)
    const formContainer = document.getElementById('dynamicFormContainer');
    
    if (formContainer) {
        const formId = formContainer.dataset.formId;
        
        fetch(`/api/form-fields/?form_id=${formId}`)
            .then(response => response.json())
            .then(data => {
                renderFormFields(data.fields);
            });
    }
    
    // Traveller counter logic (from your original code)
    const minusBtn = document.querySelector('.minus-btn');
    const plusBtn = document.querySelector('.plus-btn');
    const travellerCount = document.querySelector('.traveller-count');
    const travellersInput = document.getElementById('travellers');
    
    if (minusBtn && plusBtn) {
        let count = 1;
        travellersInput.value = count;
        
        minusBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (count > 1) {
                count--;
                updateTravellerCount();
            }
        });
        
        plusBtn.addEventListener('click', function(e) {
            e.preventDefault();
            count++;
            updateTravellerCount();
        });
        
        function updateTravellerCount() {
            travellerCount.textContent = count;
            travellersInput.value = count;
            updatePrices(count);
        }
        
        function updatePrices(count) {
            // Update prices based on count
            document.getElementById('payNowAmount').textContent = `Rs. 9,999 x ${count}`;
            document.getElementById('payLaterAmount').textContent = `Rs. 4,999 x ${count}`;
            document.getElementById('totalAmount').textContent = `Rs. ${(9999 * count).toLocaleString()}/-`;
        }
    }
});

function renderFormFields(fields) {
    const form = document.createElement('form');
    form.id = 'dynamicForm';
    form.method = 'post';
    
    fields.forEach(field => {
        const fieldGroup = document.createElement('div');
        fieldGroup.className = 'mb-3';
        
        const label = document.createElement('label');
        label.className = 'form-label';
        label.textContent = field.label;
        label.htmlFor = `id_${field.label.toLowerCase().replace(/\s+/g, '_')}`;
        
        let input;
        if (field.type === 'select') {
            input = document.createElement('select');
            input.className = `form-select ${field.css_class || ''}`;
            input.name = field.label;
            input.id = label.htmlFor;
            
            field.options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option;
                optionElement.textContent = option;
                input.appendChild(optionElement);
            });
        } else if (field.type === 'radio') {
            fieldGroup.appendChild(label);
            
            field.options.forEach((option, index) => {
                const radioDiv = document.createElement('div');
                radioDiv.className = 'form-check';
                
                const radioInput = document.createElement('input');
                radioInput.type = 'radio';
                radioInput.className = 'form-check-input';
                radioInput.name = field.label;
                radioInput.id = `${label.htmlFor}_${index}`;
                radioInput.value = option;
                
                const radioLabel = document.createElement('label');
                radioLabel.className = 'form-check-label';
                radioLabel.htmlFor = radioInput.id;
                radioLabel.textContent = option;
                
                radioDiv.appendChild(radioInput);
                radioDiv.appendChild(radioLabel);
                fieldGroup.appendChild(radioDiv);
            });
        } else {
            input = document.createElement('input');
            input.type = field.type;
            input.className = `form-control ${field.css_class || ''}`;
            input.name = field.label;
            input.id = label.htmlFor;
            input.placeholder = field.placeholder || '';
        }
        
        if (field.type !== 'radio') {
            fieldGroup.appendChild(label);
            fieldGroup.appendChild(input);
        }
        
        if (field.help_text) {
            const helpText = document.createElement('div');
            helpText.className = 'form-text';
            helpText.textContent = field.help_text;
            fieldGroup.appendChild(helpText);
        }
        
        form.appendChild(fieldGroup);
    });
    
    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.className = 'btn btn-primary';
    submitButton.textContent = 'Submit';
    form.appendChild(submitButton);
    
    document.getElementById('dynamicFormContainer').appendChild(form);
}