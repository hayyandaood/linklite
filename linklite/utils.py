import frappe
from frappe.website.path_resolver import resolve_path as orignal_resolve_path


def path_resolver(path: str):
    if frappe.db.exists("Short Link", {"short_link": path}):
        # we want to redirect
        short_link = frappe.db.get_value(
            "Short Link",
            {"short_link": path},
            ["destination_url", "name"],
            as_dict=True,
        )

        click = frappe.new_doc("Short Link Click")

        request_headers = frappe.request.headers
        click.ip = request_headers.get("X-Forwarded-For")
        click.user_agent = request_headers.get("User-Agent")
        click.referer = request_headers.get("Referer")
        frappe.logger().info(f"Referrer URL: {click.referer}")
        click.link = short_link.name
        click.insert()
        click.submit()
        frappe.db.commit() #to remove once MyISAM

        frappe.redirect(short_link.destination_url)

    return orignal_resolve_path(path)