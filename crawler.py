import os
import re
import time
import logging
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
from session_manager import session_manager

logging.basicConfig(level=logging.INFO)

def is_internal_link(base_url, link):
    base_domain = urlparse(base_url).netloc
    url_domain = urlparse(link).netloc
    
    # Log the domains being compared for debugging
    logging.info(f"Comparing domains - Base: {base_domain}, URL: {url_domain}")
    
    # If the URL has no domain (relative URL), it's internal
    if not url_domain:
        logging.info(f"URL {link} is a relative URL, treating as internal")
        return True
    
    # Check if domains match
    is_internal = base_domain == url_domain
    logging.info(f"URL {link} is {'internal' if is_internal else 'external'} to {base_url}")
    return is_internal

def normalize_url(url):
    # Log the URL being normalized for debugging
    logging.info(f"Normalizing URL: {url}")
    
    parsed = urlparse(url)
    
    # Handle relative URLs
    if not parsed.netloc and not parsed.scheme:
        logging.warning(f"Found relative URL: {url} - this should be resolved with base_url before normalization")
    
    # Normalize scheme and netloc, remove fragments and query parameters
    normalized = parsed._replace(fragment="", query="").geturl().rstrip('/')
    logging.info(f"Normalized URL: {normalized}")
    return normalized

def make_safe_filename(url, max_length=150):
    safe = re.sub(r'[^a-zA-Z0-9]', '_', url)
    return safe[:max_length]

def sanitize_filename(url):
    """Convert URL to a valid filename"""
    # Remove protocol and domain
    filename = re.sub(r'^https?://', '', url)
    # Replace invalid filename characters
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # Replace slashes with underscores
    filename = filename.replace('/', '_')
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    return filename

