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
        $('#page-find-recipe').css({
            'background-color': 'red'
        });
    });
};

//~ frappe.rezept_finden = {
	//~ make: function(page) {
		//~ var me = frappe.rezept_finden;
        //~ me.page = page;
        //~ console.log("Hallo");
        //~ me.body = $('<div style="background-color: black;" id="container-rezept-finden"></div>').appendTo(me.page.main);
	//~ },
	//~ run: function() {
		//~ console.log("run");
	//~ },
	//~ display: function() {
		//~ console.log("display");
	//~ }
//~ }
