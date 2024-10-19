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
    
    $('#page-find-recipe').addClass('background-color');
    
    create_ingredient_input_field(page, "1");
    create_ingredient_input_field(page, "2");
    create_ingredient_input_field(page, "3");
    create_ingredient_input_field(page, "4");
    create_ingredient_input_field(page, "5");
    
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

function create_ingredient_input_field(page, field_no) {
    //~ var ingredient_input_container = page.main.find(".ingredient_input_" + field_no);
    var ingredient_input_field = frappe.ui.form.make_control({
        parent: page.main.find(".ingredient_input_" + field_no),
        df: {
            fieldtype: "Link",
            fieldname: "ingredient_input_" + field_no,
            options: 'Zutaten',
            placeholder: "Zutat"
        },
        only_input: true
    });
    ingredient_input_field.refresh();
    
    ingredient_input_field.$input.on('awesomplete-selectcomplete', function() {
        var value = ingredient_input_field.get_value();
        if(value) {
            search_and_show_recipe()
            let field_no_int = parseInt(field_no) + 1
            $('.ingredient_input_' + field_no_int.toString()).show()
        } else {
            search_and_show_recipe()
            // does not work
        }
    });

    ingredient_input_field.$input.on('change', function() {
        var value = ingredient_input_field.get_value();
        if(value) {
            search_and_show_recipe()
            // does not work
        } else {
            search_and_show_recipe()
            sort_ingredient_fields();
        }
    });
}

function search_and_show_recipe() {
    let ingredients = []
    let ingredientValue_1 = $('.ingredient_input_1').find('input').val();
    if (ingredientValue_1) {
        ingredients.push(ingredientValue_1)
    }
    let ingredientValue_2 = $('.ingredient_input_2').find('input').val();
    if (ingredientValue_2) {
        ingredients.push(ingredientValue_2)
    }
    let ingredientValue_3 = $('.ingredient_input_3').find('input').val();
    if (ingredientValue_3) {
        ingredients.push(ingredientValue_3)
    }
    let ingredientValue_4 = $('.ingredient_input_4').find('input').val();
    if (ingredientValue_4) {
        ingredients.push(ingredientValue_4)
    }
    let ingredientValue_5 = $('.ingredient_input_5').find('input').val();
    if (ingredientValue_5) {
        ingredients.push(ingredientValue_5)
    }

    frappe.call({
        'method': 'rezappte.rezappte.page.find_recipe.find_recipe.find_recipe_by_ingredients',
        'args': {
            'ingredients': ingredients
        },
        'callback': function(response) {
            display_recipes(response.message);
        }
    });
}

function display_recipes(recipe_list) {
    for (let v = 0; v < 4; v++) {
        let $recipe = $('.recipe_' + v);
        let $ingredients = $('.ingredients_' + v);
        $recipe.css('display', 'none');
        $ingredients.css('display', 'none');
    }
    for (let i = 0; i < recipe_list.length; i++) {
        let $recipe = $('.recipe_' + i);
        let $ingredients = $('.ingredients_' + i);
        $recipe.html(`<a href="/desk#Form/Rezept/${recipe_list[i].recipe_number}" class="font-color" target="_blank">${recipe_list[i].recipe}</a>`);
        let ingredients_display = recipe_list[i].count + ". Zutaten benötigt: " + recipe_list[i].ingredient_1
        if (recipe_list[i].ingredient_2) {
            ingredients_display = ingredients_display + ", " + recipe_list[i].ingredient_2
        }
        if (recipe_list[i].ingredient_3) {
            ingredients_display = ingredients_display + ", " + recipe_list[i].ingredient_3
        }
        if (recipe_list[i].ingredient_4) {
            ingredients_display = ingredients_display + ", " + recipe_list[i].ingredient_4
        }
        if (recipe_list[i].ingredient_5) {
            ingredients_display = ingredients_display + ", " + recipe_list[i].ingredient5
        }
        $ingredients.text(ingredients_display);
        //~ $ingredients.text("Anzahl verwendeter Zutaten: " + recipe_list[i].count);
        $recipe.css('display', 'block');
        $ingredients.css('display', 'block');
    }
}

function sort_ingredient_fields() {
    for (let i = 1; i < 6; i++) {
        let ingredient_value = $('.ingredient_input_' + i.toString() + ' input').val();
        if (!ingredient_value) {
            let j = i + 1
            let next_value = $('.ingredient_input_' + j.toString() + ' input').val();
            $('.ingredient_input_' + i.toString() + ' input').val(next_value);
            $('.ingredient_input_' + j.toString() + ' input').val('');
        }
    }
    let hide = false
    for (let k = 1; k < 6; k++) {
        if (hide) {
            $('.ingredient_input_' + k.toString()).hide();
        }
        let ingredient_value = $('.ingredient_input_' + k.toString() + ' input').val();
        if (!ingredient_value) {
            hide = true
        }
    }
}
