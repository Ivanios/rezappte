# -*- coding: utf-8 -*-
# Copyright (c) 2024, Gokuflynn and contributors
# For license information, please see license.txt

import frappe
from rezappte.rezappte.doctype.einkaufsliste.einkaufsliste import get_shopping_list
from frappe.model.document import Document

@frappe.whitelist()
def get_shopping_list_template(shopping_list_name):
    zutat = frappe.get_doc("Zutaten", "Cherrytomaten")
    shopping_list_doc = frappe.get_doc("Einkaufsliste", shopping_list_name)
    recipe_list = []
    for recipe in shopping_list_doc.recipes:
        recipe_list.append(recipe.get('recipe'))
    
    added_ingredients = None
    if shopping_list_doc.get('additional_ingredients'):
        added_ingredients = shopping_list_doc.get('name')
    ordered_ingredients = get_shopping_list(recipe_list, shopping_list_doc.get('persons'), added_ingredients)
    shopping_list_template = frappe.render_template("rezappte/rezappte/page/shopping_list_display/shopping_list_display.html", {'ingredients': ordered_ingredients})
    return shopping_list_template
    
