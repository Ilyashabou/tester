import os
import json
from datetime import datetime
from jinja2 import Template

def generate_report(results, out_file="report.html"):
    # Calculate overall statistics
    total_elements = 0
    working_elements = 0
    elements_by_type = {}
    
    # Create a structure to store detailed page-level statistics
    pages_stats = []

    for result in results:
        page_stats = {
            'url': result['url'],
            'total_elements': 0,
            'working_elements': 0,
            'elements_by_type': {},
            'non_working_elements': {}
        }

        for element in result.get('element_results', []):
            element_type = element.get('element_type', 'unknown')
            element_description = element.get('description', '')
            element_selector = element.get('selector', '')
            is_working = element.get('is_working', False)
            error_message = element.get('error_message', '')
            page_change_detected = element.get('page_change_detected', False)
            visual_change_detected = element.get('visual_change_detected', False)
            
            # Count total elements for global stats
            total_elements += 1
            
            # Count total elements for page stats
            page_stats['total_elements'] += 1
            
            # Count working elements for global stats
            if is_working:
                working_elements += 1
                page_stats['working_elements'] += 1
            
            # Count by type for global stats
            if element_type not in elements_by_type:
                elements_by_type[element_type] = {
                    'total': 0,
                    'working': 0
                }
            elements_by_type[element_type]['total'] += 1
            if is_working:
                elements_by_type[element_type]['working'] += 1
                
            # Count by type for page stats
            if element_type not in page_stats['elements_by_type']:
                page_stats['elements_by_type'][element_type] = {
                    'total': 0,
                    'working': 0
                }
            page_stats['elements_by_type'][element_type]['total'] += 1
            if is_working:
                page_stats['elements_by_type'][element_type]['working'] += 1
            
            # Track non-working elements in a dictionary where keys are element types
            # This makes it compatible with any existing code that expects .items() method
            if not is_working:
                if element_type not in page_stats['non_working_elements']:
                    page_stats['non_working_elements'][element_type] = []
                
                page_stats['non_working_elements'][element_type].append({
                    'description': element_description,
                    'selector': element_selector,
                    'error_message': error_message,
                    'page_change_detected': page_change_detected,
                    'visual_change_detected': visual_change_detected,
                    'is_working': is_working
                })
        
        # Add the page stats to the list
        pages_stats.append(page_stats)

    # Debug the structure of pages_stats
    print("\nDEBUG - Structure of pages_stats:")
    for i, page in enumerate(pages_stats):
        print(f"Page {i}: URL={page['url']}")
        print(f"  non_working_elements type: {type(page['non_working_elements'])}")
        if isinstance(page['non_working_elements'], list):
            print(f"  non_working_elements is a list with {len(page['non_working_elements'])} items")
        else:
            print(f"  non_working_elements is a {type(page['non_working_elements']).__name__}")
            
    # Calculate percentages
    working_percentage = (working_elements / max(1, total_elements)) * 100

    # Create the HTML report
    template_str = """
    <html>
    <head>
        <title>UI Element Test Report</title>
        <style>
            /* Modern, clean styling */
            body { 
                font-family: 'Segoe UI', Roboto, Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                background-color: #f8f9fa; 
                color: #333; 
                line-height: 1.6;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            header {
                background: linear-gradient(135deg, #4a6bff, #2541b2);
                color: white;
                padding: 30px 20px;
                text-align: center;
                border-radius: 8px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            h1 { 
                margin: 0; 
                font-size: 2.5em; 
                font-weight: 300;
            }
            h2 { 
                color: #2541b2; 
                font-size: 1.8em; 
                margin-top: 30px; 
                padding-bottom: 10px; 
                border-bottom: 2px solid #e9ecef;
            }
            h3 { 
                color: #3a56e4; 
                font-size: 1.4em; 
                margin-top: 25px;
            }
            
            /* Cards for sections */
            .card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                margin-bottom: 25px;
                overflow: hidden;
            }
            .card-header {
                background-color: #f1f4f9;
                padding: 15px 20px;
                border-bottom: 1px solid #e9ecef;
                font-weight: 600;
                font-size: 1.2em;
            }
            .card-body {
                padding: 20px;
            }
            
            /* Status colors */
            .success { color: #28a745; }
            .warning { color: #ffc107; }
            .fail { color: #dc3545; }
            
            /* Modern tables */
            table { 
                border-collapse: collapse; 
                width: 100%; 
                margin-bottom: 20px; 
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 0 0 1px #e9ecef;
            }
            th, td { 
                padding: 12px 15px; 
                text-align: left; 
                border: none;
            }
            th { 
                background-color: #f1f4f9; 
                color: #2541b2;
                font-weight: 600;
            }
            tr:nth-child(even) { background-color: #f8f9fa; }
            tr:hover { background-color: #f1f4f9; }
            
            /* Better progress bars */
            .progress-bar-container { 
                width: 100%; 
                background-color: #e9ecef; 
                border-radius: 30px; 
                height: 10px;
                overflow: hidden;
            }
            .progress-bar { 
                height: 100%; 
                border-radius: 30px; 
                text-align: center; 
                color: white; 
                font-size: 12px;
                line-height: 10px;
                transition: width 0.5s ease;
            }
            .progress-high { background-color: #28a745; }
            .progress-medium { background-color: #ffc107; }
            .progress-low { background-color: #dc3545; }
            
            /* Simple collapsible sections */
            .collapsible { 
                cursor: pointer; 
                padding: 12px 15px; 
                width: 100%; 
                border: none; 
                text-align: left; 
                outline: none; 
                font-size: 1em;
                background-color: #f1f4f9;
                color: #2541b2;
                border-radius: 4px;
                margin-bottom: 5px;
                transition: all 0.3s ease;
                position: relative;
            }
            .collapsible:after {
                content: '+';
                font-weight: bold;
                position: absolute;
                right: 15px;
                top: 50%;
                transform: translateY(-50%);
            }
            .active:after {
                content: '-';
            }
            .active, .collapsible:hover { 
                background-color: #e9ecef; 
            }
            .content { 
                padding: 15px; 
                display: none; 
                background-color: white;
                border-radius: 0 0 4px 4px;
                margin-bottom: 10px;
                border: 1px solid #e9ecef;
                border-top: none;
            }
            
            /* Nested collapsible elements */
            .nested-collapsible {
                background-color: #e9ecef;
                margin-top: 5px;
                margin-bottom: 5px;
            }
            .nested-content {
                background-color: #f8f9fa;
                border-radius: 0;
                margin-bottom: 10px;
            }
            
            /* Element display */
            .element-row { 
                margin-bottom: 15px; 
                padding: 10px; 
                border-radius: 4px; 
                background-color: #f8f9fa;
                border-left: 4px solid #e9ecef;
            }
            .element-row.working { border-left-color: #28a745; }
            .element-row.not-working { border-left-color: #dc3545; }
            .element-type { 
                font-weight: 600; 
                color: #2541b2;
                margin-bottom: 5px;
            }
            .element-description { 
                font-size: 1em; 
                margin-bottom: 5px;
            }
            .element-selector { 
                font-family: monospace; 
                font-size: 0.85em; 
                color: #6c757d; 
                background-color: #f1f4f9;
                padding: 3px 6px;
                border-radius: 3px;
                display: inline-block;
                margin-top: 5px;
            }
            
            /* Element styling */
            .element-row {
                border: 1px solid #e9ecef;
                padding: 10px 15px;
                margin-bottom: 10px;
                border-radius: 4px;
                background-color: white;
            }
            .element-row.not-working {
                border-left: 3px solid #dc3545;
            }
            .element-item {
                border: 1px solid #e9ecef;
                border-radius: 4px;
                margin-bottom: 10px;
                background-color: white;
            }
            .element-summary {
                padding: 10px 15px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 10px;
            }
            .element-details {
                padding: 10px 15px;
                background-color: #f8f9fa;
                border-top: 1px solid #e9ecef;
                font-size: 0.9em;
            }
            .element-type {
                font-weight: 600;
                color: #2541b2;
                margin-right: 10px;
            }
            .element-description {
                color: #495057;
                flex-grow: 1;
            }
            .element-selector {
                font-family: monospace;
                font-size: 0.9em;
                color: #6c757d;
                margin-top: 5px;
                word-break: break-all;
            }
            .element-status {
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 0.85em;
                font-weight: 500;
            }
            .status-success {
                background-color: #d4edda;
                color: #28a745;
            }
            .status-failure {
                background-color: #f8d7da;
                color: #dc3545;
            }
            .details-btn {
                background-color: #f1f4f9;
                border: 1px solid #d6dce7;
                color: #2541b2;
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.85em;
                transition: all 0.2s ease;
            }
            .details-btn:hover {
                background-color: #e9ecef;
            }
            
            /* Charts and stats */
            .stats-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 20px;
            }
            .stat-card {
                flex: 1;
                min-width: 200px;
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                text-align: center;
            }
            .stat-number {
                font-size: 2.5em;
                font-weight: 300;
                margin: 10px 0;
            }
            .stat-label {
                font-size: 0.9em;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .chart-container {
                height: 300px;
                margin-bottom: 30px;
            }
            
            /* Screenshots */
            .screenshots-container { 
                display: flex; 
                gap: 15px; 
                margin-top: 10px;
            }
            .screenshot-container { 
                text-align: center; 
                flex: 1;
            }
            .screenshot { 
                max-width: 100%; 
                border-radius: 4px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
                transition: transform 0.3s ease;
            }
            .screenshot:hover {
                transform: scale(1.05);
            }
            .screenshot-label { 
                font-size: 0.8em; 
                color: #6c757d; 
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>UI Element Test Report</h1>
                <p>Generated on {{ timestamp }}</p>
            </header>

            <!-- Dashboard Statistics -->
            <div class="card">
                <div class="card-header">Dashboard</div>
                <div class="card-body">
                    <div class="stats-container">
                        <div class="stat-card">
                            <div class="stat-label">Total Elements</div>
                            <div class="stat-number">{{ total_elements }}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Working Elements</div>
                            <div class="stat-number" style="color: {{ '#28a745' if working_percentage >= 70 else '#ffc107' if working_percentage >= 40 else '#dc3545' }}">
                                {{ working_percentage|round(1) }}%
                            </div>
                            <div>{{ working_elements }} of {{ total_elements }}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Pages Tested</div>
                            <div class="stat-number">{{ pages_stats|length }}</div>
                        </div>
                    </div>
                    
                    <!-- Simple visual representation instead of charts -->
                    <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 20px;">
                        <div style="flex: 1; min-width: 300px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <h3>Element Working Status</h3>
                            <div style="display: flex; align-items: center; margin-top: 20px;">
                                <!-- Working elements visual -->
                                <div style="flex: {{ working_percentage|round(0)|int }}; height: 40px; background-color: #28a745; border-radius: 4px 0 0 4px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                                    {{ working_percentage|round(1) }}%
                                </div>
                                <!-- Non-working elements visual -->
                                {% if working_percentage < 100 %}
                                <div style="flex: {{ 100 - working_percentage|round(0)|int }}; height: 40px; background-color: #dc3545; border-radius: 0 4px 4px 0; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                                    {{ (100 - working_percentage)|round(1) }}%
                                </div>
                                {% endif %}
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                                <div><span style="display: inline-block; width: 12px; height: 12px; background-color: #28a745; border-radius: 2px; margin-right: 5px;"></span> Working ({{ working_elements }})</div>
                                <div><span style="display: inline-block; width: 12px; height: 12px; background-color: #dc3545; border-radius: 2px; margin-right: 5px;"></span> Not Working ({{ total_elements - working_elements }})</div>
                            </div>
                        </div>
                        
                        <div style="flex: 1; min-width: 300px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <h3>Elements by Type</h3>
                            <div style="margin-top: 20px;">
                                {% for type, stats in elements_by_type.items() %}
                                {% set success_rate = (stats.working / stats.total * 100)|round(1) %}
                                <div style="margin-bottom: 15px;">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                        <div style="font-weight: 600;">{{ type|title }}</div>
                                        <div>{{ stats.working }}/{{ stats.total }} ({{ success_rate }}%)</div>
                                    </div>
                                    <div style="height: 10px; background-color: #e9ecef; border-radius: 5px; overflow: hidden;">
                                        <div style="height: 100%; width: {{ success_rate }}%; background-color: {% if success_rate >= 70 %}#28a745{% elif success_rate >= 40 %}#ffc107{% else %}#dc3545{% endif %};"></div>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>



            <!-- Page Analysis Card -->
            <div class="card">
                <div class="card-header">Page Analysis</div>
                <div class="card-body">
                    <table>
                        <tr>
                            <th>Page URL</th>
                            <th>Elements</th>
                            <th>Working</th>
                            <th>Success Rate</th>
                            <th>Details</th>
                        </tr>
                        {% for page in pages_stats %}
                        {% set page_success_rate = (page.working_elements / page.total_elements * 100) if page.total_elements > 0 else 0 %}
                        <tr>
                            <td title="{{ page.url }}">{{ page.url }}</td>
                            <td>{{ page.total_elements }}</td>
                            <td>{{ page.working_elements }}</td>
                            <td>
                                <div class="progress-bar-container">
                                    <div class="progress-bar {{ 'progress-high' if page_success_rate >= 70 else 'progress-medium' if page_success_rate >= 40 else 'progress-low' }}" style="width: {{ page_success_rate|round(1) }}%">
                                    </div>
                                </div>
                                <div style="text-align: right; font-size: 0.9em; margin-top: 3px;">{{ page_success_rate|round(1) }}%</div>
                            </td>
                            <td>
                                <button class="collapsible">Details</button>
                                <div class="content">
                                    <div class="content-inner">
                                        <!-- Element Type Summary -->
                                        <div style="margin-bottom: 20px;">
                                            <h4>Elements by Type</h4>
                                            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                                                {% for type, stats in page.elements_by_type.items() %}
                                                {% set type_success_rate = (stats.working / stats.total * 100) if stats.total > 0 else 0 %}
                                                <div style="flex: 1; min-width: 150px; background: #f8f9fa; padding: 10px; border-radius: 4px; text-align: center;">
                                                    <div style="font-weight: 600; color: #2541b2;">{{ type|title }}</div>
                                                    <div style="font-size: 1.5em; margin: 5px 0;">{{ stats.working }}/{{ stats.total }}</div>
                                                    <div class="progress-bar-container" style="margin-top: 5px;">
                                                        <div class="progress-bar {{ 'progress-high' if type_success_rate >= 70 else 'progress-medium' if type_success_rate >= 40 else 'progress-low' }}" style="width: {{ type_success_rate|round(1) }}%">
                                                        </div>
                                                    </div>
                                                    <div style="font-size: 0.8em; margin-top: 3px;">{{ type_success_rate|round(1) }}% working</div>
                                                </div>
                                                {% endfor %}
                                            </div>
                                        </div>
                                        
                                        <!-- Non-Working Elements Summary -->
                                        {% if page.non_working_elements %}
                                        <div>
                                            <h4>Issues Found</h4>
                                            <div class="accordion">
                                                {% for type, elements in page.non_working_elements.items() %}
                                                <button class="collapsible nested-collapsible">{{ type|title }} Issues ({{ elements|length }})</button>
                                                <div class="content nested-content">
                                                    <div class="content-inner">
                                                        <div style="max-height: 300px; overflow-y: auto;">
                                                            {% for element in elements %}
                                                            <div style="background: #f8f9fa; padding: 10px; margin-bottom: 10px; border-radius: 4px; border-left: 3px solid #dc3545;">
                                                                <div style="font-weight: 600;">{{ element.description or 'No description' }}</div>
                                                                <div class="element-selector">{{ element.selector|truncate(100) }}</div>
                                                                {% if element.error %}
                                                                <div style="color: #dc3545; margin-top: 5px; font-size: 0.9em;">{{ element.error|truncate(150) }}</div>
                                                                {% endif %}
                                                            </div>
                                                            {% endfor %}
                                                        </div>
                                                    </div>
                                                </div>
                                                {% endfor %}
                                            </div>
                                        </div>
                                        {% else %}
                                        <div style="text-align: center; padding: 20px; background: #f1f9f1; border-radius: 4px; color: #28a745;">
                                            <div style="font-size: 1.2em; font-weight: 600;">✓ All elements on this page are working correctly!</div>
                                        </div>
                                        {% endif %}
                                    </div>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>



        <script>
        // Initialize all collapsible elements
        window.onload = function() {
            // Get all collapsible elements
            var collapsibles = document.getElementsByClassName('collapsible');
            
            // Add click event to each collapsible
            for (var i = 0; i < collapsibles.length; i++) {
                collapsibles[i].onclick = function() {
                    // Toggle active class
                    this.classList.toggle('active');
                    
                    // Get the next element (content)
                    var content = this.nextElementSibling;
                    
                    // Toggle display
                    if (content.style.display === 'block' || content.style.display === '') {
                        content.style.display = 'none';
                    } else {
                        content.style.display = 'block';
                    }
                }
            }
            
            // Initially hide all content sections
            var contents = document.getElementsByClassName('content');
            for (var i = 0; i < contents.length; i++) {
                contents[i].style.display = 'none';
            }
        }
        
        // Function to toggle element details when clicking the details button
        function toggleDetails(button) {
            var detailsDiv = button.parentElement.nextElementSibling;
            if (detailsDiv.style.display === 'block') {
                detailsDiv.style.display = 'none';
                button.textContent = 'Details';
            } else {
                detailsDiv.style.display = 'block';
                button.textContent = 'Hide Details';
            }
        }
        </script>
    </body>
    </html>
    """

    # Convert non_working_elements to proper format in each result
    # This ensures we're not trying to treat lists as dictionaries anywhere
    for result in results:
        # Ensure element_results has all necessary attributes
        for element in result.get('element_results', []):
            if 'page_change_detected' not in element:
                element['page_change_detected'] = False
            if 'visual_change_detected' not in element:
                element['visual_change_detected'] = False
    
    template = Template(template_str)
    html = template.render(
        results=results,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_elements=total_elements,
        working_elements=working_elements,
        working_percentage=working_percentage,
        elements_by_type=elements_by_type,
        pages_stats=pages_stats
    )

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report saved to {out_file}")
    print(f"Total elements tested: {total_elements}")
    print(f"Working elements: {working_elements} ({working_percentage:.1f}%)")
    print("Elements by type:")
    for element_type, stats in elements_by_type.items():
        success_rate = (stats['working'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"  {element_type}: {stats['working']}/{stats['total']} working ({success_rate:.1f}%)")