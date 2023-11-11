# -*- coding: utf-8 -*-
# Copyright (c) 2023, Ivanios and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Rezept(Document):
	pass

@frappe.whitelist()
def calculate_ingredients(ingredients):
	ing = """
	SELECT `name` 
	FROM `tabRezept Zutaten`
	WHERE `alternative` = 0;"""
	real_ingredients = []
	for amount in ingredients:
		# ~ frappe.log_error>(amount['alternative'], "amount")
		frappe.log_error>(type(amount), "type")
		# ~ if amount['alternative'] == 0 and amount['optional'] == 0:
			# ~ real_ingredients.append(real_ingredients)
	# ~ return len(real_ingredients)
	return 7

def data():
	    matching_projects = frappe.db.sql("""
        SELECT 
            `name`, 
            `drilling_team`, 
            `expected_start_date`, 
            `expected_end_date`, 
            `start_half_day`, 
            `end_half_day`, 
            `object`
        FROM `tabProject`
        WHERE `project_type` = "External"
          AND `status` IN ("Open", "Completed")
          AND 
            ((`expected_start_date` BETWEEN '{from_date}' AND '{to_date}')
             OR (`expected_end_date` BETWEEN '{from_date}' AND '{to_date}')
             OR (`expected_start_date` < '{from_date}' AND `expected_end_date` > '{to_date}')
            )
          {customer_filter}
          {drilling_team_filter}
        ORDER BY
            `tabProject`.`expected_start_date` ASC;
        """.format(from_date=from_date, to_date=to_date, customer_filter=customer_filter, drilling_team_filter=drilling_team_filter), as_dict=True)

	return
