# -*- coding: utf-8 -*-
# Copyright (c) 2024, Gokuflynn and contributors
# For license information, please see license.txt

import frappe
from collections import Counter
import json

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
    
@frappe.whitelist()
def find_recipe_by_ingredients(ingredients):
    ingredients = json.loads(ingredients)
    # build conditions string
    conditions = " OR ".join(
        "`tabRezept Zutaten`.`ingredient` = '{0}'".format(condition.replace("'", "''")) for condition in ingredients
    )
    
    #get al results with at least one hit
    if conditions:
        all_results = frappe.db.sql("""
                                    SELECT
                                        `tabRezept`.`title`
                                    FROM
                                        `tabRezept`
                                    LEFT JOIN
                                        `tabRezept Zutaten` ON `tabRezept`.`name` = `tabRezept Zutaten`.`parent`
                                    WHERE
                                        {conditions}""".format(conditions=conditions), as_dict=True)
    
        all_results_list = []
        for result in all_results:
            all_results_list.append(result.get('title'))
        
        #count how many searched ingredients are included in each recipe
        counter = Counter(all_results_list)
        
        #sort recipes by most ingredient hits and cut i to 10 recipes
        list_of_top_recipes = [{'recipe': item, 'count': count} for item, count in counter.most_common(10)]
        
        #get used ingredients for recipes
        for top_recipe in list_of_top_recipes:
            ingredient_hits = frappe.db.sql("""
                                        SELECT
                                            `tabRezept Zutaten`.`ingredient`,
                                            `tabRezept Zutaten`.`parent`
                                        FROM
                                            `tabRezept Zutaten`
                                        LEFT JOIN
                                            `tabRezept` ON `tabRezept`.`name` = `tabRezept Zutaten`.`parent`
                                        WHERE
                                            `tabRezept`.`title` = '{recipe}'
                                        AND
                                            ({conditions})""".format(recipe=top_recipe.get('recipe'), conditions=conditions), as_dict=True)
            ingredient_hits_index = 1
            for ingredient in ingredient_hits:
                top_recipe['ingredient_{0}'.format(ingredient_hits_index)] = ingredient.get('ingredient')
                if ingredient_hits_index == 1:
                    top_recipe['recipe_number'] = ingredient.get('parent')
                ingredient_hits_index += 1
        
        return list_of_top_recipes
    else:
        return False