def perform_login(page, auth_params):
    """Perform login on the given page using provided authentication parameters"""
    try:
        login_url = auth_params.get('login_url')
        username = auth_params.get('username')
        password = auth_params.get('password')
        
        logging.info(f"Attempting to log in at {login_url}")
        
        # Navigate to login page
        page.goto(login_url, timeout=60000)
        page.wait_for_load_state('networkidle', timeout=60000)
        
        # Look for common username/email input fields
        username_selectors = [
            'input[type="email"]', 
            'input[name="email"]',
            'input[id*="email"]',
            'input[id="email"]',
            'input[type="text"][name*="user"]',
            'input[type="text"][id*="user"]',
            'input[name="username"]',
            'input[id="username"]',
            'input[name="login"]',
            'input[id="login"]'
        ]
        
        # Try each selector until we find a match
        username_input = None
        for selector in username_selectors:
            if page.query_selector(selector):
                username_input = selector
                break
        
        # If we found a username field, fill it
        if username_input:
            page.fill(username_input, username)
            logging.info(f"Filled username/email field using selector: {username_input}")
        else:
            logging.warning("Could not find username/email input field")
            return False
        
        # Look for password input field
        password_selector = 'input[type="password"]'
        if page.query_selector(password_selector):
            page.fill(password_selector, password)
            logging.info("Filled password field")
        else:
            logging.warning("Could not find password input field")
            return False
        
        # Look for login button/submit button
        submit_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button[id="submit"]',
            'button:has-text("Log in")',
            'button:has-text("Login")',
            'button:has-text("Sign in")',
            'button:has-text("Signin")',
            'button:has-text("Submit")',
            'button:has-text("Continue with email")',
            'a:has-text("Log in")',
            'a:has-text("Login")',
            'a:has-text("Sign in")',
            'a:has-text("Signin")',
            'a:has-text("Continue with email")',
            'button.w-full.bg-\\[\\#14a970\\]',
            'button.w-full:has-text("Continue")',
            'button:has-text("Continue")'
        ]
        
        # Try each submit selector until we find a match
        submit_button = None
        for selector in submit_selectors:
            if page.query_selector(selector):
                submit_button = selector
                break
        
        # If we found a submit button, click it
        if submit_button:
            # Take screenshot before login
            os.makedirs('screenshots', exist_ok=True)
            page.screenshot(path=os.path.join('screenshots', 'before_login.png'))
            
            # Click the login button and wait for navigation
            try:
                # First try clicking the button and waiting for navigation
                with page.expect_navigation(timeout=10000):
                    page.click(submit_button)
            except Exception as e:
                logging.info(f"No navigation occurred after clicking submit button: {e}")
                # If no navigation occurs, the form might be submitted via JavaScript
                # Try clicking without waiting for navigation
                page.click(submit_button)
                # Give some time for any JavaScript to execute
                page.wait_for_timeout(3000)
                
                # If the form has a JavaScript submit handler, try to trigger form submission directly
                form_selector = 'form'
                if page.query_selector(form_selector):
                    logging.info("Attempting to submit form via JavaScript")
                    page.evaluate("document.querySelector('form').submit()")
                    
            # Wait for any network activity to settle
            page.wait_for_load_state('networkidle', timeout=60000)
            
            # Take screenshot after login
            page.screenshot(path=os.path.join('screenshots', 'after_login.png'))
            
            logging.info(f"Clicked login button using selector: {submit_button}")
            
            # Check if login was successful by looking for common failure indicators
            failure_indicators = [
                # Error messages
                'text=incorrect password',
                'text=invalid username',
                'text=invalid email',
                'text=login failed',
                # Do not check for password field as it may still be present in multi-step login processes
                # Do not check for the submit button as it may still be present after clicking
                # Check for specific error messages or elements that indicate login failure
                'text=Invalid credentials',
                '.error-message',
                '.alert-danger',
                '#error:not(:empty)',  # Check for non-empty error span with id="error"
                'span#error:not(:empty)',  # Alternative selector for error span
                # Remove the submit button check as it's causing false failures
                # submit_button
            ]
            
            # First check for failure indicators
            for indicator in failure_indicators:
                if page.query_selector(indicator):
                    logging.warning(f"Login appears to have failed. Found indicator: {indicator}")
                    return False
            
            # Then check for success indicators - elements that would only appear after successful login
            success_indicators = [
                'button#logout',  # Logout button
                'button#add-contact',  # Add contact button
                'h1:has-text("Contact List")',  # Contact list heading
                'table#myTable',  # Contact table
                '.contactTable',  # Contact table class
                '#contactTable',  # Contact table id
                'button:has-text("Logout")',  # Logout button text
                'button:has-text("Add a New Contact")'  # Add contact button text
            ]
            
            # Check if any success indicator is present
            success_found = False
            for indicator in success_indicators:
                if page.query_selector(indicator):
                    logging.info(f"Login successful! Found success indicator: {indicator}")
                    success_found = True
                    break
            
            # If we're still on the login page, it's likely the login failed
            if page.query_selector('button#submit') and page.query_selector('input#password'):
                logging.warning("Still on login page after submission. Login likely failed.")
                return False
            
            # If we found success indicators or we're no longer on the login page, consider it a success
            if success_found or not page.query_selector('button#submit'):
                logging.info("Login appears to be successful")
                
                # Display success message
                success_message = "Login successful! Authenticated session established."
                logging.info(success_message)
                
                # Save the authenticated session for reuse in tests
                logging.info("Saving authenticated session for future test runs")
                from session_manager import session_manager
                session_manager.save_session(page)
                
                # Take a screenshot with success message overlay
                page.evaluate("""
                    () => {
                        const div = document.createElement('div');
                        div.id = 'login-success-message';
                        div.style.position = 'fixed';
                        div.style.top = '20px';
                        div.style.left = '50%';
                        div.style.transform = 'translateX(-50%)';
                        div.style.backgroundColor = 'rgba(40, 167, 69, 0.9)';
                        div.style.color = 'white';
                        div.style.padding = '10px 20px';
                        div.style.borderRadius = '5px';
                        div.style.zIndex = '9999';
                        div.style.fontWeight = 'bold';
                        div.textContent = 'Login Successful!';
                        document.body.appendChild(div);
                        
                        // Remove the message after 5 seconds
                        setTimeout(() => {
                            const msgElement = document.getElementById('login-success-message');
                            if (msgElement) msgElement.remove();
                        }, 5000);
                    }
                """)
                
                # Take another screenshot with the success message
                page.screenshot(path=os.path.join('screenshots', 'login_success.png'))
                
                return True
            else:
                logging.warning("Could not confirm successful login. Proceeding with caution.")
                # Return true anyway since we didn't find explicit failure indicators
                
                # Save the authenticated session for reuse in tests
                logging.info("Saving authenticated session for future test runs even without explicit success indicators")
                from session_manager import session_manager
                session_manager.save_session(page)
                
                return True
            
            # Take a screenshot with success message overlay
            page.evaluate("""
                () => {
                    const div = document.createElement('div');
                    div.id = 'login-success-message';
                    div.style.position = 'fixed';
                    div.style.top = '20px';
                    div.style.left = '50%';
                    div.style.transform = 'translateX(-50%)';
                    div.style.backgroundColor = 'rgba(40, 167, 69, 0.9)';
                    div.style.color = 'white';
                    div.style.padding = '10px 20px';
                    div.style.borderRadius = '5px';
                    div.style.zIndex = '9999';
                    div.style.fontWeight = 'bold';
                    div.textContent = 'Login Successful!';
                    document.body.appendChild(div);
                    
                    // Remove the message after 5 seconds
                    setTimeout(() => {
                        const msgElement = document.getElementById('login-success-message');
                        if (msgElement) msgElement.remove();
                    }, 5000);
                }
            """)
            
            # Take another screenshot with the success message
            page.screenshot(path=os.path.join('screenshots', 'login_success.png'))
            
            return True
        else:
            logging.warning("Could not find login/submit button")
            return False
            
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return False

