import os
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, send_file
from crawler import crawl_website_and_screenshot
from template_generator import generate_tests_with_templates
from test_executor import execute_tests
from reporter import generate_report

# Configure Flask to ignore changes in the generated_tests directory
class CustomFlask(Flask):
    def _get_file_autowatch_paths(self, extra_files):
        paths = super()._get_file_autowatch_paths(extra_files)
        # Filter out paths in the generated_tests directory
        return [p for p in paths if 'generated_tests' not in str(p)]

app = CustomFlask(__name__)

# Global variables to track testing state
current_test = {
    "status": "idle",  # idle, crawling, generating, executing, reporting, done
    "url": None,
    "visual_mode": False,
    "single_page_mode": False,
    "requires_auth": False,
    "auth_params": None,
    "login_status": None,
    "login_screenshot": None,
    "progress": 0,
    "message": "",
    "pages": [],
    "test_scripts": [],
    "results": None,
    "report_path": None,
    "error": None,
    "process_details": [],
    "start_time": None,
    "end_time": None,
    "summary": {}
}

def reset_test_state():
    current_test["status"] = "idle"
    current_test["url"] = None
    current_test["visual_mode"] = False
    current_test["single_page_mode"] = False
    current_test["requires_auth"] = False
    current_test["auth_params"] = None
    current_test["login_status"] = None
    current_test["login_screenshot"] = None
    current_test["progress"] = 0
    current_test["message"] = ""
    current_test["pages"] = []
    current_test["test_scripts"] = []
    current_test["results"] = None
    current_test["report_path"] = None
    current_test["error"] = None
    current_test["process_details"] = []
    current_test["start_time"] = None
    current_test["end_time"] = None
    current_test["summary"] = {}

def add_process_detail(message, status=None):
    """Add a detailed process message to the current test state"""
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    detail = {
        "time": timestamp,
        "message": message
    }
    if status:
        current_test["status"] = status
    current_test["process_details"].append(detail)
    current_test["message"] = message

