# -*- coding: utf-8 -*-
# Copyright (c) 2023, Ivanios and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

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
	frappe.log_error(parent_name, "parent_name")
	ing = frappe.db.sql("""
	SELECT `name` 
	FROM `tabRezept Zutaten`
	WHERE `parent` = '{name}'
	AND `alternative` = 0
	AND `optional` = 0;
	""".format(name=parent_name), as_list=True)
	frappe.log_error(len(ing), "ing")
	
	doc = frappe.get_doc("Rezept", parent_name)
	doc.ingredients_qty = len(ing)
	doc.save()

	return

@frappe.whitelist()
def create_shopping_list(recipe, persons):
    frappe.log_error(recipe, "recipe")
    frappe.log_error(persons, "persons")
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
