# FocusManager: Detailed Function Documentation

This document provides a detailed description of each file in the project and the functions they contain.

## 1. main.py

The main entry point of the application that orchestrates the entire testing process.

### Functions:

#### `main(base_url, visual_mode=False)`
- **Purpose**: Coordinates the entire testing workflow
- **Parameters**:
  - `base_url`: The starting URL for website testing
  - `visual_mode`: Boolean flag to run tests with visible browser
- **Process**:
  1. Calls `crawl_website_and_screenshot()` to crawl the website
  2. Calls `generate_tests_with_templates()` to create test scripts
  3. Calls `execute_tests()` to run the tests
  4. Calls `generate_report()` to create the final report
- **Returns**: None

## 2. crawler.py

Handles website crawling and screenshot capture.

### Functions:

#### `is_internal_link(base_url, link)`
- **Purpose**: Determines if a link belongs to the same domain as the base URL
- **Parameters**:
  - `base_url`: The starting URL of the crawl
  - `link`: The link to check
- **Returns**: Boolean indicating if the link is internal

#### `normalize_url(url)`
- **Purpose**: Standardizes URLs for comparison
- **Parameters**:
  - `url`: The URL to normalize
- **Process**:
  1. Removes fragments and query parameters
  2. Removes trailing slashes
- **Returns**: Normalized URL string

#### `make_safe_filename(url, max_length=150)`
- **Purpose**: Converts URLs to valid filenames
- **Parameters**:
  - `url`: The URL to convert
  - `max_length`: Maximum length for the filename
- **Process**: Replaces invalid characters with underscores
- **Returns**: Safe filename string

#### `sanitize_filename(url)`
- **Purpose**: Convert URL to a valid filename
- **Parameters**:
  - `url`: The URL to convert
- **Process**:
  1. Removes protocol and domain
  2. Replaces invalid characters
  3. Limits length to 100 characters
- **Returns**: Sanitized filename string

#### `crawl_website_and_screenshot(base_url, out_dir="screenshots", max_depth=3, throttle_seconds=1)`
- **Purpose**: Crawls a website, captures screenshots, and saves HTML content
- **Parameters**:
  - `base_url`: The starting URL for crawling
  - `out_dir`: Directory to save screenshots
  - `max_depth`: Maximum crawl depth
  - `throttle_seconds`: Delay between requests
- **Process**:
  1. Creates output directories
  2. Initializes tracking variables
  3. Launches Playwright browser
  4. For each URL to visit:
     - Navigates to the URL
     - Takes a screenshot
     - Saves the HTML
     - Extracts internal links
     - Adds new links to the queue
  5. Implements retry logic for failed requests
- **Returns**: List of dictionaries with page information

## 3. template_generator.py

Generates test scripts based on element roles.

### Classes:

#### `RoleBasedTestGenerator`

##### Constructor `__init__(self)`
- **Purpose**: Initializes the generator with role selectors and action templates
- **Fields**:
  - `self.role_selectors`: Maps element roles to CSS selectors and actions
  - `self.step_templates`: Templates for different test actions

##### Methods:

###### `optimize_html(self, html)`
- **Purpose**: Removes unnecessary elements from HTML
- **Parameters**:
  - `html`: Raw HTML content
- **Process**:
  1. Parses HTML with BeautifulSoup
  2. Removes script tags
  3. Removes style tags
  4. Removes comments
  5. Removes meta tags
  6. Removes link tags
  7. Removes SVG elements
- **Returns**: Optimized BeautifulSoup object

###### `extract_elements_by_role(self, soup)`
- **Purpose**: Identifies all interactive elements in the HTML
- **Parameters**:
  - `soup`: BeautifulSoup object of the page
- **Process**:
  1. First pass: Extracts buttons and inputs directly by tag
  2. Second pass: Extracts elements by role using selectors
  3. Third pass: Finds additional interactive elements
- **Returns**: Dictionary of elements grouped by role

###### `_get_element_unique_id(self, element)`
- **Purpose**: Creates a unique identifier for an element
- **Parameters**:
  - `element`: BeautifulSoup element
- **Returns**: String identifier

###### `_create_selector_for_element(self, element_info)`
- **Purpose**: Creates a robust CSS selector for an element
- **Parameters**:
  - `element_info`: Dictionary with element attributes
- **Process**:
  1. Tries ID-based selector (highest priority)
  2. Tries test-specific attributes (data-testid, data-cy)
  3. Tries aria attributes
  4. Tries name, placeholder, or role attributes
  5. Tries text content for links and buttons
  6. Creates position-based selectors as fallback
- **Returns**: CSS selector string

###### `generate_test_steps(self, elements_by_role)`
- **Purpose**: Generates test steps for elements
- **Parameters**:
  - `elements_by_role`: Dictionary of elements grouped by role
- **Process**:
  1. For each role and its elements:
     - Gets the appropriate action template
     - Creates a test step with the element's selector
- **Returns**: List of test step strings

###### `generate_test_script(self, url, html, html_file=None)`
- **Purpose**: Creates a complete test script
- **Parameters**:
  - `url`: Target URL for testing
  - `html`: HTML content of the page
  - `html_file`: Path to saved HTML file
