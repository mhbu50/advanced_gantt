/**
 * Advanced Gantt Chart Component for Frappe
 * Integrates Bryntum Gantt with ERPNext Project and Task data
 */

class AdvancedGanttChart {
    constructor(options = {}) {
        this.container = options.container || '#gantt-container';
        this.project = options.project || null;
        this.startDate = options.startDate || null;
        this.endDate = options.endDate || null;
        this.gantt = null;
        this.data = null;
        
        this.init();
    }
    
    async init() {
        try {
            // Load Bryntum Gantt resources
            await this.loadBryntumResources();
            
            // Fetch data from ERPNext
            await this.fetchGanttData();
            
            // Initialize Bryntum Gantt
            this.initializeBryntumGantt();
            
        } catch (error) {
            console.error('Error initializing Gantt chart:', error);
            frappe.msgprint(__('Error loading Gantt chart: {0}', [error.message]));
        }
    }
    
    async loadBryntumResources() {
        // Note: In a real implementation, you would need to include Bryntum Gantt files
        // This is a placeholder for the Bryntum Gantt library loading
        
        if (typeof bryntum === 'undefined') {
            // Load Bryntum CSS
            const cssLink = document.createElement('link');
            cssLink.rel = 'stylesheet';
            cssLink.href = '/assets/advanced_gantt/css/bryntum-gantt.css';
            document.head.appendChild(cssLink);
            
            // Load Bryntum JS
            const script = document.createElement('script');
            script.src = '/assets/advanced_gantt/js/bryntum-gantt.js';
            document.head.appendChild(script);
            
            // Wait for script to load
            await new Promise((resolve, reject) => {
                script.onload = resolve;
                script.onerror = reject;
            });
        }
    }
    
    async fetchGanttData() {
        try {
            const response = await frappe.call({
                method: 'advanced_gantt.api.gantt_data.get_gantt_data',
                args: {
                    project: this.project,
                    start_date: this.startDate,
                    end_date: this.endDate
                }
            });
            
            this.data = response.message;
            
        } catch (error) {
            console.error('Error fetching Gantt data:', error);
            throw new Error('Failed to fetch Gantt data from server');
        }
    }
    
    initializeBryntumGantt() {
        // Note: This is a placeholder implementation
        // In a real scenario, you would need the actual Bryntum Gantt library
        
        const ganttConfig = {
            appendTo: this.container,
            
            // Data configuration
            project: {
                tasks: this.data.tasks,
                dependencies: this.data.dependencies,
                resources: this.data.resources,
                assignments: this.data.assignments
            },
            
            // UI Configuration
            columns: [
                { type: 'name', field: 'name', text: 'Task Name', width: 250 },
                { type: 'startdate', field: 'startDate', text: 'Start Date', width: 100 },
                { type: 'enddate', field: 'endDate', text: 'End Date', width: 100 },
                { type: 'duration', field: 'duration', text: 'Duration', width: 80 },
                { type: 'percentdone', field: 'percentDone', text: 'Progress', width: 80 },
                { type: 'resourceassignment', field: 'assignments', text: 'Assigned To', width: 150 }
            ],
            
            // Features
            features: {
                taskEdit: {
                    editorConfig: {
                        title: 'Edit Task'
                    }
                },
                dependencies: true,
                taskResize: true,
                taskDrag: true,
                progressLine: {
                    statusDate: new Date()
                },
                filter: true,
                sort: true,
                columnLines: true,
                timeRanges: true,
                labels: {
                    left: {
                        field: 'name'
                    }
                }
            },
            
            // Event listeners
            listeners: {
                taskDrop: this.onTaskDrop.bind(this),
                taskResize: this.onTaskResize.bind(this),
                progressChange: this.onProgressChange.bind(this),
                dependencyCreate: this.onDependencyCreate.bind(this)
            },
            
            // Timeline configuration
            startDate: this.startDate || new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
            endDate: this.endDate || new Date(Date.now() + 90 * 24 * 60 * 60 * 1000),
            
            // View preset
            viewPreset: 'weekAndDayLetter'
        };
        
        // Initialize Bryntum Gantt (placeholder)
        // this.gantt = new bryntum.gantt.Gantt(ganttConfig);
        
        // For now, create a placeholder UI
        this.createPlaceholderUI();
    }
    
