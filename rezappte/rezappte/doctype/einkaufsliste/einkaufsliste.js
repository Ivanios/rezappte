// Copyright (c) 2024, Ivanios and contributors
// For license information, please see license.txt

frappe.ui.form.on('Einkaufsliste', {
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("Postiliste herunterladen"),  function(){
              download_shopping_list(frm);
            });
            frm.add_custom_button(__("Postiliste öffnen"),  function(){
              window.location.href = '/desk#shopping-list-display?shopping_list=' + frm.doc.name;
            }).css({
                'background-color': 'orange',
                'color': '#ffffff'
            });
        }
    },
    //~ persons: function(frm) {
        //~ if (frm.doc.same_persons) {
            //~ set_persons_in_recipes(frm);
        //~ }
    //~ },
    keep_list: function(frm) {
        if (frm.doc.keep_list) {
            cur_frm.set_df_property('shopping_list_name', 'reqd', 1);
        } else {
            cur_frm.set_df_property('shopping_list_name', 'reqd', 0);
        }
    }
});

//~ frappe.ui.form.on('Einkaufsliste Rezept', {
    //~ recipes_add(frm, cdt, cdn) {
        //~ var row = locals[cdt][cdn];
        //~ if (frm.doc.same_persons) {
            //~ frappe.model.set_value(cdt, cdn, "persons", frm.doc.persons);
        //~ }
    //~ }
//~ });

frappe.ui.form.on('Einkaufsliste Additional Ingredients', {
    additional_ingredient(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        console.log(row);
        set_additional_uom_options(row.additional_ingredient);
    }
});

function set_additional_uom_options(ingredient) {
    frappe.call({
        'method': "frappe.client.get",
        'args': {
            'doctype': "Zutaten",
            'name': ingredient
        },
        'callback': function(response) {
            let main_uom = response.message.uom;
            let conversions = response.message.conversions;
            let options = [];
            options.push(main_uom);
            if (conversions) {
                for (let i = 0; i < conversions.length; i++) {
                    options.push(conversions[i].conversion_uom);
                }
            }
            var options_string = options.join("\n");
            console.log(options_string);
            cur_frm.get_field("additional_ingredients").grid.docfields[2].options = options_string;
            cur_frm.refresh_field("additional_ingredients");
        }
    });
}

function download_shopping_list(frm) {
    //~ let recipe_list = [];
    //~ for (let i = 0; i < frm.doc.recipes.length; i++) {
        //~ recipe_list.push(frm.doc.recipes[i].recipe);
    //~ }
    let added_ingredients = false
    if (frm.doc.additional_ingredients) {
        added_ingredients = frm.doc.name;
    }
    frappe.call({
        'method': 'rezappte.rezappte.doctype.einkaufsliste.einkaufsliste.get_shopping_list',
        'args': {
            'shopping_list_name': frm.doc.name,
            'persons': frm.doc.persons,
            'added_ingredients': added_ingredients,
            'pdf_download': true
        },
        'callback': function(response) {
            window.open(response.message.url, '_blank');
        }
    });
}
