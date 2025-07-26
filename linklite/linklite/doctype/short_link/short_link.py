# Copyright (c) 2025, Hayyan Daood and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShortLink(Document):
	def on_trash(self):
		#delete the short links clicks records .
		frappe.db.delete("Short Link Click", {"link": self.name})
			
