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
	calced_ingredients = calc_ingredients(ingredients)
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
	
def calc_ingredients(ingredients):
	calced_ingredients = []
	for ingredient in ingredients:
		ingredient_uom = frappe.get_value("Zutaten", ingredient.get('ingredient'), "uom")
		if ingredient.get('uom') != ingredient_uom:
			actual_ingredient, real_amount, main_uom  = convert_uom(ingredient.get('ingredient'), ingredient.get('amount'), ingredient.get('uom'))
		else:
			actual_ingredient, real_amount, main_uom  = ingredient.get('ingredient'), ingredient.get('amount'), ingredient.get('uom')
		
		found_match = False
		for existing_ingredient in calced_ingredients:
			if existing_ingredient.get('ingredient') == actual_ingredient:
				found_match = True
				existing_ingredient['amount'] += real_amount
		if not found_match:
			calced_ingredients.append({'ingredient': actual_ingredient, 'amount': real_amount or 0, 'uom': main_uom, 'abteilung': ingredient.get('abteilung')})

	return calced_ingredients
									
def convert_uom(ingredient, amount, uom):
	ingredient_doc = frappe.get_doc("Zutaten", ingredient)
	main_uom = ingredient_doc.get('uom')
	for sub_uom in ingredient_doc.get('conversions'):
		if sub_uom.get('conversion_uom') == uom:
			real_amount = amount * sub_uom.get('conversion_factor')
			
	return ingredient, real_amount, main_uom
	