def crawl_website_and_screenshot(base_url, out_dir="screenshots", max_depth=3, throttle_seconds=1, single_page_mode=False, requires_auth=False, auth_params=None):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs('html_files', exist_ok=True)
    visited = set()
    to_visit = [(normalize_url(base_url), 0)]
    pages = []
    login_successful = False

    with sync_playwright() as p:
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
        
        # Handle authentication if required
        if requires_auth and auth_params:
            logging.info("Authentication required. First crawling the login page...")
            login_url = auth_params.get('login_url')
            
            # First crawl the login page before authentication
            login_page = browser.new_page()
            logging.info(f"Crawling login page: {login_url}")
            login_page.goto(login_url, timeout=60000)
            login_page.wait_for_load_state('networkidle', timeout=60000)
            
            # Save login page screenshot and HTML
            login_page_url = normalize_url(login_page.url)
            login_filename = make_safe_filename(login_page_url)
            login_screenshot_path = os.path.join(out_dir, login_filename + "_before_auth.png")
            login_page.screenshot(path=login_screenshot_path, full_page=True)
            
            # Save login page HTML
            login_html = login_page.content()
            login_html_path = os.path.join('html_files', login_filename + "_before_auth.html")
            with open(login_html_path, "w", encoding="utf-8") as f:
                f.write(login_html)
            
            # Store login page info
            pages.append({
                'url': login_page_url,
                'html': login_html,
                'screenshot': login_screenshot_path,
                'html_file': login_html_path
            })
            
            # Extract internal links from login page if not in single page mode
            if not single_page_mode:
                try:
                    logging.info(f"Extracting links from login page: {login_page_url}")
                    # Extract links from <a> tags
                    a_links = login_page.eval_on_selector_all('a[href]', 'elements => elements.map(a => a.href)')
                    logging.info(f"Found {len(a_links)} <a> links on login page")
                    
                    # Extract links from onclick attributes (like buttons with location.href)
                    onclick_links = login_page.eval_on_selector_all('[onclick*="location.href"]', 
                        '''elements => elements.map(el => {
                            const match = el.getAttribute("onclick").match(/location\.href=[\"\\']([^\"\\']+)[\"\\']/);
                            return match ? match[1] : null;
                        }).filter(link => link !== null)'''
                    )
                    logging.info(f"Found {len(onclick_links)} onclick links on login page")
                    
                    # Combine all links
                    links = a_links + onclick_links
                    logging.info(f"Total of {len(links)} links found on login page")
                    
                    for link in links:
                        # Handle relative URLs by joining with the login page URL
                        if not urlparse(link).netloc:
                            absolute_link = urljoin(login_page_url, link)
                            logging.info(f"Converted relative URL {link} to absolute URL {absolute_link}")
                            link = absolute_link
                        
                        normalized_link = normalize_url(link)
                        logging.info(f"Normalized link: {normalized_link}")
                        
                        if is_internal_link(base_url, normalized_link) and normalized_link not in visited:
                            logging.info(f"Adding internal link to visit: {normalized_link} (depth 1)")
                            to_visit.append((normalized_link, 1))
                except Exception as e:
                    logging.error(f"Error extracting links from login page: {e}")
            
            # Now proceed with login
            logging.info("Now attempting to log in...")
            auth_page = browser.new_page()
            login_successful = perform_login(auth_page, auth_params)
            
            # Create a login result dictionary to return with pages
            login_result = {
                'success': login_successful,
                'message': "Login successful! Authenticated session established." if login_successful else "Login failed. Check your credentials.",
                'screenshot': os.path.join('screenshots', 'login_success.png') if login_successful else os.path.join('screenshots', 'after_login.png')
            }
            
            # Close the login page as we now have the authenticated page
            login_page.close()
            
            if login_successful:
                logging.info("Login successful! Proceeding with crawling.")
                # If login was successful, we'll use the authenticated page for further crawling
                login_domain = urlparse(auth_params.get('login_url')).netloc
                target_domain = urlparse(base_url).netloc
                
                # Stay on the current authenticated page after login
                logging.info(f"Using authenticated page for crawling")
                auth_page.wait_for_load_state('networkidle', timeout=60000)
                
                # Process the authenticated page
                auth_url = normalize_url(auth_page.url)
                visited.add(auth_url)
                
                # Save screenshot of authenticated page
                auth_filename = make_safe_filename(auth_url)
                auth_screenshot_path = os.path.join(out_dir, auth_filename + "_after_auth.png")
                auth_page.screenshot(path=auth_screenshot_path, full_page=True)
                
                # Save HTML of authenticated page
                auth_html = auth_page.content()
                auth_html_path = os.path.join('html_files', auth_filename + "_after_auth.html")
                with open(auth_html_path, "w", encoding="utf-8") as f:
                    f.write(auth_html)
                
                # Store authenticated page info
                pages.append({
                    'url': auth_url,
                    'html': auth_html,
                    'screenshot': auth_screenshot_path,
                    'html_file': auth_html_path
                })
                
                # Extract internal links from authenticated page if not in single page mode
                if not single_page_mode:
                    try:
                        logging.info(f"Extracting links from authenticated page: {auth_url}")
                        # Extract links from <a> tags
                        a_links = auth_page.eval_on_selector_all('a[href]', 'elements => elements.map(a => a.href)')
                        logging.info(f"Found {len(a_links)} <a> links on authenticated page")
                        
                        # Extract links from onclick attributes (like buttons with location.href)
                        onclick_links = auth_page.eval_on_selector_all('[onclick*="location.href"]', 
                            '''elements => elements.map(el => {
                                const match = el.getAttribute("onclick").match(/location\.href=[\"\\']([^\"\\']+)[\"\\']/);
                                return match ? match[1] : null;
                            }).filter(link => link !== null)'''
                        )
                        logging.info(f"Found {len(onclick_links)} onclick links on authenticated page")
                        
                        # Combine all links
                        links = a_links + onclick_links
                        logging.info(f"Total of {len(links)} links found on authenticated page")
                        
                        for link in links:
                            # Handle relative URLs by joining with the authenticated page URL
                            if not urlparse(link).netloc:
                                absolute_link = urljoin(auth_url, link)
                                logging.info(f"Converted relative URL {link} to absolute URL {absolute_link}")
                                link = absolute_link
                            
                            normalized_link = normalize_url(link)
                            logging.info(f"Normalized link: {normalized_link}")
                            
                            if is_internal_link(base_url, normalized_link) and normalized_link not in visited:
                                logging.info(f"Adding internal link to visit: {normalized_link}")
                                to_visit.append((normalized_link, 1))
                    except Exception as e:
                        logging.error(f"Error extracting links from authenticated page: {e}")
                else:
                    logging.info("Single page mode enabled - not extracting links from authenticated page")
                
                # We no longer need to keep the auth_context since we'll create a new context for each page
                # and apply the session to it
            else:
                logging.error("Login failed. Proceeding without authentication.")
                auth_page.close()
        
        # Continue with regular crawling for remaining URLs
        while to_visit:
            url, depth = to_visit.pop(0)
            if url in visited or depth > max_depth:
                continue
            visited.add(url)

            for attempt in range(3):  # Retry logic
                try:
                    logging.info(f"Crawling: {url} (depth {depth})")
                    
                    # Instead of creating a new context and page for each URL,
                    # reuse the authenticated page if login was successful
                    if login_successful and 'auth_page' in locals():
                        page = auth_page
                        logging.info(f"Reusing authenticated page for: {url}")
                    else:
                        # Create a new context for each page to avoid the 'Please use browser.new_context()' error
                        # but reuse the authentication by applying the session
                        context = browser.new_context()
                        
                        # If login was successful, apply the saved session to this context
                        if login_successful:
                            from session_manager import session_manager
                            session_manager.load_session(context, url)
                            logging.info(f"Applied authenticated session for: {url}")
                        
                        # Create a new page from this context
                        page = context.new_page()
                        
                        # Apply localStorage and sessionStorage after page is created
                        if login_successful:
                            session_manager.apply_storage(page)
                            logging.info(f"Applied storage (localStorage/sessionStorage) for: {url}")
                    
                    # Navigate to the URL
                    page.goto(url, timeout=60000)
                    page.wait_for_load_state('networkidle', timeout=60000)

                    final_url = normalize_url(page.url)
                    if final_url != url:
                        if final_url in visited:
                            # Don't close the page if it's the auth_page
                            if not (login_successful and page == auth_page):
                                page.close()
                            break
                        visited.add(final_url)
                        url = final_url

                    # Save screenshot
                    filename = make_safe_filename(url)
                    screenshot_path = os.path.join(out_dir, filename + ".png")
                    page.screenshot(path=screenshot_path, full_page=True)

                    # Save HTML
                    html = page.content()
                    html_path = os.path.join('html_files', filename + ".html")
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html)

                    # Store page info
                    pages.append({
                        'url': url,
                        'html': html,
                        'screenshot': screenshot_path,
                        'html_file': html_path
                    })

                    # Extract internal links (only if not in single page mode)
                    if not single_page_mode:
                        try:
                            logging.info(f"Extracting links from page: {url}")
                            # Extract links from <a> tags
                            a_links = page.eval_on_selector_all('a[href]', 'elements => elements.map(a => a.href)')
                            logging.info(f"Found {len(a_links)} <a> links on page")
                            
                            # Extract links from onclick attributes (like buttons with location.href)
                            onclick_links = page.eval_on_selector_all('[onclick*="location.href"]', 
                                '''elements => elements.map(el => {
                                    const match = el.getAttribute("onclick").match(/location\.href=[\"\\']([^\"\\']*)[\"\\']/);
                                    return match ? match[1] : null;
                                }).filter(link => link !== null)'''
                            )
                            logging.info(f"Found {len(onclick_links)} onclick links on page")
                            
                            # Combine all links
                            links = a_links + onclick_links
                            logging.info(f"Total of {len(links)} links found on page")
                            
                            for link in links:
                                # Handle relative URLs by joining with the current page URL
                                if not urlparse(link).netloc:
                                    absolute_link = urljoin(url, link)
                                    logging.info(f"Converted relative URL {link} to absolute URL {absolute_link}")
                                    link = absolute_link
                                
                                normalized_link = normalize_url(link)
                                if is_internal_link(base_url, normalized_link) and normalized_link not in visited:
                                    logging.info(f"Adding internal link to visit: {normalized_link} (depth {depth + 1})")
                                    to_visit.append((normalized_link, depth + 1))
                        except Exception as e:
                            logging.error(f"Error extracting links from page {url}: {e}")

                    # Only close the page and context if it's not the auth_page
                    if not (login_successful and page == auth_page):
                        page.close()
                        context.close()
                    
                    time.sleep(throttle_seconds)  # Optional throttling
                    break  # Successful crawl
                except Exception as e:
                    logging.warning(f"Failed to process {url} (attempt {attempt + 1}/3): {e}")
                    if attempt == 2:
                        logging.error(f"Giving up on {url} after 3 failed attempts.")
                    # Clean up resources in case of error
                    # Only close the page and context if it's not the auth_page
                    if 'page' in locals() and not (login_successful and page == auth_page):
                        try:
                            page.close()
                        except:
                            pass
                    if 'context' in locals() and not (login_successful and 'auth_page' in locals() and page == auth_page):
                        try:
                            context.close()
                        except:
                            pass
        
        # Close any remaining browser resources
        if login_successful and 'auth_page' in locals() and not auth_page.is_closed():
            auth_page.close()
        
        browser.close()
        
        # Return the list of crawled pages and login result if authentication was required
        if requires_auth and auth_params:
            return pages, login_result
        else:
            return pages
    
    # This code is unreachable - removing it
    # Return login result along with pages if authentication was required
    # if requires_auth and auth_params:
    #     return pages, login_result
    # else:
    #     return pages
