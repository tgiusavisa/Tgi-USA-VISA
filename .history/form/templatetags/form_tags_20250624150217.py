from django import template
from django.utils.safestring import mark_safe
from ..models import Form

register = template.Library()

@register.simple_tag
def render_dynamic_form(form_name):
    try:
        form = Form.objects.get(name=form_name, is_active=True)
    except Form.DoesNotExist:
        return mark_safe("<p>Form not found or inactive</p>")
    
    fields_html = []
    
    for field in form.fields.filter(is_active=True).order_by('order'):
        field_html = f"""
        <div class="col-6 mt-1 mb-1">
            <label class='ps-1 pb-1'>{field.label}</label>
            <div class="d-flex">
        """
        
        if field.icon:
            field_html += f"""
                <span class="input-group-text form-img form-sec-01 form-border1">
                    <img src="{field.icon.url}" alt="{field.label}" class='rounded'/>
                </span>
            """
        
        if field.field_type == 'select':
            field_html += f"""
                <select class="form-select form-control form-sec-01 fs-6 form-border2" id="{field.label.lower().replace(' ', '_')}" name="{field.label.lower().replace(' ', '_')}" {'required' if field.required else ''}>
                    <option value="" selected disabled>{field.placeholder or field.label}</option>
            """
            for option in field.options.all():
                field_html += f"""
                    <option value="{option.value}">{option.label}</option>
                """
            field_html += """
                </select>
            """
        else:
            field_html += f"""
                <input type="{field.field_type}" class="form-control form-sec-01 fs-6 form-border2" id="{field.label.lower().replace(' ', '_')}" name="{field.label.lower().replace(' ', '_')}" placeholder="{field.placeholder or ''}" {'required' if field.required else ''}>
            """
        
        field_html += """
            </div>
        </div>
        """
        fields_html.append(field_html)
    
    price_items_html = []
    for item in form.price_items.all().order_by('order'):
        if item.is_free:
            price_items_html.append(f"""
                <li class='fs-6 d-flex flex-row align-item-center justify-content-between m-1'>
                    <span style='font-weight:500;'>{item.label}</span>
                    <span class='rounded-pill ps-2 pe-2 text-dark' style='background-color: #FFDD00; padding-bottom:1px !important;'>{item.value}</span>
                </li>
            """)
        else:
            price_items_html.append(f"""
                <li class='fs-6 d-flex flex-row align-item-center justify-content-between m-1'>
                    <span style='font-weight:500;'>{item.label}</span>
                    <span>{item.value}</span>
                </li>
            """)
    
    form_html = f"""
    <div class="col-4 position-fixed bg-white rounded-4 pb-3 pt-2 border border-gray shadow-sm" style='z-index:1000; top:9%; right:1%;'>
        <div class='fw-bolder fs-5 main-heading text-center'>{form.title}</div>
        <form id="appointmentForm" class="container row justify-content-center m-0 p-0">
            {"".join(fields_html)}
            <div class="col-6 mt-1 mb-1">
                <label class='ps-1 pb-1'>Travellers</label>
                <div class="d-flex">
                    <span class="input-group-text form-img form-sec-01 form-border1">
                        <img src="/static/images/icons/group.svg" alt="Group" class='rounded'/>
                    </span>
                    <input type="text" class="form-control form-sec-01 rounded-0" style="border: 1.2px solid rgba(0, 0, 0, 0.5); border-left: none !important; border-right: none;" id="travellers" placeholder="Traveller" value="1" readonly>
                    <span class="input-group-text form-img form-sec-01 form-border2">
                        <button class="btn btn-sm p-0 minus-btn">
                            <img src="/static/images/icons/minus.svg" alt="Minus" style='width:15px !important; object-fit:contain !important;'/>
                        </button>
                        <span class="mx-2 fw-bold fs-6 traveller-count">1</span>
                        <button class="btn btn-sm p-0 plus-btn">
                            <img src="/static/images/icons/plus.svg" alt="Add" style='width:15px !important; object-fit:contain !important;'/>
                        </button>
                    </span>
                </div>
            </div>
            <div class='mt-2'>
                <div class='d-flex justify-content-between w-100'>
                    <p class=' w-25 text-center fw-bolder fs-6 rounded-pill ps-2 pe-2 m-1 text-dark' style='background-color: #FFDD00; padding-bottom:1px !important;'>Price<p>
                    <p class=' w-75 text-end fw-bold fs-6ps-2 pe-2 m-1 text-dark'>Govt. Fees Not Included<p>
                </div>
                <ul class='m-0 p-0'>
                    {"".join(price_items_html)}
                    <div class='w-100 d-flex flex-row align-item-center justify-content-center mt-2 mb-2'><div class='line'></div></div>
                    <li class='fs-6 fw-bold d-flex flex-row align-item-center justify-content-between'><span>Pay later</span><span id="payLaterAmount">Rs. 4,999 x 1</span></li>
                    <li class='fs-6 fw-bold d-flex flex-row align-item-center justify-content-between'><span>Total Amount</span><span id="totalAmount">Rs. 9,999/-</span></li>
                </ul>
            <div>
            <button type="button" onclick="submitAppointmentForm()" class='mt-3 w-100 text-decoration-none align-items-center justify-content-center d-flex rounded-pill fw-bold pt-1 pb-1 button2 text-dark border-2 fs-5'>
                {form.submit_button_text}
            </button>
        </form>
    </div>
    """
    
    return mark_safe(form_html)