# Copyright (c) 2025, Hayyan Daood and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BlackListedSlug(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		slug: DF.Data | None
	# end: auto-generated types
	pass
