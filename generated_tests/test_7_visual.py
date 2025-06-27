
# Playwright test for https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793
# Generated using role-based template approach
# HTML file: html_files\https___master_d2l4isn05opwbv_amplifyapp_com_profile_0a1afd61_4de1_4925_a2c1_a46220739793.html
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
    Role-based test for https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793
    This test interacts with UI elements based on their roles.
    """
    # Create element tracker to record test results
    element_tracker = ElementTracker(output_dir="test_results")

    with sync_playwright() as p:
        browser = None
        try:
            print(f"Starting test for https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793")

            # Launch browser
            browser = p.chromium.launch(headless=False, args=[
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
            session_loaded = session_manager.load_session(context, "https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793")
            if session_loaded:
                print("Successfully loaded authenticated session")
            else:
                print("No authenticated session found or failed to load session")
                
            page = context.new_page()

            # Set a longer default timeout to prevent timeout issues
            page.set_default_timeout(30000)

            # Store the original URL for navigation back after clicks
            original_url = "https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793"

            # Navigate to the URL with improved error handling
            print(f"Navigating to https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793")
            try:
                page.goto("https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793", timeout=30000, wait_until="networkidle")
                
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
                    page_url="https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793",
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
                    page_url="https://master.d2l4isn05opwbv.amplifyapp.com/profile/0a1afd61-4de1-4925-a2c1-a46220739793",
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
            
                        # Testing form with selector div[class*='-translate-x-1/2']
            # Testing form with selector div[class*='translate-y-1/2']
            
# Testing input elements
            
# Testing button elements
            try:
                print(f'Testing button: [aria-label=\'Toggle menu\']')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_7_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("[aria-label='Toggle menu']").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_20_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: [aria-label=\'Toggle menu\']')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="[aria-label='Toggle menu']",
                    description='[aria-label=\'Toggle menu\']',
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
                    selector="[aria-label='Toggle menu']",
                    description='[aria-label=\'Toggle menu\']',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: [aria-label=\'Switch to dark mode\']')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_60_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("[aria-label='Switch to dark mode']").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_73_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: [aria-label=\'Switch to dark mode\']')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="[aria-label='Switch to dark mode']",
                    description='[aria-label=\'Switch to dark mode\']',
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
                    selector="[aria-label='Switch to dark mode']",
                    description='[aria-label=\'Switch to dark mode\']',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: [aria-label=\'Change language\']')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_113_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("[aria-label='Change language']").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_126_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: [aria-label=\'Change language\']')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="[aria-label='Change language']",
                    description='[aria-label=\'Change language\']',
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
                    selector="[aria-label='Change language']",
                    description='[aria-label=\'Change language\']',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_166_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator('html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(3)').click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_179_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(3)',
                    description='html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div',
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
                    selector='html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(3)',
                    description='html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_219_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator('html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > button:nth-child(1)').click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_232_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > button:nth-child(1)',
                    description='html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div',
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
                    selector='html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > button:nth-child(1)',
                    description='html:nth-child(1) > body:nth-child(2) > div:nth-child(2) > div:nth-child(1) > nav:nth-child(1) > div',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: Follow')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_272_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator('button.flex:nth-match(1)').click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_285_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: Follow')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='button.flex:nth-match(1)',
                    description='Follow',
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
                    selector='button.flex:nth-match(1)',
                    description='Follow',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: Message')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_325_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("button:has-text('Message'):nth-match(2)").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_338_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: Message')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="button:has-text('Message'):nth-match(2)",
                    description='Message',
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
                    selector="button:has-text('Message'):nth-match(2)",
                    description='Message',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: about')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_378_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator('button.py-2:nth-match(3)').click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_391_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: about')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='button.py-2:nth-match(3)',
                    description='about',
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
                    selector='button.py-2:nth-match(3)',
                    description='about',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: experience')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_431_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("button:has-text('experience'):nth-match(4)").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_444_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: experience')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="button:has-text('experience'):nth-match(4)",
                    description='experience',
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
                    selector="button:has-text('experience'):nth-match(4)",
                    description='experience',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: education')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_484_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("button:has-text('education'):nth-match(5)").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_497_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: education')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="button:has-text('education'):nth-match(5)",
                    description='education',
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
                    selector="button:has-text('education'):nth-match(5)",
                    description='education',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: skills')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_537_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("button:has-text('skills'):nth-match(6)").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_550_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: skills')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="button:has-text('skills'):nth-match(6)",
                    description='skills',
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
                    selector="button:has-text('skills'):nth-match(6)",
                    description='skills',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: Try now')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_590_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("button:has-text('Try now'):nth-match(7)").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_603_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: Try now')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="button:has-text('Try now'):nth-match(7)",
                    description='Try now',
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
                    selector="button:has-text('Try now'):nth-match(7)",
                    description='Try now',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: Register')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_643_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator('button.text-sm:nth-match(8)').click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_656_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: Register')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector='button.text-sm:nth-match(8)',
                    description='Register',
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
                    selector='button.text-sm:nth-match(8)',
                    description='Register',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: App Store')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_696_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("button:has-text('App Store'):nth-match(9)").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_709_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: App Store')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="button:has-text('App Store'):nth-match(9)",
                    description='App Store',
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
                    selector="button:has-text('App Store'):nth-match(9)",
                    description='App Store',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing button: Google Play')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'button_749_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("button:has-text('Google Play'):nth-match(10)").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'button_762_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with button: Google Play')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='button',
                    selector="button:has-text('Google Play'):nth-match(10)",
                    description='Google Play',
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
                    selector="button:has-text('Google Play'):nth-match(10)",
                    description='Google Play',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            
# Testing link elements
            try:
                print(f'Testing link: Community')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_803_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='/community']:has-text('Community')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_816_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Community')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/community']:has-text('Community')",
                    description='Community',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/community']:has-text('Community')",
                    description='Community',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Internships')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_856_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='/internships']:has-text('Internships')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_869_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Internships')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/internships']:has-text('Internships')",
                    description='Internships',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/internships']:has-text('Internships')",
                    description='Internships',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Jobs')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_909_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='/jobs']:has-text('Jobs')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_922_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Jobs')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/jobs']:has-text('Jobs')",
                    description='Jobs',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/jobs']:has-text('Jobs')",
                    description='Jobs',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: CV')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_962_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='/CV']:has-text('CV')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_975_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: CV')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/CV']:has-text('CV')",
                    description='CV',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/CV']:has-text('CV')",
                    description='CV',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Courses')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1015_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='/courses']:has-text('Courses')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1028_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Courses')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/courses']:has-text('Courses')",
                    description='Courses',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/courses']:has-text('Courses')",
                    description='Courses',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Explore All Companies')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1068_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='/company']:has-text('Explore All Companies')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1081_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Explore All Companies')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/company']:has-text('Explore All Companies')",
                    description='Explore All Companies',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='/company']:has-text('Explore All Companies')",
                    description='Explore All Companies',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: About / Press')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1121_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('About / Press')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1134_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: About / Press')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('About / Press')",
                    description='About / Press',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('About / Press')",
                    description='About / Press',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Awards')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1174_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Awards')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1187_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Awards')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Awards')",
                    description='Awards',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Awards')",
                    description='Awards',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Blog')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1227_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1240_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Blog')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']",
                    description='Blog',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']",
                    description='Blog',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Research')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1280_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Research')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1293_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Research')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Research')",
                    description='Research',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Research')",
                    description='Research',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Contact Us')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1333_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Contact Us')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1346_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Contact Us')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Contact Us')",
                    description='Contact Us',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Contact Us')",
                    description='Contact Us',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Guides')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1386_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Guides')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1399_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Guides')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Guides')",
                    description='Guides',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Guides')",
                    description='Guides',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Get a Free Employer Account')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1439_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Get a Free Employer Account')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1452_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Get a Free Employer Account')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Get a Free Employer Account')",
                    description='Get a Free Employer Account',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Get a Free Employer Account')",
                    description='Get a Free Employer Account',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Employer Center')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1492_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Employer Center')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1505_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Employer Center')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Employer Center')",
                    description='Employer Center',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Employer Center')",
                    description='Employer Center',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Help')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1545_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Help')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1558_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Help')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Help')",
                    description='Help',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Help')",
                    description='Help',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Guidelines')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1598_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Guidelines')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1611_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Guidelines')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Guidelines')",
                    description='Guidelines',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Guidelines')",
                    description='Guidelines',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Terms of Use')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1651_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Terms of Use')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1664_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Terms of Use')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Terms of Use')",
                    description='Terms of Use',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Terms of Use')",
                    description='Terms of Use',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Privacy & Ad Choices')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1704_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Privacy & Ad Choices')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1717_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Privacy & Ad Choices')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Privacy & Ad Choices')",
                    description='Privacy & Ad Choices',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Privacy & Ad Choices')",
                    description='Privacy & Ad Choices',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Do Not Sell Or Share')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1757_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Do Not Sell Or Share')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1770_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Do Not Sell Or Share')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Do Not Sell Or Share')",
                    description='Do Not Sell Or Share',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Do Not Sell Or Share')",
                    description='Do Not Sell Or Share',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: My Information')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1810_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('My Information')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1823_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: My Information')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('My Information')",
                    description='My Information',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('My Information')",
                    description='My Information',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Cookie Consent Tool')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1863_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Cookie Consent Tool')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1876_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Cookie Consent Tool')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Cookie Consent Tool')",
                    description='Cookie Consent Tool',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Cookie Consent Tool')",
                    description='Cookie Consent Tool',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Security')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1916_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Security')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1929_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Security')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Security')",
                    description='Security',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Security')",
                    description='Security',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Advertisers')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_1969_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Advertisers')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_1982_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Advertisers')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Advertisers')",
                    description='Advertisers',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Advertisers')",
                    description='Advertisers',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility
            try:
                print(f'Testing link: Careers')
                # Take screenshot before interaction
                before_screenshot = take_screenshot(page, 'link_2022_before')
                # Record URL and title before interaction
                before_url = page.url
                before_title = page.title()
                # Perform the action
                page.locator("a[href='#']:has-text('Careers')").click(timeout=3000)
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
                after_screenshot = take_screenshot(page, 'link_2035_after')
                # Detect visual changes
                visual_changed = detect_visual_change(before_screenshot, after_screenshot)
                if visual_changed:
                    print(f'Visual changes detected after interacting with link: Careers')
                # Record element effectiveness
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Careers')",
                    description='Careers',
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
                print(f'Error interacting with link element: {e}')
                # Record failed interaction
                element_tracker.record_element_test(
                    page_url=original_url,
                    element_type='link',
                    selector="a[href='#']:has-text('Careers')",
                    description='Careers',
                    success=False,
                    error_message=str(e)
                )
                # Continue with other elements
                time.sleep(1)  # Add delay for visibility

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
