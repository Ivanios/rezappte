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
					"type": "doctype",
					"name": "Zutaten",
				}
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
	]
