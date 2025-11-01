import frappe
from frappe.model.document import Document

class GanttChartSettings(Document):
    def validate(self):
        """Validate Gantt Chart Settings"""
        if self.default_start_date_offset < 0:
            frappe.throw("Start date offset cannot be negative")
        
        if self.default_end_date_offset < 0:
            frappe.throw("End date offset cannot be negative")
        
        if self.auto_refresh_interval < 0:
            frappe.throw("Auto refresh interval cannot be negative")
    
    def on_update(self):
        """Clear cache when settings are updated"""
        frappe.cache().delete_key("gantt_chart_settings")
    
    @staticmethod
    def get_settings():
        """Get Gantt Chart Settings with caching"""
        settings = frappe.cache().get_value("gantt_chart_settings")
        
        if not settings:
            try:
                settings_doc = frappe.get_single("Gantt Chart Settings")
                settings = {
                    "default_view_preset": settings_doc.default_view_preset or "weekAndDayLetter",
                    "default_start_date_offset": settings_doc.default_start_date_offset or 30,
                    "default_end_date_offset": settings_doc.default_end_date_offset or 90,
                    "auto_refresh_interval": settings_doc.auto_refresh_interval or 0,
                    "show_progress_line": settings_doc.show_progress_line,
                    "show_dependencies": settings_doc.show_dependencies,
                    "enable_task_editing": settings_doc.enable_task_editing,
                    "enable_drag_drop": settings_doc.enable_drag_drop,
                    "bryntum_license_key": settings_doc.bryntum_license_key,
                    "custom_css": settings_doc.custom_css,
                    "custom_js": settings_doc.custom_js,
                    "sync_with_project_updates": settings_doc.sync_with_project_updates,
                    "update_task_dates_on_drag": settings_doc.update_task_dates_on_drag,
                    "create_dependencies_on_link": settings_doc.create_dependencies_on_link,
                    "send_email_on_task_update": settings_doc.send_email_on_task_update
                }
                frappe.cache().set_value("gantt_chart_settings", settings, expires_in_sec=3600)
            except:
                # Return default settings if document doesn't exist
                settings = {
                    "default_view_preset": "weekAndDayLetter",
                    "default_start_date_offset": 30,
                    "default_end_date_offset": 90,
                    "auto_refresh_interval": 0,
                    "show_progress_line": True,
                    "show_dependencies": True,
                    "enable_task_editing": True,
                    "enable_drag_drop": True,
                    "bryntum_license_key": "",
                    "custom_css": "",
                    "custom_js": "",
                    "sync_with_project_updates": True,
                    "update_task_dates_on_drag": True,
                    "create_dependencies_on_link": True,
                    "send_email_on_task_update": False
                }
        
        return settings