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

def get_ingredients(recipe, persons):
	#get the amount of persons, which the recipe is calculated for
	persons_qty = frappe.db.get_value("Rezept", recipe, "persons_qty")
	
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
		""".format(recipe=recipe), as_dict=True)

	print(persons_qty)
	print(ingredients)
	
	return
