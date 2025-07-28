// Copyright (c) 2025, Hayyan Daood and contributors
// For license information, please see license.txt

frappe.ui.form.on("Short Link", {
	refresh(frm) {
        frm.sidebar
			.add_user_action(__("Copy Short Code"))
			.attr("href", "#")
			.on("click", () => {
				const url = frappe.urllib.get_full_url(frm.doc.short_link);
				frappe.utils.copy_to_clipboard(url, __("Short Link copied"));
			});

		frm.add_custom_button("Regenerate QR Code", () => {
			frm.call('generate_qr_code').then(() => {
				frappe.show_alert("Regenerated!")
				frm.refresh()
			})
		})
	},
});