def run_test_process(url, visual_mode, single_page_mode, requires_auth=False, auth_params=None):
    try:
        # Initialize test start time
        current_test["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # Step 1: Crawling
        current_test["status"] = "crawling"
        add_process_detail(f"Starting to crawl {url}...", "crawling")
        current_test["progress"] = 10
        
        # Crawling substeps
        add_process_detail(f"Initializing browser for crawling...")
        current_test["progress"] = 15
        
        # If authentication is required, display message
        if requires_auth and auth_params:
            add_process_detail(f"Authentication required. Will attempt to log in at {auth_params['login_url']}")
            
            # Add a placeholder for login status that will be updated after crawling
            current_test["login_status"] = "pending"
        
        # If in single page mode, display different message
        if single_page_mode:
            add_process_detail(f"Single page mode: Testing only {url} without crawling links")
        
        # Call the crawler with authentication if required
        if requires_auth and auth_params:
            pages, login_result = crawl_website_and_screenshot(url, single_page_mode=single_page_mode, requires_auth=requires_auth, auth_params=auth_params)
            current_test["pages"] = pages
            
            # Update login status and add a message about login result
            current_test["login_status"] = "success" if login_result["success"] else "failed"
            current_test["login_screenshot"] = login_result["screenshot"]
            
            # Add a process detail about the login result
            if login_result["success"]:
                add_process_detail(f"✅ {login_result['message']}")
            else:
                add_process_detail(f"❌ {login_result['message']}")
        else:
            pages = crawl_website_and_screenshot(url, single_page_mode=single_page_mode, requires_auth=requires_auth, auth_params=auth_params)
            current_test["pages"] = pages
        
        add_process_detail(f"Crawled {len(pages)} pages and captured screenshots")
        current_test["progress"] = 25
        
        # Step 2: Generating tests
        add_process_detail("Starting test generation with role-based templates...", "generating")
        current_test["progress"] = 30
        
        # Test generation substeps
        add_process_detail(f"Analyzing HTML structure of {len(pages)} pages...")
        current_test["progress"] = 35
        
        test_scripts = generate_tests_with_templates(pages)
        current_test["test_scripts"] = test_scripts
        add_process_detail(f"Generated {len(test_scripts)} test scripts")
        current_test["progress"] = 45
        
        # Update the test execution section to better handle visual mode
        add_process_detail(f"Starting test execution{' in visual mode' if visual_mode else ''}...", "executing")
        current_test["progress"] = 50
        
        # Test execution substeps
        add_process_detail(f"Setting up browser for test execution...")
        current_test["progress"] = 55
        
        if visual_mode:
            add_process_detail(f"Visual mode enabled - browser will be visible during test execution")
            add_process_detail(f"Note: Visual mode tests will create *_visual.py files that can be run manually")
        
        results = execute_tests(test_scripts, visual_mode=visual_mode)
        current_test["results"] = results
        
        # Extract some summary information from results
        if results:
            # Check if results is an object with get_summary method
            if hasattr(results, 'get_summary'):
                summary = results.get_summary()
                current_test["summary"] = summary
                add_process_detail(f"Executed tests with {summary.get('success_rate', 0)}% success rate")
            else:
                # If results is a list (as expected), count success rate manually
                successful_tests = sum(1 for r in results if r.get('success', False))
                total_tests = len(results)
                success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
                current_test["summary"] = {
                    'success_rate': success_rate,
                    'total_tests': total_tests,
                    'successful_tests': successful_tests
                }
                add_process_detail(f"Executed {successful_tests}/{total_tests} tests successfully ({success_rate:.1f}% success rate)")
        else:
            add_process_detail(f"No test results were returned")
        
        current_test["progress"] = 70
        
        # Step 4: Generating report
        add_process_detail("Generating comprehensive HTML report...", "reporting")
        current_test["progress"] = 80
        
        # Report generation substeps
        add_process_detail("Processing test results and screenshots...")
        current_test["progress"] = 85
        
        generate_report(results)
        current_test["report_path"] = "report.html"
        add_process_detail("HTML report generated successfully")
        current_test["progress"] = 95
        
        # Step 5: Done
        current_test["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        add_process_detail("Testing process completed successfully!", "done")
        current_test["progress"] = 100
    except Exception as e:
        current_test["status"] = "error"
        current_test["error"] = str(e)
        error_message = f"Error: {str(e)}"
        add_process_detail(error_message, "error")
        current_test["progress"] = 0
        current_test["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_test', methods=['POST'])
def start_test():
    if current_test["status"] not in ["idle", "done", "error"]:
        return jsonify({"success": False, "message": "A test is already running"})
    
    url = request.form.get('url')
    visual_mode = request.form.get('visual_mode') == 'true'
    single_page_mode = request.form.get('single_page_mode') == 'true'
    requires_auth = request.form.get('requires_auth') == 'true'
    
    # Authentication parameters
    auth_params = None
    if requires_auth:
        login_url = request.form.get('login_url')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not login_url or not username or not password:
            return jsonify({"success": False, "message": "Login URL, username, and password are required for authentication"})
        
        auth_params = {
            'login_url': login_url,
            'username': username,
            'password': password
        }
    
    if not url:
        return jsonify({"success": False, "message": "URL is required"})
    
    # Reset the test state
    reset_test_state()
    
    # Update the test state
    current_test["status"] = "starting"
    current_test["url"] = url
    current_test["visual_mode"] = visual_mode
    current_test["single_page_mode"] = single_page_mode
    current_test["requires_auth"] = requires_auth
    current_test["auth_params"] = auth_params
    current_test["message"] = "Starting test..."
    
    # Start the test process in a separate thread
    thread = threading.Thread(target=run_test_process, args=(url, visual_mode, single_page_mode, requires_auth, auth_params))
    thread.daemon = True
    thread.start()
    
    return jsonify({"success": True})

@app.route('/status')
def status():
    return jsonify(current_test)

@app.route('/report')
def report():
    if current_test["status"] == "done" and current_test["report_path"]:
        return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 
                                  os.path.basename(current_test["report_path"]))
    return redirect(url_for('index'))

@app.route('/download_report')
def download_report():
    if current_test["status"] == "done" and current_test["report_path"]:
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  os.path.basename(current_test["report_path"]))
        return send_file(report_path, as_attachment=True, 
                        download_name=f"test_report_{time.strftime('%Y%m%d_%H%M%S')}.html")
    return redirect(url_for('index'))

@app.route('/screenshots/<path:filename>')
def screenshot(filename):
    return send_from_directory('screenshots', filename)

@app.route('/test_results/<path:filename>')
def test_result(filename):
    return send_from_directory('test_results', filename)

@app.route('/cancel_test', methods=['POST'])
def cancel_test():
    if current_test["status"] not in ["idle", "done", "error"]:
        reset_test_state()
        current_test["message"] = "Test cancelled by user"
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "No test is running"})

if __name__ == '__main__':
    # Set use_reloader=False to prevent Flask from restarting when test files are generated
    app.run(debug=True, host='0.0.0.0', port=4000, use_reloader=False)
