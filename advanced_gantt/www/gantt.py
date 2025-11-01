import frappe
from frappe import _

def get_context(context):
    """Get context for Gantt page"""
    context.no_cache = 1
    context.title = _("Advanced Gantt Chart")
    
    # Get projects for filter dropdown
    projects = frappe.get_all(
        "Project",
        fields=["name", "project_name", "status"],
        filters={"status": ["!=", "Cancelled"]},
        order_by="modified desc",
        limit=100
    )
    
    context.projects = projects
    
    # Get current user permissions
    context.can_write = frappe.has_permission("Task", "write")
    context.can_create = frappe.has_permission("Task", "create")
    
    return context