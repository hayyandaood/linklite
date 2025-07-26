# Copyright (c) 2025, Hayyan Daood and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShortLink(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.SmallText | None
		destination_url: DF.Data
		short_link: DF.Data
	# end: auto-generated types
	def before_insert(self):
		self.validate_black_listed_slug()
		self.validate_nested_slug()
	
	def validate_black_listed_slug(self):
		if frappe.db.exists("Black Listed Slug",self.short_link):
			frappe.throw(f"Slug {frappe.bold(self.short_link)} is not allowed!")

	def validate_nested_slug(self):
		if "/" in self.short_link:
			frappe.throw("Short link Cannot contain '/'!")
	def on_trash(self):
		#delete the short links clicks records .
		frappe.db.delete("Short Link Click", {"link": self.name})