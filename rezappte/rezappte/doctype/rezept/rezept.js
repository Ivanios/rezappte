// Copyright (c) 2023, Ivanios and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rezept', {
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("Postiliste herunterladen"),  function(){
              create_recipe_shopping_list(frm);
            });
        }
    },
    validate: function(frm) {
        cur_frm.set_value("ingredients_qty", cur_frm.doc.ingredients.length);
    },
    typ: function(frm) {
        set_naming_series(frm);
    }
});

frappe.ui.form.on('Rezept Zutaten', {
    ingredient(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        set_uom_options(row.ingredient);
    }
});

function set_naming_series(frm) {
    if (frm.doc.typ == "Kochen") {
        cur_frm.set_value("naming_series", "K-.####.")
    } else if (frm.doc.typ == "Backen") {
        cur_frm.set_value("naming_series", "B-.####.")
    } else if (frm.doc.typ == "Drink") {
        cur_frm.set_value("naming_series", "D-.####.")
    }
}


function set_uom_options(ingredient) {
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
            cur_frm.get_field("ingredients").grid.docfields[2].options = options_string;
            cur_frm.refresh_field("ingredients");
        }
    });
}

function create_recipe_shopping_list(frm) {
	frappe.prompt([
		{'fieldname': 'persons', 'fieldtype': 'Int', 'label': 'Anzahl Personen', 'reqd': 1}  
	],
	function(values){
		create_recipe_shopping_html(frm, values.persons);
	},
	'Für wieviele Personen möchtest du kochen?',
	'Postiliste!'
	)
}

function create_recipe_shopping_html(frm, persons) {
	console.log(persons);
    let recipe_list = [];
    recipe_list.push(frm.doc.name);
    frappe.call({
        'method': 'rezappte.rezappte.doctype.shopping_list.shopping_list.get_shopping_list_html',
        'args': {
            'recipe_list': recipe_list,
            'pdf_download': true
        },
        'callback': function(response) {
            window.open(response.message.url, '_blank');
        }
    });
}

