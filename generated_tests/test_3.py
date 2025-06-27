
# Playwright test for https://thinking-tester-contact-list.herokuapp.com/addUser
# Generated using role-based template approach
# HTML file: html_files\https___thinking_tester_contact_list_herokuapp_com_addUser.html
# Note: This test runs in headless mode by default. 
# A visual mode version (with headless=False) will be created as test_X_visual.py when visual mode is enabled.

from playwright.sync_api import sync_playwright
import os
import sys
import time
import traceback
import json
from datetime import datetime

# Add parent directory to path to import ElementTracker and SessionManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from element_tracker import ElementTracker
from session_manager import session_manager

def create_screenshot_dir():
    """Create screenshots directory if it doesn't exist"""
    screenshots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    return screenshots_dir

def take_screenshot(page, name):
    """Take a screenshot and save it with timestamp"""
    screenshots_dir = create_screenshot_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)
    page.screenshot(path=filepath)
    print(f"Screenshot saved: {filepath}")
    return filepath

def detect_page_change(before_url, after_url, before_title, after_title):
    """Detect if the page has changed after an interaction"""
    url_changed = before_url != after_url
    title_changed = before_title != after_title
    return url_changed or title_changed

def detect_visual_change(before_screenshot, after_screenshot, threshold=0.05):
    """Detect if there are visual changes between two screenshots
    
    Args:
        before_screenshot: Path to the screenshot before interaction
        after_screenshot: Path to the screenshot after interaction
        threshold: Difference threshold (0.0-1.0) to consider as a change
        
    Returns:
        bool: True if visual changes detected, False otherwise
    """
    try:
        from PIL import Image, ImageChops, ImageStat
        import math
        import os
        
        # Check if both screenshots exist
        if not (os.path.exists(before_screenshot) and os.path.exists(after_screenshot)):
            return False
            
        # Open images
        before_img = Image.open(before_screenshot)
        after_img = Image.open(after_screenshot)
        
        # Ensure both images are the same size
        if before_img.size != after_img.size:
            # Resize to match
            after_img = after_img.resize(before_img.size)
        
        # Calculate difference
        diff = ImageChops.difference(before_img, after_img)
        
        # Calculate the difference percentage
        stat = ImageStat.Stat(diff)
        diff_ratio = sum(stat.mean) / (3 * 255)  # Normalize to 0-1 range
        
        # Return True if the difference is above the threshold
        return diff_ratio > threshold
    except Exception as visual_error:
        print(f"Error detecting visual changes: {visual_error}")
        return None  # Return None to indicate error

def test_page():
    """
    Role-based test for https://thinking-tester-contact-list.herokuapp.com/addUser
    This test interacts with UI elements based on their roles.
    """
    # Create element tracker to record test results
    element_tracker = ElementTracker(output_dir="test_results")

    with sync_playwright() as p:
        browser = None
        try:
            print(f"Starting test for https://thinking-tester-contact-list.herokuapp.com/addUser")

            # Launch browser
            browser = p.chromium.launch(headless=True, args=[
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--allow-running-insecure-content',
                '--disable-webgl-image-chromium',
                '--ignore-certificate-errors',
                '--disable-notifications',
                '--disable-popup-blocking',
                '--no-sandbox',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-dev-shm-usage'
            ])
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            
            # Try to load the authenticated session
            print("Attempting to load authenticated session...")
            session_loaded = session_manager.load_session(context, "https://thinking-tester-contact-list.herokuapp.com/addUser")
            if session_loaded:
                print("Successfully loaded authenticated session")
            else:
                print("No authenticated session found or failed to load session")
                
            page = context.new_page()

            # Set a longer default timeout to prevent timeout issues
            page.set_default_timeout(30000)

            # Store the original URL for navigation back after clicks
            original_url = "https://thinking-tester-contact-list.herokuapp.com/addUser"

            # Navigate to the URL with improved error handling
            print(f"Navigating to https://thinking-tester-contact-list.herokuapp.com/addUser")
            try:
                page.goto("https://thinking-tester-contact-list.herokuapp.com/addUser", timeout=30000, wait_until="networkidle")
                
                # Apply localStorage and sessionStorage if session was loaded
                if session_loaded:
                    session_manager.apply_storage(page)
                    print("Applied localStorage and sessionStorage from saved session")
                
                # Take initial screenshot
                initial_screenshot = take_screenshot(page, "initial_page")
            except Exception as nav_error:
                print(f"Error navigating to {url}: {str(nav_error)}")
                # Record the error in the element tracker
                element_tracker.record_element_test(
                    page_url="https://thinking-tester-contact-list.herokuapp.com/addUser",
                    element_type="page",
                    selector="N/A",
                    description="Initial page navigation",
                    success=False,
                    is_working=False,
                    error_message="{str(nav_error)}",
                    screenshot_before=None,
                    screenshot_after=None,
                    page_change_detected=False,
                    visual_change_detected=False
                )
                # Save results and exit gracefully
                element_tracker.save_results()
                return

            # Basic assertions with error handling
            try:
                title = page.title()
                print(f"Page title: {title}")
                assert title != "", "Page title should not be empty"
            except Exception as title_error:
                print(f"Error getting page title: {str(title_error)}")
                # Record the error in the element tracker
                element_tracker.record_element_test(
                    page_url="https://thinking-tester-contact-list.herokuapp.com/addUser",
                    element_type="page",
                    selector="N/A",
                    description="Page title verification",
                    success=False,
                    is_working=False,
                    error_message="{str(title_error)}",
                    screenshot_before=None,
                    screenshot_after=None,
                    page_change_detected=False,
                    visual_change_detected=False
                )
                # Continue with the test despite the error

            # Execute test steps for each element type
            
                        # Testing form with selector #add-user
            
