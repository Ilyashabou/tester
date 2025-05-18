# FocusManager: Comprehensive Project Documentation

## 1. Project Overview

FocusManager is an automated web testing framework that crawls websites, generates tests for UI elements, executes those tests, and produces comprehensive reports on the functionality of web interfaces. The system uses a role-based approach to identify and test interactive elements without requiring AI assistance.

## 2. Technologies Used

### Core Technologies
- **Python**: The primary programming language used throughout the project
- **Playwright**: Used for browser automation, web crawling, and test execution
- **BeautifulSoup4**: HTML parsing and element extraction
- **Jinja2**: Template rendering for test generation and report creation
- **Pillow**: Image processing for screenshots and visual comparison

### Additional Libraries
- **Requests**: HTTP requests for web interactions
- **urllib.parse**: URL parsing and manipulation

## 3. Project Structure

### Main Files
- **main.py**: Entry point of the application that orchestrates the entire testing process
- **crawler.py**: Handles website crawling and screenshot capture
- **template_generator.py**: Generates test scripts based on element roles
- **test_executor.py**: Executes the generated test scripts
- **reporter.py**: Generates HTML reports from test results
- **element_tracker.py**: Tracks element interactions and test results
- **_fallback_detection.py**: Provides fallback methods for element detection

### Directories
- **screenshots/**: Stores screenshots of crawled pages
- **html_files/**: Stores HTML content of crawled pages
- **generated_tests/**: Contains generated Playwright test scripts
- **test_results/**: Stores test execution results and reports

## 4. Key Functions and Classes

### Crawler Module
- **crawl_website_and_screenshot()**: Crawls a website, captures screenshots, and saves HTML content
- **normalize_url()**: Standardizes URLs for comparison
- **is_internal_link()**: Determines if a link belongs to the same domain
- **make_safe_filename()**: Converts URLs to valid filenames

### Template Generator Module
- **RoleBasedTestGenerator**: Main class for test generation
  - **role_selectors**: Maps UI element roles to CSS selectors and actions
  - **step_templates**: Templates for different test actions
  - **optimize_html()**: Removes unnecessary elements from HTML
  - **extract_elements_by_role()**: Identifies interactive elements by role
  - **_create_selector_for_element()**: Creates robust CSS selectors
  - **generate_test_steps()**: Generates test steps for elements
  - **generate_test_script()**: Creates complete test scripts
  - **_fallback_element_detection()**: Alternative detection for complex pages

### Test Executor Module
- **execute_tests()**: Runs generated test scripts
- **get_url_from_script()**: Extracts target URL from test scripts

### Reporter Module
- **generate_report()**: Creates HTML reports with test results and statistics

### Element Tracker Module
- **ElementTracker**: Tracks element testing results
  - **record_element_test()**: Records test results for elements
  - **save_results()**: Saves results to JSON
  - **get_summary()**: Generates summary statistics

## 5. Process Flow

### 1. Crawling Phase
- The process begins with `crawl_website_and_screenshot()` from the crawler module
- The function takes a base URL and crawls the website to a specified depth
- For each page:
  - A screenshot is captured and saved
  - HTML content is saved
  - Internal links are extracted for further crawling
  - Page information is stored for test generation

### 2. Test Generation Phase
- `generate_tests_with_templates()` processes each crawled page
- For each page:
  - HTML is optimized using `optimize_html()`
  - Elements are extracted by role using `extract_elements_by_role()`
  - If few elements are found, `_fallback_element_detection()` is used
  - Test steps are generated for each element using `generate_test_steps()`
  - A complete test script is created with `generate_test_script()`
  - The script is saved to the generated_tests directory

### 3. Test Execution Phase
- `execute_tests()` runs each generated test script
- Tests can be run in headless mode (default) or visual mode
- For visual mode, scripts are modified to run with visible browser and delays
- Element interactions are tracked using the ElementTracker class
- Results are collected for reporting

### 4. Reporting Phase
- `generate_report()` creates an HTML report with:
  - Overall statistics on element testing
  - Breakdown by element type
  - Detailed results for each page
  - Screenshots before and after interactions
  - Test output logs

## 6. Running the Project

### Command Line Usage
```
python main.py <base_url> [--visual|-v]
```

### Parameters
- **base_url**: The starting URL for website testing
- **--visual** or **-v**: Optional flag to run tests in visual mode (browser visible)

### Example
```
python main.py https://example.com --visual
```

## 7. Test Generation Details

### Element Role Detection
The system identifies UI elements based on their roles:
- **Buttons**: Any clickable control elements
- **Links**: Navigation elements
- **Inputs**: Text fields, textareas
- **Checkboxes**: Toggle elements
- **Radio buttons**: Selection elements
- **Select boxes**: Dropdown menus
- **Tabs**: Tab navigation elements
- **Menus**: Navigation menus
- **Forms**: Data submission containers
- **Interactive elements**: Any element with event handlers

### Selector Generation
For each element, the system creates robust CSS selectors using:
1. ID attributes (highest priority)
2. Test-specific attributes (data-testid, data-cy)
3. Aria attributes for accessibility
4. Name, placeholder, or role attributes
5. Text content for links and buttons
6. Tag name with class or attributes
7. Position-based selectors as a fallback

### Test Actions
Different actions are applied based on element role:
- **click**: For buttons, links, tabs, menus
- **fill**: For text inputs, textareas
- **check**: For checkboxes, radio buttons
- **select_option**: For select/dropdown elements
- **detect**: For dialogs, alerts
- **submit**: For forms
- **slide**: For range inputs
- **toggle**: For toggle switches

## 8. Test Execution Details

### Test Script Structure
Each generated test script:
1. Imports necessary Playwright modules
2. Defines a test function
3. Sets up a browser instance
4. Navigates to the target URL
5. Executes test steps for each element
6. Takes screenshots
7. Records results
8. Closes the browser

### Visual Mode
When running in visual mode:
- Browser is visible (headless=False)
- Delays are added between actions
- User can observe the testing process
- Tests can be interrupted with Ctrl+C

### Element Testing Logic
The system determines if elements are "working" based on:
- **Links**: Expected to navigate unless they're anchor links
- **Buttons**: May navigate or trigger JS actions
- **Forms**: Expected to submit data
- **Inputs**: Expected to accept input
- **Checkboxes/Radios**: Expected to toggle state

## 9. Reporting Details

The HTML report provides:
- **Summary statistics**: Total elements tested, success rates
- **Element type breakdown**: Performance by element type
- **Page-by-page results**: Detailed test results for each page
- **Visual evidence**: Screenshots before and after interactions
- **Logs**: Test execution output
- **Interactive UI**: Collapsible sections for detailed information

## 10. Project Strengths

1. **No AI Dependency**: Uses role-based detection instead of AI
2. **Comprehensive Coverage**: Tests all types of interactive elements
3. **Robust Selectors**: Creates selectors that resist minor UI changes
4. **Visual Feedback**: Provides screenshots for verification
5. **Detailed Reporting**: Generates comprehensive test reports
6. **Fallback Mechanisms**: Uses alternative detection methods when needed
7. **Error Handling**: Robust error handling throughout the process

## 11. Limitations and Considerations

1. **JavaScript-Heavy Sites**: May have difficulty with highly dynamic content
2. **Authentication**: No built-in support for authenticated testing
3. **Complex Interactions**: Limited to basic element interactions
4. **Performance**: Comprehensive testing can be time-consuming
5. **Selector Reliability**: Some selectors may break with major UI changes
