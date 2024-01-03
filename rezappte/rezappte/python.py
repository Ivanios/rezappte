# Copyright (c) 2023, Ivanios and Contributors
# License: GNU General Public License v3. See license.txt
#
#
# Helper functions to find closest suppliers
#
# Find closest hotels
#  $ bench execute heimbohrtechnik.heim_bohrtechnik.locator.find_closest_hotels --kwargs "{'object_name': 'P-231234' }"
#

import frappe

@frappe.whitelist()	
def get_recipe_html(recipe_no, persons):
	
	#get recipe
	recipe = get_recipe(recipe_no, persons)
	
	html = frappe.render_template("rezappte/rezappte/page/rezept_kochen/rezept_kochen.html", recipe)

	return html

@frappe.whitelist()
def get_recipe(recipe_no, persons):
	#get ingredients for wished amount of persons
	ingredients = get_ingredients(recipe_no, persons)
	
	#get the recipe instruction
	instruction = get_instruction(recipe_no)
	
	#get_recipe_information
	information = get_recipe_information(recipe_no)
	
	hints = get_recipe_hints(recipe_no)
	
	recipe = {
		'ingredients': ingredients,
		'instruction': instruction,
		'information': information,
		'hints': hints }
	
	return recipe
		

def get_ingredients(recipe_no, persons):
	#get the amount of persons, which the recipe is calculated for
	persons_qty = frappe.db.get_value("Rezept", recipe_no, "persons_qty")
	
	#get ingredients
	ingredients = frappe.db.sql("""
		SELECT `sinvitem`.`ingredient`,
			`sinvitem`.`amount`,
			`sinvitem`.`uom`,
			`sinvitem`.`alternative`,
			`sinvitem`.`optional`
		FROM `tabRezept Zutaten` AS `sinvitem`
		LEFT JOIN `tabRezept` AS `sinv` ON `sinvitem`.`parent` = `sinv`.`name`
		WHERE `sinv`.`name` = '{recipe}'
		""".format(recipe=recipe_no), as_dict=True)
	
	#calculate real ingredients
	for ingredient in ingredients:
		new_amount = ingredient['amount'] / persons_qty * int(persons)
		ingredient['amount'] = new_amount
	
	return ingredients

def get_instruction(recipe_no):

	#get recipe document
	doc = frappe.get_doc("Rezept", recipe_no)
	
	#get steps an put it in a list of dicts
	instruction = []
	for step in doc.instruction:
		instruction.append({
			'step': step.description
		})
	
	return instruction
	
def get_recipe_information(recipe_no):
	
	information = frappe.db.sql("""
		SELECT `name`,
			`title`,
			`effort`,
			`ingredients_qty`,
			`origin`,
			`region`,
			`vegetarian`,
			`vegan`,
			`lactose`,
			`gluten`,
			`owner`
		FROM `tabRezept`
		WHERE `name` = '{recipe}'
		""".format(recipe=recipe_no), as_dict=True)

	return information
	
def get_recipe_hints(recipe_no):
	
	hints = frappe.db.get_value("Rezept", recipe_no, "hints")
	
	return hints
