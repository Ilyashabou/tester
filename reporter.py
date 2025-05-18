import os
import json
from datetime import datetime
from jinja2 import Template

def generate_report(results, out_file="report.html"):
    # Calculate overall statistics
    total_elements = 0
    working_elements = 0
    elements_by_type = {}

    for result in results:
        for element in result.get('element_results', []):
            element_type = element.get('element_type', 'unknown')

            # Count total elements
            total_elements += 1

            # Count working elements
            if element.get('is_working', False):
                working_elements += 1

            # Count by type
            if element_type not in elements_by_type:
                elements_by_type[element_type] = {
                    'total': 0,
                    'working': 0
                }
            elements_by_type[element_type]['total'] += 1
            if element.get('is_working', False):
                elements_by_type[element_type]['working'] += 1

    # Calculate percentages
    working_percentage = (working_elements / max(1, total_elements)) * 100

    # Create the HTML report
    template_str = """
    <html>
    <head>
        <title>UI Element Test Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1, h2, h3 { color: #333; }
            .summary { background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .success { color: green; }
            .fail { color: red; }
            .warning { color: orange; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .element-details { margin-top: 5px; font-size: 0.9em; color: #666; }
            .screenshot { max-width: 200px; border: 1px solid #ddd; margin: 5px 0; }
            .progress-bar-container { width: 100%; background-color: #e0e0e0; border-radius: 4px; }
            .progress-bar { height: 20px; background-color: #4CAF50; border-radius: 4px; text-align: center; color: white; }
            .element-row { margin-bottom: 10px; padding: 5px; border-bottom: 1px solid #eee; }
            .element-row:hover { background-color: #f5f5f5; }
            .element-type { font-weight: bold; }
            .element-selector { font-family: monospace; font-size: 0.9em; color: #666; }
            .element-description { font-style: italic; }
            .screenshots-container { display: flex; gap: 10px; }
            .screenshot-container { text-align: center; }
            .screenshot-label { font-size: 0.8em; color: #666; }
            .collapsible { cursor: pointer; padding: 10px; width: 100%; border: none; text-align: left; outline: none; }
            .active, .collapsible:hover { background-color: #f1f1f1; }
            .content { padding: 0 18px; max-height: 0; overflow: hidden; transition: max-height 0.2s ease-out; }
        </style>
    </head>
    <body>
        <h1>UI Element Test Report</h1>
        <p>Generated on {{ timestamp }}</p>

        <div class="summary">
            <h2>Summary</h2>
            <p>Total elements tested: <strong>{{ total_elements }}</strong></p>
            <p>Working elements: <strong class="{{ 'success' if working_percentage >= 70 else 'warning' if working_percentage >= 40 else 'fail' }}">
                {{ working_elements }} ({{ working_percentage|round(1) }}%)
            </strong></p>

            <h3>Elements by Type</h3>
            <table>
                <tr>
                    <th>Element Type</th>
                    <th>Total</th>
                    <th>Working</th>
                    <th>Success Rate</th>
                </tr>
                {% for type, stats in elements_by_type.items() %}
                <tr>
                    <td>{{ type }}</td>
                    <td>{{ stats.total }}</td>
                    <td>{{ stats.working }}</td>
                    <td>
                        <div class="progress-bar-container">
                            <div class="progress-bar" style="width: {{ (stats.working / stats.total * 100)|round(1) }}%">
                                {{ (stats.working / stats.total * 100)|round(1) }}%
                            </div>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <h2>Test Results</h2>
        <table>
            <tr>
                <th>URL</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
            {% for r in results %}
            <tr>
                <td>{{ r.url }}</td>
                <td class="{{ 'success' if r.success else 'fail' }}">{{ 'PASS' if r.success else 'FAIL' }}</td>
                <td>
                    <button class="collapsible">Show Details ({{ r.element_results|length }} elements)</button>
                    <div class="content">
                        <h3>Elements Tested</h3>
                        {% for element in r.element_results %}
                        <div class="element-row">
                            <div class="element-type">{{ element.element_type }}</div>
                            <div class="element-description">{{ element.description }}</div>
                            <div class="element-selector">{{ element.selector }}</div>
                            <div class="element-status {{ 'success' if element.is_working else 'fail' }}">
                                {{ 'WORKING' if element.is_working else 'NOT WORKING' }}
                                {% if element.element_type == 'link' %}
                                    {% if element.page_change_detected %}
                                        (Page changed after interaction)
                                    {% elif '#' in element.description or '#' in element.selector %}
                                        (Anchor link - no page change expected)
                                    {% else %}
                                        {% set navigation_indicators = ['login', 'sign', 'register', 'checkout', 'buy', 'purchase', 'download', 'upload', 'submit'] %}
                                        {% set should_navigate = false %}
                                        {% if element.description %}
                                            {% for indicator in navigation_indicators %}
                                                {% if indicator in element.description.lower() %}
                                                    {% set should_navigate = true %}
                                                {% endif %}
                                            {% endfor %}
                                        {% endif %}
                                        {% if should_navigate %}
                                            (Expected to navigate but didn't)
                                        {% else %}
                                            (Interaction successful)
                                        {% endif %}
                                    {% endif %}
                                {% endif %}
                                {% if element.element_type == 'button' %}
                                    {% set navigation_indicators = ['login', 'sign', 'submit', 'continue', 'next', 'previous', 'back', 'proceed', 'checkout', 'buy', 'purchase', 'register'] %}
                                    {% set should_navigate = false %}
                                    {% if element.description %}
                                        {% for indicator in navigation_indicators %}
                                            {% if indicator in element.description.lower() %}
                                                {% set should_navigate = true %}
                                            {% endif %}
                                        {% endfor %}
                                    {% endif %}
                                    {% if should_navigate %}
                                        {% if element.page_change_detected %}
                                            (Page changed after interaction)
                                        {% else %}
                                            (No page change detected)
                                        {% endif %}
                                    {% endif %}
                                {% endif %}
                                {% if element.element_type == 'form' %}
                                    {% if element.page_change_detected %}
                                        (Form submitted successfully)
                                    {% else %}
                                        (No form submission detected)
                                    {% endif %}
                                {% endif %}
                            </div>
                            {% if element.screenshot_before and element.screenshot_after %}
                            <div class="screenshots-container">
                                <div class="screenshot-container">
                                    <div class="screenshot-label">Before</div>
                                    <img src="{{ element.screenshot_before }}" class="screenshot">
                                </div>
                                <div class="screenshot-container">
                                    <div class="screenshot-label">After</div>
                                    <img src="{{ element.screenshot_after }}" class="screenshot">
                                </div>
                            </div>
                            {% endif %}
                            {% if element.error_message %}
                            <div class="error-message">Error: {{ element.error_message }}</div>
                            {% endif %}
                        </div>
                        {% endfor %}

                        <h3>Test Output</h3>
                        <pre>{{ r.output }}</pre>

                        {% if r.screenshot %}
                        <h3>Final Screenshot</h3>
                        <img src="{{ r.screenshot }}" width="400">
                        {% endif %}
                    </div>
                </td>
            </tr>
            {% endfor %}
        </table>

        <script>
        var coll = document.getElementsByClassName("collapsible");
        for (var i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        }
        </script>
    </body>
    </html>
    """

    template = Template(template_str)
    html = template.render(
        results=results,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_elements=total_elements,
        working_elements=working_elements,
        working_percentage=working_percentage,
        elements_by_type=elements_by_type
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