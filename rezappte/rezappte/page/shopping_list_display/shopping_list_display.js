frappe.pages['shopping-list-display'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Shopping List',
		single_column: true
	});
	// create page
    frappe.shopping_list_display.make(page);
    // run page
    frappe.shopping_list_display.run(page);
    // Display recipe
    frappe.shopping_list_display.display(page);
    
    // add the application reference
    frappe.breadcrumbs.add("Einkaufsliste");
    
    // Button to run the Rezept
    page.set_primary_action( __('Stand speichern'), () => {
        get_choice();
    });
}

frappe.shopping_list_display = {
	make: function(page) {
		var me = frappe.shopping_list_display;
        me.page = page;
        me.body = $('<div id="container-shopping_list_display"></div>').appendTo(me.page.main);
	},
	run: function() {
		console.log("run");
	},
	display: function() {
		console.log("display");
        const shopping_list_name = get_shopping_list_name()
        display_shopping_list(shopping_list_name);
	}
}

function get_shopping_list_name() {
    var arguments = window.location.toString().split("?");
    if (!arguments[arguments.length - 1].startsWith("http")) {
       var args_raw = arguments[arguments.length - 1].split("&");
       var args = {};
       args_raw.forEach(function (arg) {
           var kv = arg.split("=");
           if (kv.length > 1) {
               args[kv[0]] = kv[1];
           }
       });
       if (args['shopping_list']) {
           return args['shopping_list']
       }      
    } else {
       frappe.msgprint("Shopping List Name missing");
       
    }
}

function display_shopping_list(shopping_list_name) {
	frappe.call({
		'method': 'rezappte.rezappte.page.shopping_list_display.shopping_list_display.get_shopping_list_template',
		'args': {
			'shopping_list_name': shopping_list_name
		},
		'callback': function(response) {
			if (response.message) {
				var shopping_list_template = response.message
				var container = document.getElementById("container-shopping_list_display");
				container.innerHTML = shopping_list_template; 
				//~ $('body').html(recipe);
			}
		}
	});
}

function toggleLine(ingredient) {
    var line = document.getElementById(ingredient.id);
    //~ var checkbox_id = ingredient + "_check"
    var checkbox = document.getElementById(ingredient.id + "_check");

    if (checkbox.checked) {
        line.style.display = "none";
    } else {
        line.style.display = "block";
    }
    return false
}

function unhide_category(category, ingredients) {
    for (let i  = 0; i < ingredients.length; i++) {
        let line = document.getElementById(ingredients[i].ingredient);
        line.style.display = "block";
    }
    return false
}