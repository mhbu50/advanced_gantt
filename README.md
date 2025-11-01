# Advanced Gantt Chart for Frappe/ERPNext

A custom Frappe app that provides advanced Gantt chart functionality for ERPNext projects and tasks, with integration support for Bryntum Gantt component.

## Features

- **Interactive Gantt Chart**: Visualize projects and tasks in a timeline view
- **Drag & Drop**: Reschedule tasks by dragging them in the timeline
- **Task Dependencies**: Create and manage task dependencies
- **Progress Tracking**: Update and visualize task progress
- **Project Filtering**: Filter by specific projects and date ranges
- **Real-time Updates**: Sync changes back to ERPNext Project and Task doctypes
- **Responsive Design**: Works on desktop and mobile devices
- **Customizable Settings**: Configure chart behavior and appearance

## Installation

1. **Clone the repository** into your Frappe bench apps directory:
   ```bash
   cd frappe-bench/apps
   git clone https://github.com/mhbu50/advanced_gantt.git
   ```

2. **Install the app** on your site:
   ```bash
   bench --site your-site-name install-app advanced_gantt
   ```

3. **Migrate the database**:
   ```bash
   bench --site your-site-name migrate
   ```

4. **Build assets**:
   ```bash
   bench build
   ```

5. **Restart the server**:
   ```bash
   bench restart
   ```

## Bryntum Gantt Integration

This app is designed to work with the Bryntum Gantt component. To use the full functionality:

1. **Obtain a Bryntum Gantt license** from [Bryntum](https://bryntum.com/products/gantt/)

2. **Download the Bryntum Gantt library** and place the files in:
   - CSS: `advanced_gantt/public/css/bryntum-gantt.css`
   - JS: `advanced_gantt/public/js/bryntum-gantt.js`

3. **Update the license key** in Gantt Chart Settings

4. **Replace placeholder code** in `gantt_component.js` with actual Bryntum initialization

## Usage

### Accessing the Gantt Chart

1. Navigate to the **Advanced Gantt** workspace in ERPNext
2. Click on **Gantt Chart** to open the interactive view
3. Use filters to select specific projects or date ranges

### Features Available

#### Without Bryntum License (Demo Mode)
- View projects and tasks in a table format
- See task progress and assignments
- Export data as JSON
- Basic filtering and refresh functionality

#### With Bryntum License (Full Mode)
- Interactive timeline with drag & drop
- Task resizing and dependency creation
- Real-time progress updates
- Advanced filtering and sorting
- Multiple view presets (day, week, month, year)
- Resource management and assignments

### Configuration

Access **Gantt Chart Settings** to configure:

- **View Settings**: Default view preset, date ranges
- **Interaction**: Enable/disable drag & drop, task editing
- **Integration**: Sync settings with ERPNext updates
- **Customization**: Custom CSS and JavaScript
- **Notifications**: Email alerts for task updates

## API Endpoints

The app provides several API endpoints for data access:

### Get Gantt Data
```javascript
frappe.call({
    method: 'advanced_gantt.api.gantt_data.get_gantt_data',
    args: {
        project: 'PROJECT-001',  // Optional
        start_date: '2024-01-01', // Optional
        end_date: '2024-12-31'    // Optional
    }
});
```

### Update Task Dates
```javascript
frappe.call({
    method: 'advanced_gantt.api.gantt_data.update_task_dates',
    args: {
        task_id: 'TASK-001',
        start_date: '2024-02-01',
        end_date: '2024-02-15'
    }
});
```

### Update Task Progress
```javascript
frappe.call({
    method: 'advanced_gantt.api.gantt_data.update_task_progress',
    args: {
        task_id: 'TASK-001',
        progress: 75
    }
});
```

### Create Task Dependency
```javascript
frappe.call({
    method: 'advanced_gantt.api.gantt_data.create_task_dependency',
    args: {
        from_task: 'TASK-001',
        to_task: 'TASK-002',
        dependency_type: 2  // Finish to Start
    }
});
```

## Data Structure

The app transforms ERPNext Project and Task data into Bryntum Gantt format:

### Projects
- Displayed as parent tasks in the Gantt chart
- Include project timeline, progress, and metadata
- Support hierarchical task organization

### Tasks
- Child tasks under projects or other tasks
- Include start/end dates, progress, assignments
- Support dependencies and milestones

### Dependencies
- Finish-to-Start relationships between tasks
- Automatically created from ERPNext Task dependencies
- Visual representation in timeline

### Resources
- ERPNext users as assignable resources
- Support for resource allocation and workload

## Customization

### Custom CSS
Add custom styles in Gantt Chart Settings:
```css
.gantt-placeholder {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

### Custom JavaScript
Add custom behavior in Gantt Chart Settings:
```javascript
// Custom event handlers
ganttChart.on('taskClick', function(event) {
    console.log('Task clicked:', event.task);
});
```

## Development

### File Structure
```
advanced_gantt/
├── advanced_gantt/
│   ├── api/
│   │   └── gantt_data.py          # API endpoints
│   ├── doctype/
│   │   └── gantt_chart_settings/  # Settings DocType
│   ├── public/
│   │   ├── css/
│   │   │   └── gantt_styles.css   # Styles
│   │   └── js/
│   │       └── gantt_component.js # Main component
│   ├── workspace/
│   │   └── advanced_gantt/        # Workspace definition
│   └── www/
│       ├── gantt.html             # Web page template
│       └── gantt.py               # Page controller
├── hooks.py                       # App hooks
└── README.md
```

### Adding Features

1. **New API endpoints**: Add to `api/gantt_data.py`
2. **UI enhancements**: Modify `public/js/gantt_component.js`
3. **Styling changes**: Update `public/css/gantt_styles.css`
4. **Settings options**: Extend `doctype/gantt_chart_settings/`

## Troubleshooting

### Common Issues

1. **Gantt chart not loading**
   - Check browser console for JavaScript errors
   - Verify assets are built: `bench build`
   - Ensure app is installed: `bench list-apps`

2. **No data showing**
   - Verify you have Project and Task records
   - Check user permissions for Project and Task doctypes
   - Review API endpoint responses in browser network tab

3. **Drag & drop not working**
   - Ensure you have write permissions for Task doctype
   - Check if Bryntum Gantt library is properly loaded
   - Verify settings allow drag & drop functionality

### Debug Mode

Enable debug mode in Gantt Chart Settings to see:
- API request/response data
- JavaScript console logs
- Data transformation details

## License

This app is open source. However, the Bryntum Gantt component requires a separate commercial license from Bryntum.

## Support

For issues and feature requests, please create an issue on the GitHub repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Changelog

### Version 1.0.0
- Initial release
- Basic Gantt chart functionality
- ERPNext Project/Task integration
- Bryntum Gantt support
- Web interface and API endpoints