- **Process**:
  1. Optimizes the HTML
  2. Extracts elements by role
  3. Generates test steps
  4. Creates a complete Playwright script with:
     - Imports
     - Test function
     - Browser setup
     - Navigation
     - Element interaction steps
     - Result tracking
     - Browser cleanup
- **Returns**: Path to the generated test script

###### `_fallback_element_detection(self, soup)`
- **Purpose**: Alternative detection for pages with few elements
- **Parameters**:
  - `soup`: BeautifulSoup object of the page
- **Process**:
  1. Finds elements with onclick attributes
  2. Finds elements with interactive class names
  3. Finds elements with tabindex
  4. Finds elements with hover effects
- **Returns**: Dictionary of additional elements

#### `generate_tests_with_templates(pages, out_dir="generated_tests")`
- **Purpose**: Generates tests for a list of pages
- **Parameters**:
  - `pages`: List of page dictionaries from crawler
  - `out_dir`: Directory to save generated tests
- **Process**:
  1. Creates the output directory
  2. Initializes the test generator
  3. For each page:
     - Generates a test script
     - Saves the script to the output directory
- **Returns**: List of paths to generated test scripts

## 4. test_executor.py

Executes the generated test scripts.

### Functions:

#### `execute_tests(test_scripts, out_dir="test_results", visual_mode=False)`
- **Purpose**: Runs generated test scripts
- **Parameters**:
  - `test_scripts`: List of paths to test scripts
  - `out_dir`: Directory to save results
  - `visual_mode`: Boolean flag to run with visible browser
- **Process**:
  1. Creates the output directory
  2. For each test script:
     - In visual mode:
       - Modifies the script to run with headless=False
       - Adds delays for visibility
       - Runs the modified script
     - In headless mode:
       - Runs the script using subprocess
     - Collects results and element tracking data
- **Returns**: List of dictionaries with test results

#### `get_url_from_script(script_path)`
- **Purpose**: Extracts the target URL from a test script
- **Parameters**:
  - `script_path`: Path to the test script
- **Process**: Searches for the "original_url =" line in the script
- **Returns**: URL string or "Unknown URL"

## 5. reporter.py

Generates HTML reports from test results.

### Functions:

#### `generate_report(results, out_file="report.html")`
- **Purpose**: Creates an HTML report with test results
- **Parameters**:
  - `results`: List of test result dictionaries
  - `out_file`: Output file path
- **Process**:
  1. Calculates statistics:
     - Total elements tested
     - Working elements count
     - Elements by type
  2. Creates an HTML report using Jinja2 template with:
     - Summary statistics
     - Element type breakdown
     - Page-by-page results
     - Screenshots
     - Test output logs
  3. Saves the report to the output file
  4. Prints summary statistics
- **Returns**: None

## 6. element_tracker.py

Tracks element interactions and test results.

### Classes:

#### `ElementTracker`

##### Constructor `__init__(self, output_dir="test_results")`
- **Purpose**: Initializes the tracker
- **Parameters**:
  - `output_dir`: Directory to save results
- **Fields**:
  - `self.output_dir`: Output directory
  - `self.elements`: List to store element results
  - `self.test_id`: Unique ID for the test run

##### Methods:

###### `record_element_test(self, page_url, element_type, selector, description="", success=False, error_message=None, screenshot_before=None, screenshot_after=None, page_change_detected=False, visual_change_detected=None)`
- **Purpose**: Records the result of testing an element
- **Parameters**:
  - `page_url`: URL of the page
  - `element_type`: Type of element
  - `selector`: CSS selector
  - `description`: Text description
  - `success`: Whether interaction succeeded
  - `error_message`: Error message if failed
  - `screenshot_before`: Path to before screenshot
  - `screenshot_after`: Path to after screenshot
  - `page_change_detected`: Whether page changed
  - `visual_change_detected`: Whether visual changes detected
- **Process**:
  1. Determines if the element is "working" based on:
     - Element type
     - Success of interaction
     - Expected behavior
  2. Creates a result dictionary
  3. Adds the result to the elements list
- **Returns**: None

###### `save_results(self)`
- **Purpose**: Saves element tracking results to JSON
- **Process**:
  1. Creates a JSON structure with:
     - Test ID
     - Timestamp
     - Element results
  2. Writes to a file in the output directory
- **Returns**: Path to the output file

###### `get_summary(self)`
- **Purpose**: Generates summary statistics
- **Process**:
  1. Counts total elements
  2. Counts successful interactions
  3. Counts working elements
  4. Breaks down statistics by element type
- **Returns**: Dictionary with summary statistics

## 7. _fallback_detection.py

Provides fallback methods for element detection.

### Functions:

#### `_fallback_element_detection(self, soup)`
- **Purpose**: More aggressive element detection for complex pages
- **Parameters**:
  - `soup`: BeautifulSoup object of the page
- **Process**:
  1. Finds elements with onclick attributes
  2. Finds elements with interactive class names
  3. Finds elements with tabindex
  4. Finds elements with hover effects
- **Returns**: Dictionary of additional elements
