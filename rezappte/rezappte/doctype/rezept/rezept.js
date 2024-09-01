// Copyright (c) 2023, Ivanios and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rezept', {
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("Postiliste erstellen"),  function(){
              create_shopping_list(frm);
            }).css({
                'background-color': 'orange',
                'color': '#ffffff'
            });
        }
    },
    validate: function(frm) {
        cur_frm.set_value("ingredients_qty", cur_frm.doc.ingredients.length);
    },
    typ: function(frm) {
        set_naming_series(frm);
    },
    vegan: function(frm) {
        set_vegan_information(frm);
    },
    ingredients_from_instruction: function(frm) {
        get_ingredients_from_instruction(frm);
    }
});

frappe.ui.form.on('Rezept Zutaten', {
    ingredient(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.ingredient) {
            set_uom_options(row.ingredient);
        } else {
            frappe.model.set_value(cdt, cdn, "amount", "");
            frappe.model.set_value(cdt, cdn, "uom", "");
            cur_frm.get_field("ingredients").grid.docfields[2].options = "";
            cur_frm.refresh_field("ingredients");
        }
    },
    form_render(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.ingredient) {
            set_uom_options(row.ingredient);
        } else {
            frappe.model.set_value(cdt, cdn, "amount", "");
            frappe.model.set_value(cdt, cdn, "uom", "");
            cur_frm.get_field("ingredients").grid.docfields[2].options = "";
            cur_frm.refresh_field("ingredients");
        }
    }
});

frappe.ui.form.on('Schritte', {
    steps_ingredient(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.steps_ingredient) {
            set_steps_uom_options(row.steps_ingredient);
        } else {
            frappe.model.set_value(cdt, cdn, "steps_amount", "");
            frappe.model.set_value(cdt, cdn, "steps_uom", "");
            cur_frm.get_field("instruction").grid.docfields[2].options = "";
            cur_frm.refresh_field("instruction");
        }
    },
    form_render(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.steps_ingredient) {
            set_steps_uom_options(row.steps_ingredient);
        } else {
            frappe.model.set_value(cdt, cdn, "steps_amount", "");
            frappe.model.set_value(cdt, cdn, "steps_uom", "");
            cur_frm.get_field("instruction").grid.docfields[2].options = "";
            cur_frm.refresh_field("instruction");
        }
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

function create_shopping_list(frm) {
    frappe.call({
        'method': 'rezappte.rezappte.doctype.rezept.rezept.create_shopping_list',
        'args': {
            'recipe': frm.doc.name,
            'persons': frm.doc.persons_qty
        },
        'callback': function(response) {
            if (response.message) {
                window.location.href = '/desk#Form/Einkaufsliste/' + response.message;
            }
        }
    });
}

function set_vegan_information(frm) {
    if (frm.doc.vegan) {
        cur_frm.set_value("vegetarian", 1);
        cur_frm.set_value("lactose", 1);
    }
}

function set_steps_uom_options(ingredient) {
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
            cur_frm.get_field("instruction").grid.docfields[2].options = options_string;
            cur_frm.refresh_field("instruction");
        }
    });
}

function get_ingredients_from_instruction(frm) {
    frappe.call({
        'method': "rezappte.rezappte.doctype.rezept.rezept.get_ingredients_from_instruction",
        'args': {
            'instruction': frm.doc.instruction
        },
        'callback': function(response) {
            var ingredients = response.message
            for (var i = 0; i < ingredients.length; i++) {
                var child = cur_frm.add_child('ingredients');
                child.ingredient = ingredients[i].ingredient;
                child.amount = ingredients[i].amount;
                child.uom = ingredients[i].uom;
                cur_frm.refresh_field("ingredients");
            }
        }
    });
}

