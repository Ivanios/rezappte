# -*- coding: utf-8 -*-
# Copyright (c) 2023, Ivanios and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json

class Rezept(Document):
    pass
    
@frappe.whitelist()
def fill_uom(ingredient):
    frappe.log_error(ingredient, "ingredient")
    
    uom = frappe.db.get_value("Zutaten", {"Name": ingredient}, "uom")
    
    frappe.log_error(uom, "uom")
    

    return 7

@frappe.whitelist()
def calculate_ingredients(parent_name):
    ing = frappe.db.sql("""
    SELECT `name` 
    FROM `tabRezept Zutaten`
    WHERE `parent` = '{name}'
    AND `alternative` = 0
    AND `optional` = 0;
    """.format(name=parent_name), as_list=True)
    
    doc = frappe.get_doc("Rezept", parent_name)
    doc.ingredients_qty = len(ing)
    doc.save()

    return

@frappe.whitelist()
def create_shopping_list(recipe, persons):
    shopping_list_doc = frappe.get_doc({
        "doctype": "Einkaufsliste",
        "persons": persons,
        #Create subtable "layers"
        "recipes": [{
        "reference_doctype": "Einkaufsliste Rezept",
        "recipe": recipe
        }]
    })
    
    shopping_list_doc.insert()
    frappe.db.commit()
    
    return shopping_list_doc.name
    
@frappe.whitelist()
def get_ingredients_from_instruction(instruction):
    instruction = json.loads(instruction)
    ingredients = []
    for step in instruction:
        found_match = False
        for existing_ingredient in ingredients:
            if step.get('steps_ingredient') == existing_ingredient.get('ingredient') and step.get('steps_uom') == existing_ingredient.get('uom'):
                found_match = True
                existing_ingredient['amount'] += int(step.get('steps_amount'))
        if not found_match:
            ingredients.append({
                'ingredient': step.get('steps_ingredient'),
                'amount': int(step.get('steps_amount')),
                'uom': step.get('steps_uom')
            })
    frappe.log_error(ingredients, "ingredients")
    return ingredients
