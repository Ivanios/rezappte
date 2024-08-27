# -*- coding: utf-8 -*-
# Copyright (c) 2024, Gokuflynn and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
import random
import string

class Einkaufsliste(Document):
	pass
    
# ~ @frappe.whitelist()
# ~ def get_shopping_list_wrapper(recipe_list, persons, added_ingredients=False, return_html=False, pdf_download=False):
    # ~ _recipe_list = []
    # ~ for recipe in recipe_list:
        # ~ _recipe_list.append(recipe)
    # ~ recipe_list = _recipe_list
    # ~ pdf = get_shopping_list(recipe_list, persons, added_ingredients, pdf_download=True)
    # ~ return pdf
    
@frappe.whitelist()
def get_shopping_list(shopping_list_name, persons, added_ingredients=False, return_html=False, pdf_download=False):
    raw_ingredients = get_ingredients(shopping_list_name)
    ingredients = add_persons_to_ingredients(raw_ingredients, persons)
    if added_ingredients:
        ingredients = add_ingredients(ingredients, added_ingredients)
    calced_ingredients = calc_ingredients(ingredients)
    ordered_ingredients = order_ingredients(calced_ingredients)
    if return_html:
        html = create_html(ordered_ingredients)
        return html
    if pdf_download:
        html = create_html(ordered_ingredients)
        pdf = create_pdf(html)
        return pdf
    return ordered_ingredients
    
    
def get_ingredients(shopping_list_name):
    # ~ if type(recipe_list) == "Str":
        # ~ recipe_list = json.loads(recipe_list)
    # ~ formatted_recipe_list = ""
    # ~ for i , recipe in enumerate(recipe_list):
        # ~ if i == 0:
            # ~ formatted_recipe_list += "'{0}'".format(recipe)
        # ~ else:
            # ~ formatted_recipe_list += " ,'{0}'".format(recipe)
            
    
    ingredients = frappe.db.sql("""
                                SELECT
                                    `tabRezept Zutaten`.`ingredient`,
                                    `tabRezept Zutaten`.`amount`,
                                    `tabRezept Zutaten`.`uom`,
                                    `tabRezept`.`persons_qty`,
                                    `tabZutaten`.`abteilung`
                                FROM
                                    `tabRezept Zutaten`
                                LEFT JOIN
                                    `tabRezept` ON `tabRezept Zutaten`.`parent` = `tabRezept`.`name`
                                LEFT JOIN
                                    `tabZutaten` ON `tabRezept Zutaten`.`ingredient` = `tabZutaten`.`name`
                                WHERE
                                    `tabRezept`.`name` IN (SELECT `recipe` FROM `tabEinkaufsliste Rezept` WHERE `parent` = '{}')""".format(shopping_list_name), as_dict=True)
                                    # ~ `tabRezept`.`name` IN ({})""".format(formatted_recipe_list), as_dict=True)
    return ingredients
    
def add_persons_to_ingredients(raw_ingredients, persons):
    ingredients = []
    for raw_ingredient in raw_ingredients:
        if raw_ingredient.get('persons_qty') != int(persons):
            raw_ingredient['amount'] = raw_ingredient.get('amount') / raw_ingredient.get('persons_qty') * int(persons)
        ingredients.append(raw_ingredient)
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
    
def order_ingredients(ingredients):
    #get User Card
    user_card = frappe.get_doc("User Card", frappe.session.user)
    
    #get needed Market
    market = user_card.favorite_market
    market_doc = frappe.get_doc("Market", market)
    
    #create list of ingredients at home
    ingredients_at_home = []
    if user_card.ingredients_at_home:
        for ingredient in user_card.ingredients_at_home:
            ingredients_at_home.append(ingredient.home_ingredient)
    
    #create dict with empty list for each section
    ordered_ingredients = {}
    for section in market_doc.section_order:
        ordered_ingredients[section.get('section')] = []
    
    #loopt through all ingredients and append it to the list of respective section
    for ingredient in ingredients:
        if ingredient.get('ingredient') not in ingredients_at_home:
            ordered_ingredients[ingredient.get('abteilung')].append({
                                                                        'ingredient': ingredient.get('ingredient'),
                                                                        'amount': ingredient.get('amount'),
                                                                        'uom': ingredient.get('uom'),
                                                                        'html_id': get_html_id(length=12)
                                                                    })
    frappe.log_error(ordered_ingredients, "ordered_ingredients")
    return ordered_ingredients
    
def create_html(ingredients):
    html = "<div>"
    for key, value in ingredients.items():
        if value:
            html += "<b>{0}:</b>".format(key)
            for ingredient in value:
                html += "<p style='padding: None !important;'>-{0} {1} {2}</p>".format(ingredient.get('amount'), ingredient.get('uom'), ingredient.get('ingredient'))
    html += "</div>"
    return html
    
def create_pdf(html):
    from frappe.utils.pdf import get_pdf
    from PyPDF2 import PdfFileWriter
    from frappe.utils.pdf import get_file_data_from_writer
    
    output = PdfFileWriter()
    output = get_pdf(html, output=output)
    filedata = get_file_data_from_writer(output)
    
    _file = frappe.get_doc({
        "doctype": "File",
        "file_name": "Postiliste",
        # ~ "folder": folder,
        "is_private": 0,
        "content": filedata
    })
    
    _file.save(ignore_permissions=True)
    
    return {'url': _file.file_url, 'name': _file.name}

def add_ingredients(ingredients, shoppping_list_name):
    ingredients_to_add = frappe.db.sql("""
                                        SELECT
                                            `tabEinkaufsliste Additional Ingredients`.`additional_ingredient` AS `ingredient`,
                                            `tabEinkaufsliste Additional Ingredients`.`additional_amount` AS `amount`,
                                            `tabEinkaufsliste Additional Ingredients`.`additional_uom` AS `uom`,
                                            `tabZutaten`.`abteilung`
                                        FROM
                                            `tabEinkaufsliste Additional Ingredients`
                                        LEFT JOIN
                                            `tabZutaten` ON `tabEinkaufsliste Additional Ingredients`.`additional_ingredient` = `tabZutaten`.`name`
                                        WHERE
                                            `tabEinkaufsliste Additional Ingredients`.`parent` = '{shopping_list}'""".format(shopping_list=shoppping_list_name), as_dict=True)
    for ingredient in ingredients_to_add:
        ingredients.append(ingredient)
    return ingredients

def delete_shopping_lists():
    shopping_lists = frappe.db.sql("""
                                    SELECT
                                        `name`
                                    FROM
                                        `tabEinkaufsliste`
                                    WHERE
                                        `keep_list` = 0""", as_dict=True)
    if len(shopping_lists) > 0:
        for shopping_list in shopping_lists:
            frappe.delete_doc("Einkaufsliste", shopping_list.get('name'))
            
    return
    
def get_html_id(length=20):
    random_string = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return random_string
