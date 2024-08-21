from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Kochen"),
			"items": [
				{
					"type": "doctype",
					"name": "Rezept",
				},
				{
					"type": "page",
					"name": "rezept_kochen",
					"label": "Rezept Kochen"
				},
			]
		},
		{
			"label": _("Einkaufen"),
			"items": [
				{
					"type": "doctype",
					"name": "Einkaufsliste",
				}
			]
		},
		{
			"label": _("Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "User Card",
				}
			]
		},
        {
			"label": _("Daten"),
			"items": [
				{
					"type": "doctype",
					"name": "Zutaten",
				},
                {
					"type": "doctype",
					"name": "uom",
				},
                {
					"type": "doctype",
					"name": "Origin",
				},
				{
					"type": "doctype",
					"name": "Market",
				},
			]
		},
	]
