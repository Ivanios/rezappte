# -*- coding: utf-8 -*-
# Copyright (c) 2024, Gokuflynn and contributors
# For license information, please see license.txt

import frappe

@frappe.whitelist()
def get_colors():
    user_card = frappe.get_doc("User Card", frappe.session.user)
    
    if user_card.get('choose_own_colors'):
        background_color = user_card.get('background_color')
        font_color = user_card.get('font_color')
    else:
        background_color = frappe.db.get_value("Color Scheme", user_card.get('color_scheme'), "background_color")
        font_color = frappe.db.get_value("Color Scheme", user_card.get('color_scheme'), "font_color")
        
    return {'background_color': background_color, 'font_color': font_color}
