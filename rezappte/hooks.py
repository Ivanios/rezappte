# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "rezappte"
app_title = "Rezappte"
app_publisher = "Ivanios"
app_description = "An app to manage your recipes and share them with your friends. With additional functions."
app_icon = "octicon octicon-file-directory"
app_color = "black"
app_email = "gokuflynn@gmail.com"
app_license = "MIT"

#Rezappte specific changes
home_page = "welcome"
website_route_rules = [
	{"from_route": "/me", "to_route": "dashboard"}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/rezappte/css/rezappte.css"
# app_include_js = "/assets/rezappte/js/rezappte.js"

# include js, css files in header of web template
# web_include_css = "/assets/rezappte/css/rezappte.css"
# web_include_js = "/assets/rezappte/js/rezappte.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "rezappte.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "rezappte.install.before_install"
# after_install = "rezappte.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rezappte.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "rezappte.rezappte.doctype.shopping_list.shopping_list.delete_shopping_lists"
    ]
}

# Testing
# -------

# before_tests = "rezappte.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "rezappte.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "rezappte.task.get_dashboard_data"
# }

