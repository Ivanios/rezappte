# -*- coding: utf-8 -*-
# Copyright (c) 2023, Ivanios and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
# ~ from frappe.model.document import Document

# ~ class Shopping List(Document):
	# ~ pass

@frappe.whitelist()
def get_shopping_list_html(recipe_list):
	ingredients = get_ingredients(recipe_list)
	frappe.log_error(ingredients, "ingredients")
	return
	
def get_ingredients(recipe_list):
	recipe_list = json.loads(recipe_list)
	formatted_recipe_list = ""
	for i , recipe in enumerate(recipe_list):
		if i == 0:
			formatted_recipe_list += "'{0}'".format(recipe)
		else:
			formatted_recipe_list += " ,'{0}'".format(recipe)
			
	frappe.log_error(formatted_recipe_list)
	ingredients = frappe.db.sql("""
								SELECT
									`tabRezept Zutaten`.`ingredient`,
									`tabRezept Zutaten`.`amount`,
									`tabRezept Zutaten`.`uom`,
									`tabZutaten`.`abteilung`
								FROM
									`tabRezept Zutaten`
								LEFT JOIN
									`tabRezept` ON `tabRezept Zutaten`.`parent` = `tabRezept`.`name`
								LEFT JOIN
									`tabZutaten` ON `tabRezept Zutaten`.`ingredient` = `tabZutaten`.`name`
								WHERE
									`tabRezept`.`name` IN ({})""".format(formatted_recipe_list), as_dict=True)
	return ingredients
									
