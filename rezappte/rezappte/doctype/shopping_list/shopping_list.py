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
def get_shopping_list_html(recipe_list, added_ingredients=False, pdf_download=False):
    ingredients = get_ingredients(recipe_list)
    if added_ingredients:
        ingredients = add_ingredients(ingredients, added_ingredients)
    calced_ingredients = calc_ingredients(ingredients)
    ordered_ingredients = order_ingredients(calced_ingredients)
    html = create_html(ordered_ingredients)
    if pdf_download:
        pdf = create_pdf(html)
        return pdf
    frappe.log_error(html, "html")
    return html
    
def get_ingredients(recipe_list):
    recipe_list = json.loads(recipe_list)
    formatted_recipe_list = ""
    for i , recipe in enumerate(recipe_list):
        if i == 0:
            formatted_recipe_list += "'{0}'".format(recipe)
        else:
            formatted_recipe_list += " ,'{0}'".format(recipe)
            
    
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
    
def order_ingredients(ingredients):
    #get needed Market
    market = "Migros Sonnenhof"
    market_doc = frappe.get_doc("Market", market)
    
    #create dict with empty list for each section
    ordered_ingredients = {}
    for section in market_doc.section_order:
        ordered_ingredients[section.get('section')] = []
    
    #loopt through all ingredients and append it to the list of respective section
    for ingredient in ingredients:
        ordered_ingredients[ingredient.get('abteilung')].append({
                                                                    'ingredient': ingredient.get('ingredient'),
                                                                    'amount': ingredient.get('amount'),
                                                                    'uom': ingredient.get('uom')
                                                                })
    
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
