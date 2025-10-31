import frappe
from frappe import _
from frappe.utils import getdate, get_datetime, nowdate, add_days
import json


@frappe.whitelist()
def get_gantt_data(project=None, start_date=None, end_date=None):
    """
    Get Gantt chart data from ERPNext Project and Task doctypes
    Returns data in Bryntum Gantt format
    """
    try:
        # Set default date range if not provided
        if not start_date:
            start_date = add_days(nowdate(), -30)
        if not end_date:
            end_date = add_days(nowdate(), 90)
        
        # Get projects data
        projects_data = get_projects_data(project, start_date, end_date)
        
        # Get tasks data
        tasks_data = get_tasks_data(project, start_date, end_date)
        
        # Get dependencies data
        dependencies_data = get_dependencies_data(project)
        
        # Transform data to Bryntum format
        gantt_data = {
            "tasks": transform_tasks_for_bryntum(projects_data, tasks_data),
            "dependencies": transform_dependencies_for_bryntum(dependencies_data),
            "resources": get_resources_data(),
            "assignments": get_assignments_data(project)
        }
        
        return gantt_data
        
    except Exception as e:
        frappe.log_error(f"Error in get_gantt_data: {str(e)}")
        frappe.throw(_("Error fetching Gantt data: {0}").format(str(e)))


def get_projects_data(project=None, start_date=None, end_date=None):
    """Get projects data from ERPNext"""
    filters = {}
    
    if project:
        filters["name"] = project
    
    if start_date and end_date:
        filters["expected_start_date"] = ["between", [start_date, end_date]]
    
    projects = frappe.get_all(
        "Project",
        filters=filters,
        fields=[
            "name", "project_name", "status", "priority", "percent_complete",
            "expected_start_date", "expected_end_date", "actual_start_date", 
            "actual_end_date", "project_type", "department", "company",
            "estimated_costing", "total_costing_amount", "description"
        ]
    )
    
    return projects


def get_tasks_data(project=None, start_date=None, end_date=None):
    """Get tasks data from ERPNext"""
    filters = {}
    
    if project:
        filters["project"] = project
    
    if start_date and end_date:
        filters["exp_start_date"] = ["between", [start_date, end_date]]
    
    tasks = frappe.get_all(
        "Task",
        filters=filters,
        fields=[
            "name", "subject", "status", "priority", "progress", "project",
            "exp_start_date", "exp_end_date", "act_start_date", "act_end_date",
            "expected_time", "actual_time", "parent_task", "task_weight",
            "assigned_to", "department", "company", "description", "is_milestone"
        ]
    )
    
    return tasks


def get_dependencies_data(project=None):
    """Get task dependencies data"""
    filters = {}
    
    if project:
        # Get all tasks for the project first
        project_tasks = frappe.get_all("Task", filters={"project": project}, fields=["name"])
        task_names = [task.name for task in project_tasks]
        if task_names:
            filters["task"] = ["in", task_names]
    
    dependencies = frappe.get_all(
        "Task Depends On",
        filters=filters,
        fields=["parent", "task", "depends_on_task"]
    )
    
    return dependencies


def get_resources_data():
    """Get resources (users/employees) data"""
    resources = frappe.get_all(
        "User",
        filters={"enabled": 1, "user_type": "System User"},
        fields=["name", "full_name", "email", "user_image"]
    )
    
    # Transform to Bryntum format
    bryntum_resources = []
    for resource in resources:
        bryntum_resources.append({
            "id": resource.name,
            "name": resource.full_name or resource.name,
            "email": resource.email,
            "image": resource.user_image
        })
    
    return bryntum_resources


def get_assignments_data(project=None):
    """Get task assignments data"""
    filters = {}
    
    if project:
        # Get all tasks for the project first
        project_tasks = frappe.get_all("Task", filters={"project": project}, fields=["name"])
        task_names = [task.name for task in project_tasks]
        if task_names:
            filters["parent"] = ["in", task_names]
    
    assignments = frappe.get_all(
        "Task Assigned To",
        filters=filters,
        fields=["parent", "assigned_to"]
    )
    
    # Transform to Bryntum format
    bryntum_assignments = []
    for assignment in assignments:
        bryntum_assignments.append({
            "id": f"{assignment.parent}_{assignment.assigned_to}",
            "taskId": assignment.parent,
            "resourceId": assignment.assigned_to,
            "units": 100  # Default to 100% allocation
        })
    
    return bryntum_assignments


