frappe.pages['find-recipe'].on_page_load = function(wrapper) {
    var me = this;
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Find Recipe',
        single_column: true
    });
    
    page.main.html(frappe.render_template("find_recipe", {}));
    
    

    //~ // Erstelle die Seite
    //~ frappe.rezept_finden.make(page);

    //~ // Führe die Seite aus
    //~ frappe.rezept_finden.run(page);

    //~ // Zeige das Rezept an
    //~ frappe.rezept_finden.display(page);

    //~ // Füge das Application-Reference-Breadcrumb hinzu
    //~ frappe.breadcrumbs.add("Rezept");

    // Füge einen Button hinzu, um das Rezept zu speichern
    page.set_primary_action(__('Stand speichern'), () => {
        frappe.msgprint("Oops, Funktion leider noch nicht verfügbar :-(", "Sorry!");
    });
    
    $(document).ready(function() {
    
    //~ create_ingredients_link_field(page);
    
    let ingredients_qty = $("#ingredients_qty")
    
    ingredients_qty.on('input', function() {
                set_ingredient_inputs($(this).val());
                create_ingredient_input_field(page);
            });

    
    $('#page-find-recipe').addClass('background-color');
    
    set_colors();
    });
};

function set_colors() {
    frappe.call({
        'method': 'rezappte.rezappte.page.find_recipe.find_recipe.get_colors',
        'callback': function(response) {
            let font_color = response.message.font_color
            let background_color = response.message.background_color
            
            $('.font-color').css({
                'color': font_color,
            });
            
            $('.background-color').css({
                'background-color': background_color,
            });
        }
    });
}

function toggle_option(div_id) {
    var option = $(div_id).data("option")
    var element = $("#" + option)
    console.log(element);
    
    if (element.length > 0) {
        if (element.is(':visible')) {
            element.hide();
        } else {
            element.show();
        }
    } else {
        console.error('Element mit ID ' + div_id + ' wurde nicht gefunden.');
    }
}

function set_ingredient_inputs(qty) {
    console.log(qty);
}

function create_ingredient_input_field(page) {
    var ingredient_input_container = page.main.find(".ingredient_input");
    console.log(ingredient_input_container);
    var ingredient_input_field = frappe.ui.form.make_control({
        parent: page.main.find(".ingredient_input"),
        df: {
            fieldtype: "Link",
            fieldname: "ingredient_input",
            options: 'Zutaten',
            placeholder: "Zutat"
        },
        only_input: true,
    });
    return ingredient_input_field
}