# Testing input elements
            try:
                print(f'Testing input: First Name')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'input_5_before')
                # Perform the action
                page.locator('#firstName').fill("test value")
                # Wait a moment for any visual changes to complete
                page.wait_for_timeout(500)  # 500ms wait
                # Take screenshot after interaction
                after_screenshot = take_screenshot(page, 'input_11_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with input: First Name')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='input',
                    selector='#firstName',
                    description='First Name',
                    success=True,  # We got this far without exception
                    visual_change_detected=visual_changed,
                    screenshot_before=before_screenshot,
                    screenshot_after=after_screenshot
                )
            except Exception as e:
                print(f'Error interacting with input element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='input',
                    selector='#firstName',
                    description='First Name',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
            try:
                print(f'Testing input: Last Name')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'input_42_before')
                # Perform the action
                page.locator('#lastName').fill("test value")
                # Wait a moment for any visual changes to complete
                page.wait_for_timeout(500)  # 500ms wait
                # Take screenshot after interaction
                after_screenshot = take_screenshot(page, 'input_48_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with input: Last Name')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='input',
                    selector='#lastName',
                    description='Last Name',
                    success=True,  # We got this far without exception
                    visual_change_detected=visual_changed,
                    screenshot_before=before_screenshot,
                    screenshot_after=after_screenshot
                )
            except Exception as e:
                print(f'Error interacting with input element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='input',
                    selector='#lastName',
                    description='Last Name',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
            try:
                print(f'Testing input: Email')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'input_79_before')
                # Perform the action
                page.locator('#email').fill("test value")
                # Wait a moment for any visual changes to complete
                page.wait_for_timeout(500)  # 500ms wait
                # Take screenshot after interaction
                after_screenshot = take_screenshot(page, 'input_85_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with input: Email')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='input',
                    selector='#email',
                    description='Email',
                    success=True,  # We got this far without exception
                    visual_change_detected=visual_changed,
                    screenshot_before=before_screenshot,
                    screenshot_after=after_screenshot
                )
            except Exception as e:
                print(f'Error interacting with input element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='input',
                    selector='#email',
                    description='Email',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
            try:
                print(f'Testing input: Password')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'input_116_before')
                # Perform the action
                page.locator('#password').fill("test value")
                # Wait a moment for any visual changes to complete
                page.wait_for_timeout(500)  # 500ms wait
                # Take screenshot after interaction
                after_screenshot = take_screenshot(page, 'input_122_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with input: Password')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='input',
                    selector='#password',
                    description='Password',
                    success=True,  # We got this far without exception
                    visual_change_detected=visual_changed,
                    screenshot_before=before_screenshot,
                    screenshot_after=after_screenshot
                )
            except Exception as e:
                print(f'Error interacting with input element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='input',
                    selector='#password',
                    description='Password',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
            
# Testing button elements
            try:
                print(f'Testing button: Submit')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_154_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator('#submit').click(timeout=3000)
                try:
                    page.wait_for_load_state('networkidle', timeout=5000)
                except Exception as e:
                    print(f'Navigation wait error: {{e}}')
                page.goto(original_url, timeout=5000)
                try:
                    page.wait_for_load_state('networkidle', timeout=5000)
                except Exception as e:
                    print(f'Return navigation wait error: {{e}}')
                # Wait a moment for any visual changes to complete
                page.wait_for_timeout(500)  # 500ms wait
                # Check if the page changed (URL or title)
                after_url = page.url
                after_title = page.title()
                page_changed = after_url != before_url or after_title != before_title
                # Take screenshot after interaction
                after_screenshot = take_screenshot(page, 'button_167_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: Submit')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='#submit',
                    description='Submit',
                    success=True,  # We got this far without exception
                    screenshot_before=before_screenshot,
                    screenshot_after=after_screenshot,
                    page_change_detected=page_changed,
                    visual_change_detected=visual_changed
                )
                # Go back to original URL if page changed
                if page_changed:
                    print(f"Page changed after interaction! New URL: {after_url}")
                    page.goto(original_url, timeout=5000)
                    try:
                        page.wait_for_load_state('networkidle', timeout=5000)
                    except Exception as e:
                        print(f'Return navigation wait error: {e}')
            except Exception as e:
                print(f'Error interacting with button element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='#submit',
                    description='Submit',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
            try:
                print(f'Testing button: Cancel')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_207_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator('#cancel').click(timeout=3000)
                try:
                    page.wait_for_load_state('networkidle', timeout=5000)
                except Exception as e:
                    print(f'Navigation wait error: {{e}}')
                page.goto(original_url, timeout=5000)
                try:
                    page.wait_for_load_state('networkidle', timeout=5000)
                except Exception as e:
                    print(f'Return navigation wait error: {{e}}')
                # Wait a moment for any visual changes to complete
                page.wait_for_timeout(500)  # 500ms wait
                # Check if the page changed (URL or title)
                after_url = page.url
                after_title = page.title()
                page_changed = after_url != before_url or after_title != before_title
                # Take screenshot after interaction
                after_screenshot = take_screenshot(page, 'button_220_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: Cancel')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='#cancel',
                    description='Cancel',
                    success=True,  # We got this far without exception
                    screenshot_before=before_screenshot,
                    screenshot_after=after_screenshot,
                    page_change_detected=page_changed,
                    visual_change_detected=visual_changed
                )
                # Go back to original URL if page changed
                if page_changed:
                    print(f"Page changed after interaction! New URL: {after_url}")
                    page.goto(original_url, timeout=5000)
                    try:
                        page.wait_for_load_state('networkidle', timeout=5000)
                    except Exception as e:
                        print(f'Return navigation wait error: {e}')
            except Exception as e:
                print(f'Error interacting with button element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='#cancel',
                    description='Cancel',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements

            print("Test completed successfully")

        except Exception as e:
            print(f"Test failed: {e}")
            traceback.print_exc()
            if 'page' in locals():
                take_screenshot(page, "error_state")
            raise
        finally:
            if browser:
                browser.close()

            # Save element tracking results
            results_path = element_tracker.save_results()
            print(f"Element tracking results saved to: {results_path}")

            # Print summary
            summary = element_tracker.get_summary()
            print(f"\nElement Testing Summary:")
            print(f"Total elements tested: {summary['total']}")
            print(f"Successfully interacted: {summary['successful']} ({summary['successful']/max(1, summary['total'])*100:.1f}%)")
            print(f"Working elements: {summary['working']} ({summary['working']/max(1, summary['total'])*100:.1f}%)")
            print("\nBy element type:")
            for element_type, stats in summary['by_type'].items():
                print(f"  {element_type}: {stats['working']}/{stats['total']} working ({stats['working']/max(1, stats['total'])*100:.1f}%)")

if __name__ == "__main__":
    test_page()
