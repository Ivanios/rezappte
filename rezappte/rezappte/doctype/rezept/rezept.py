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

# ~ def data():
	    # ~ matching_projects = frappe.db.sql("""
        # ~ SELECT 
            # ~ `name`, 
            # ~ `drilling_team`, 
            # ~ `expected_start_date`, 
            # ~ `expected_end_date`, 
            # ~ `start_half_day`, 
            # ~ `end_half_day`, 
            # ~ `object`
        # ~ FROM `tabProject`
        # ~ WHERE `project_type` = "External"
          # ~ AND `status` IN ("Open", "Completed")
          # ~ AND 
            # ~ ((`expected_start_date` BETWEEN '{from_date}' AND '{to_date}')
             # ~ OR (`expected_end_date` BETWEEN '{from_date}' AND '{to_date}')
             # ~ OR (`expected_start_date` < '{from_date}' AND `expected_end_date` > '{to_date}')
            # ~ )
          # ~ {customer_filter}
          # ~ {drilling_team_filter}
        # ~ ORDER BY
            # ~ `tabProject`.`expected_start_date` ASC;
        # ~ """.format(from_date=from_date, to_date=to_date, customer_filter=customer_filter, drilling_team_filter=drilling_team_filter), as_dict=True)

	# ~ return
