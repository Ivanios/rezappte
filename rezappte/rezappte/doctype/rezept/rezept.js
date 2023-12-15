// Copyright (c) 2023, Ivanios and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rezept', {
    validate: function(frm) {
		cur_frm.set_value("ingredients_qty", cur_frm.doc.ingredients.length);
		autocomplete_region(frm);
	},
    //~ after_save: function(frm) {
		//~ calculate_ingredients(frm);
    //~ },
    origin: function(frm) {
        autocomplete_region(frm);
    }
    //~ ingredients: function(frm) {
        //~ fill_uom(frm);
    //~ }
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
