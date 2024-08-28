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
    
    set_colors();
    });
};

function set_colors() {
    frappe.call({
        'method': 'rezappte.rezappte.page.find_recipe.find_recipe.get_colors',
        //~ 'args': {
            //~ 'project': frm.doc.name,
            //~ 'objekt': frm.doc.object
        //~ },
        'callback': function(response) {
            console.log(response.message);
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

function show_option(div_id) {
    var $element = $('#' + div_id); // Stelle sicher, dass elementId ein String ist
    
    if ($element.length > 0) { // Überprüfe, ob das Element existiert
        if ($element.is(':visible')) {
            // Element ist sichtbar, also verstecke es
            $element.hide();
        } else {
            // Element ist versteckt, also zeige es an
            $element.show();
        }
    } else {
        console.error('Element mit ID ' + div_id + ' wurde nicht gefunden.');
    }
}