    createPlaceholderUI() {
        const container = document.querySelector(this.container);
        if (!container) return;
        
        container.innerHTML = `
            <div class="gantt-placeholder">
                <div class="gantt-header">
                    <h3>Advanced Gantt Chart</h3>
                    <div class="gantt-controls">
                        <button class="btn btn-primary btn-sm" onclick="ganttChart.refreshData()">
                            <i class="fa fa-refresh"></i> Refresh
                        </button>
                        <button class="btn btn-secondary btn-sm" onclick="ganttChart.exportData()">
                            <i class="fa fa-download"></i> Export
                        </button>
                    </div>
                </div>
                <div class="gantt-content">
                    <div class="gantt-grid">
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th>Task Name</th>
                                    <th>Start Date</th>
                                    <th>End Date</th>
                                    <th>Progress</th>
                                    <th>Assigned To</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${this.renderTaskRows()}
                            </tbody>
                        </table>
                    </div>
                    <div class="gantt-timeline">
                        <div class="timeline-placeholder">
                            <p><strong>Bryntum Gantt Timeline</strong></p>
                            <p>This is a placeholder for the Bryntum Gantt timeline.</p>
                            <p>To use the actual Bryntum Gantt component, you need to:</p>
                            <ol>
                                <li>Obtain a Bryntum Gantt license</li>
                                <li>Include the Bryntum Gantt library files</li>
                                <li>Replace the placeholder code with actual Bryntum initialization</li>
                            </ol>
                            <div class="data-preview">
                                <h5>Data Preview:</h5>
                                <pre>${JSON.stringify(this.data, null, 2)}</pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    renderTaskRows() {
        if (!this.data || !this.data.tasks) return '<tr><td colspan="5">No tasks found</td></tr>';
        
        return this.data.tasks.map(task => `
            <tr>
                <td>${task.name || ''}</td>
                <td>${task.startDate || ''}</td>
                <td>${task.endDate || ''}</td>
                <td>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar" role="progressbar" 
                             style="width: ${task.percentDone || 0}%"
                             aria-valuenow="${task.percentDone || 0}" 
                             aria-valuemin="0" aria-valuemax="100">
                            ${task.percentDone || 0}%
                        </div>
                    </div>
                </td>
                <td>${task.assignedTo || ''}</td>
            </tr>
        `).join('');
    }
    
    // Event handlers for Bryntum Gantt interactions
    async onTaskDrop(event) {
        const { task } = event;
        try {
            await frappe.call({
                method: 'advanced_gantt.api.gantt_data.update_task_dates',
                args: {
                    task_id: task.id,
                    start_date: task.startDate,
                    end_date: task.endDate
                }
            });
            
            frappe.show_alert({
                message: __('Task dates updated successfully'),
                indicator: 'green'
            });
            
        } catch (error) {
            console.error('Error updating task dates:', error);
            frappe.msgprint(__('Error updating task dates: {0}', [error.message]));
        }
    }
    
    async onTaskResize(event) {
        const { task } = event;
        try {
            await frappe.call({
                method: 'advanced_gantt.api.gantt_data.update_task_dates',
                args: {
                    task_id: task.id,
                    start_date: task.startDate,
                    end_date: task.endDate
                }
            });
            
            frappe.show_alert({
                message: __('Task duration updated successfully'),
                indicator: 'green'
            });
            
        } catch (error) {
            console.error('Error updating task duration:', error);
            frappe.msgprint(__('Error updating task duration: {0}', [error.message]));
        }
    }
    
    async onProgressChange(event) {
        const { task } = event;
        try {
            await frappe.call({
                method: 'advanced_gantt.api.gantt_data.update_task_progress',
                args: {
                    task_id: task.id,
                    progress: task.percentDone
                }
            });
            
            frappe.show_alert({
                message: __('Task progress updated successfully'),
                indicator: 'green'
            });
            
        } catch (error) {
            console.error('Error updating task progress:', error);
            frappe.msgprint(__('Error updating task progress: {0}', [error.message]));
        }
    }
    
    async onDependencyCreate(event) {
        const { dependency } = event;
        try {
            await frappe.call({
                method: 'advanced_gantt.api.gantt_data.create_task_dependency',
                args: {
                    from_task: dependency.fromTask,
                    to_task: dependency.toTask,
                    dependency_type: dependency.type
                }
            });
            
            frappe.show_alert({
                message: __('Task dependency created successfully'),
                indicator: 'green'
            });
            
        } catch (error) {
            console.error('Error creating task dependency:', error);
            frappe.msgprint(__('Error creating task dependency: {0}', [error.message]));
        }
    }
    
    // Utility methods
    async refreshData() {
        try {
            await this.fetchGanttData();
            if (this.gantt) {
                this.gantt.project.loadInlineData(this.data);
            } else {
                this.createPlaceholderUI();
            }
            
            frappe.show_alert({
                message: __('Gantt data refreshed successfully'),
                indicator: 'green'
            });
            
        } catch (error) {
            console.error('Error refreshing data:', error);
            frappe.msgprint(__('Error refreshing data: {0}', [error.message]));
        }
    }
    
    exportData() {
        if (!this.data) return;
        
        const dataStr = JSON.stringify(this.data, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `gantt_data_${frappe.datetime.now_datetime()}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        frappe.show_alert({
            message: __('Gantt data exported successfully'),
            indicator: 'green'
        });
    }
    
    destroy() {
        if (this.gantt) {
            this.gantt.destroy();
        }
    }
}

// Global reference for easy access
window.AdvancedGanttChart = AdvancedGanttChart;