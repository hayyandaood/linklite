import frappe 
from frappe.website.path_resolver import resolve_path as orignal_resolve_path

def path_resolver(path: str):
    #if we want to handle the short link
    #frappe.redirect("https://google.com")

    #else pass it on!
    #return orignal_resolve_path(path)
    if frappe.db.exists("Short Link",{"short_link" : path}):
        #we want to redirect
        destination_url = frappe.db.get_value("Short Link", {"short_link" : path}, "destination_url")
        frappe.redirect(destination_url)
    
    