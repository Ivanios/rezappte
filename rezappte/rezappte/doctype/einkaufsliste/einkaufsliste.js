// Copyright (c) 2024, Ivanios and contributors
// For license information, please see license.txt

frappe.ui.form.on('Einkaufsliste', {
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("Postiliste herunterladen"),  function(){
              create_shopping_list(frm);
            });
        }
    },
    keep_list: function(frm) {
        console.log(frm.doc.keep_list);
        if (frm.doc.keep_list) {
            cur_frm.set_df_property('shopping_list_name', 'reqd', 1);
        } else {
            cur_frm.set_df_property('shopping_list_name', 'reqd', 0);
        }
    }
});

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

function create_shopping_list(frm) {
    let recipe_list = [];
    for (let i = 0; i < frm.doc.recipes.length; i++) {
        recipe_list.push(frm.doc.recipes[i].recipe);
    }
    frappe.call({
        'method': 'rezappte.rezappte.doctype.shopping_list.shopping_list.get_shopping_list_html',
        'args': {
            'recipe_list': recipe_list,
            'added_ingredients': frm.doc.name,
            'pdf_download': true
        },
        'callback': function(response) {
            console.log(response.message);
            window.open(response.message.url, '_blank');
        }
    });
}
