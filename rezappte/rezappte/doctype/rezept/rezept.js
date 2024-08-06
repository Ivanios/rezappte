// Copyright (c) 2023, Ivanios and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rezept', {
    validate: function(frm) {
		cur_frm.set_value("ingredients_qty", cur_frm.doc.ingredients.length);
		autocomplete_region(frm);
	},
    origin: function(frm) {
        autocomplete_region(frm);
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


function autocomplete_region() {
	let asiatisch = ["Thailand", "Vietnam", "China", "Japan"];
	let europäisch = ["Italien", "Frankreich", "Österreich", "Schweiz", "Deutschland"];
    if (asiatisch.includes(cur_frm.doc.origin)) {
        cur_frm.set_value("region", "Asiatisch");
    } else if (europäisch.includes(cur_frm.doc.origin)) {
		cur_frm.set_value("region", "Europäisch");
    }
}

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
			console.log(options_string);
			cur_frm.get_field("ingredients").grid.docfields[2].options = options_string;
			cur_frm.refresh_field("ingredients");
        }
    });
}

