// Copyright (c) 2023, Ivanios and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rezept', {
    after_save: function(frm) {
		calculate_ingredients(frm);
    },
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

//~ function fill_uom(frm) {
	//~ console.log("1")
	//~ frappe.call({
        //~ 'method': 'rezappte.rezappte.doctype.rezept.rezept.fill_uom',
        //~ 'args': {
            //~ 'ingredients': frm.doc.ingredients.ingredient
        //~ },
        //~ 'callback': function(r) {
			//~ console.log("2")
            //~ cur_frm.set_value("ingredients.ingredient", r.message);
        //~ }
    //~ });
//~ }



function calculate_ingredients(frm) {
	console.log("1");
	frappe.call({
        'method': 'rezappte.rezappte.doctype.rezept.rezept.calculate_ingredients',
        'args': {
            'parent_name': frm.doc.name
        },
        'callback': function(r) {
			//~ console.log(r.message)
            //~ cur_frm.set_value("ingredients_qty", r.message);
        }
    });
}

//~ function calculate_ingredients(frm) {
	//~ cur_frm.set_value("ingredients_qty", frm.doc.ingredients.length);
//~ }
