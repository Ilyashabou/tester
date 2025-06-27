# Role-Based UI WebApp Tester

## Overview

Role-Based UI WebApp Tester is an automated testing framework designed to crawl websites, generate and execute tests for UI elements, and produce comprehensive reports on web interface functionality. The system uses a role-based approach to identify and test interactive elements without requiring AI assistance.

## Key Features

### 1. Intelligent Web Crawling
- Automated exploration of websites with configurable depth control
- Screenshot capture of each page for visual reference
- HTML extraction and cleaning for analysis
- Support for authenticated website testing

### 2. Advanced Element Detection
- Identification of 15+ types of UI elements (buttons, links, inputs, etc.)
- Role-based classification of elements using robust CSS selectors
- Intelligent element categorization based on attributes and context
- Fallback detection mechanisms for complex pages

### 3. Automated Test Generation
- Template-based test script generation for each detected element
- Python scripts using Playwright for browser automation
- Error handling and recovery mechanisms
- Automatic navigation between pages

### 4. Visual Change Detection
- Before/after screenshot comparison for interactions
- Detection of subtle visual changes
- Accurate assessment of element functionality

### 5. Comprehensive Reporting
- Detailed statistics on element testing (global and per-page)
- Identification of non-functional elements
- Success rate breakdown by element type
- Visual comparison with before/after screenshots

## Technical Architecture

### Core Technologies
- **Python**: Primary programming language
- **Playwright**: Browser automation and test execution
- **BeautifulSoup4**: HTML parsing and element extraction
- **Flask**: Web interface for test configuration and results
- **Jinja2**: Template rendering for test generation and reports
- **Pillow**: Image processing for visual comparison

### Project Structure

```
├── app.py                 # Flask web application
├── crawler.py             # Website crawling functionality
├── template_generator.py  # Test script generation
├── test_executor.py       # Test execution engine
├── element_tracker.py     # Element interaction tracking
├── reporter.py            # HTML report generation
├── session_manager.py     # Authentication session management
├── check_session.py       # Session verification utility
├── _fallback_detection.py # Alternative element detection
├── auth_sessions/         # Stored authentication sessions
├── doc/                   # Project documentation
├── generated_tests/       # Generated test scripts
│   └── screenshots/       # Test execution screenshots
└── templates/             # Flask HTML templates
```

## Process Flow

1. **Crawling Phase**:
   - Start with a base URL and crawl the website to specified depth
   - Capture screenshots and save HTML content for each page
   - Extract internal links for further crawling

2. **Test Generation Phase**:
   - Process each crawled page's HTML
   - Extract interactive elements by role
   - Generate test steps for each element
   - Create complete test scripts

3. **Test Execution Phase**:
   - Run each generated test script
   - Track element interactions and results
   - Capture before/after screenshots
   - Detect visual and navigation changes

4. **Reporting Phase**:
   - Compile test results and statistics
   - Generate comprehensive HTML report
   - Highlight problematic elements
   - Provide visual evidence of testing

## Usage

### Web Interface

The application provides a web interface for configuring and running tests:

1. Start the application: `python app.py`
2. Access the web interface at `http://localhost:5000`
3. Enter the target website URL
4. Configure testing options (visual mode, single page, authentication)
5. Start the testing process
6. View real-time progress and final report

### Authentication Support

For testing websites that require login:

1. Enable the "Requires Authentication" option
2. Provide login URL, username, and password
3. The system will attempt to log in before crawling
4. Session data is stored for subsequent test runs

### Visual Mode

Enable visual mode to see the browser in action during testing:

- Tests run with visible browser windows
- Interactions are slowed down for better visibility
- Useful for debugging and demonstration purposes

## Evolution from AI-Based Approach

The project initially aimed to use AI models to generate test scripts but evolved to a template-based approach due to several limitations:

- **Token Limits**: AI models couldn't process complete web pages
- **Performance**: AI generation was extremely slow
- **Cost**: API usage for large-scale testing was prohibitively expensive
- **Quality**: Generated tests often required significant manual revision

The current role-based approach offers:
- **Speed**: Much faster test generation
- **Independence**: No reliance on external services
- **Control**: Complete control over test logic
- **Consistency**: Standardized tests following established patterns
- **Scalability**: Easy addition of new element types or behaviors

## Future Enhancements

- **Parallel Execution**: Run multiple tests simultaneously
- **Machine Learning**: Improve element detection through learning
- **CI/CD Integration**: Automate testing in development pipelines
- **Mobile Testing**: Extend to test mobile interfaces
- **API Testing**: Add support for testing backend APIs