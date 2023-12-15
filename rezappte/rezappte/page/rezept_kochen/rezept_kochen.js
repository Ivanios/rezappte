frappe.pages['rezept_kochen'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Rezept kochen',
		single_column: true
	});
	
	// create page
    frappe.rezept_kochen.make(page);
    // run page
    frappe.rezept_kochen.run(page);
    
    // add the application reference
    frappe.breadcrumbs.add("Rezappte");
    
    // Button to run the Rezept
    page.set_primary_action( __('Anderes Rezept kochen'), () => {
        get_choice();
    });
}


frappe.rezept_kochen = {
	make: function(page) {
		console.log("make");
	},
	run: function() {
		console.log("run");
		get_choice();
	}
	//~ display: function() {
		//~ console.log("display");
		
	//~ }
}

function get_choice() {
	frappe.prompt([
		{'fieldname': 'recipe_choice', 'fieldtype': 'Link', 'label': 'Rezept wählen', 'options': 'Rezept', 'reqd': 1},
		{'fieldname': 'person_qty', 'fieldtype': 'Int', 'label': 'Anzahl Personen', 'reqd': 1}
	],
	function(values){
		frappe.show_alert("Du Maschine", 5);
		get_recipe(values);
	},
	'Rezept kochen',
	'Kochen!'
	)
}

function get_recipe(values) {
	frappe.call({
		'method': 'rezappte.rezappte.python.get_recipe_html',
		'args': {
			'recipe_no': values.recipe_choice,
			'persons': values.person_qty
		},
		'callback': function(response) {
			var recipe = response.message
			//~ console.log(recipe);
			//~ get_recipe_html(recipe);
		}
	});
}

//~ function get_recipe_html(recipe) {
	//~ console.log("get_recipe_html");
	//~ frappe.call({
		//~ 'method': 'rezappte.rezappte.python.get_recipe_html',
		//~ 'args': {
			//~ 'recipe': recipe
		//~ },
		//~ 'callback': function(response) {
			//~ console.log("verdammts Tier");
		//~ }
	//~ });
//~ }



	