def transform_tasks_for_bryntum(projects_data, tasks_data):
    """Transform ERPNext projects and tasks to Bryntum Gantt format"""
    bryntum_tasks = []
    
    # Add projects as parent tasks
    for project in projects_data:
        bryntum_tasks.append({
            "id": f"project_{project.name}",
            "name": project.project_name or project.name,
            "startDate": project.expected_start_date or project.actual_start_date,
            "endDate": project.expected_end_date or project.actual_end_date,
            "percentDone": project.percent_complete or 0,
            "expanded": True,
            "leaf": False,
            "type": "project",
            "status": project.status,
            "priority": project.priority,
            "department": project.department,
            "company": project.company,
            "description": project.description,
            "estimatedCost": project.estimated_costing,
            "actualCost": project.total_costing_amount
        })
    
    # Add tasks as child tasks
    for task in tasks_data:
        parent_id = None
        if task.parent_task:
            parent_id = task.parent_task
        elif task.project:
            parent_id = f"project_{task.project}"
        
        bryntum_tasks.append({
            "id": task.name,
            "name": task.subject,
            "startDate": task.exp_start_date or task.act_start_date,
            "endDate": task.exp_end_date or task.act_end_date,
            "percentDone": task.progress or 0,
            "parentId": parent_id,
            "leaf": True,
            "type": "milestone" if task.is_milestone else "task",
            "status": task.status,
            "priority": task.priority,
            "project": task.project,
            "expectedTime": task.expected_time,
            "actualTime": task.actual_time,
            "weight": task.task_weight,
            "assignedTo": task.assigned_to,
            "department": task.department,
            "company": task.company,
            "description": task.description
        })
    
    return bryntum_tasks


def transform_dependencies_for_bryntum(dependencies_data):
    """Transform ERPNext task dependencies to Bryntum format"""
    bryntum_dependencies = []
    
    for dep in dependencies_data:
        bryntum_dependencies.append({
            "id": f"dep_{dep.parent}_{dep.depends_on_task}",
            "fromTask": dep.depends_on_task,
            "toTask": dep.parent,
            "type": 2,  # Finish to Start dependency
            "lag": 0
        })
    
    return bryntum_dependencies


@frappe.whitelist()
def update_task_dates(task_id, start_date, end_date):
    """Update task dates when dragged in Gantt chart"""
    try:
        if not frappe.has_permission("Task", "write"):
            frappe.throw(_("No permission to update tasks"))
        
        task_doc = frappe.get_doc("Task", task_id)
        task_doc.exp_start_date = getdate(start_date)
        task_doc.exp_end_date = getdate(end_date)
        task_doc.save()
        
        return {"status": "success", "message": _("Task dates updated successfully")}
        
    except Exception as e:
        frappe.log_error(f"Error updating task dates: {str(e)}")
        frappe.throw(_("Error updating task dates: {0}").format(str(e)))


@frappe.whitelist()
def update_task_progress(task_id, progress):
    """Update task progress"""
    try:
        if not frappe.has_permission("Task", "write"):
            frappe.throw(_("No permission to update tasks"))
        
        task_doc = frappe.get_doc("Task", task_id)
        task_doc.progress = float(progress)
        task_doc.save()
        
        return {"status": "success", "message": _("Task progress updated successfully")}
        
    except Exception as e:
        frappe.log_error(f"Error updating task progress: {str(e)}")
        frappe.throw(_("Error updating task progress: {0}").format(str(e)))


@frappe.whitelist()
def create_task_dependency(from_task, to_task, dependency_type=2):
    """Create a new task dependency"""
    try:
        if not frappe.has_permission("Task", "write"):
            frappe.throw(_("No permission to create dependencies"))
        
        # Check if dependency already exists
        existing = frappe.db.exists("Task Depends On", {
            "parent": to_task,
            "depends_on_task": from_task
        })
        
        if existing:
            return {"status": "exists", "message": _("Dependency already exists")}
        
        # Add dependency to the task
        task_doc = frappe.get_doc("Task", to_task)
        task_doc.append("depends_on", {
            "depends_on_task": from_task
        })
        task_doc.save()
        
        return {"status": "success", "message": _("Dependency created successfully")}
        
    except Exception as e:
        frappe.log_error(f"Error creating task dependency: {str(e)}")
        frappe.throw(_("Error creating task dependency: {0}").format(str(e)))