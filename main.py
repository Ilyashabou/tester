import sys
from crawler import crawl_website_and_screenshot
from template_generator import generate_tests_with_templates
from test_executor import execute_tests
from reporter import generate_report

def main(base_url, visual_mode=False):
    print(f"[1/5] Crawling and screenshotting {base_url}...")
    pages = crawl_website_and_screenshot(base_url)
    print(f"[2/5] Generating tests with role-based templates...")
    test_scripts = generate_tests_with_templates(pages)
    print(f"[3/5] Executing tests{' in visual mode' if visual_mode else ''}...")
    results = execute_tests(test_scripts, visual_mode=visual_mode)
    print(f"[4/5] Generating report...")
    generate_report(results)
    print(f"[5/5] Done! Report generated.")

if __name__ == "__main__":
    # Check for visual mode flag
    visual_mode = False
    base_url = None
    
    for arg in sys.argv[1:]:
        if arg == "--visual" or arg == "-v":
            visual_mode = True
        elif not base_url:  # First non-flag argument is the URL
            base_url = arg
    
    if not base_url:
        print("Usage: python main.py <base_url> [--visual|-v]")
        print("  --visual or -v: Run tests in visual mode (browser will be visible)")
        sys.exit(1)
        
    main(base_url, visual_mode)