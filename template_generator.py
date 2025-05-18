import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class RoleBasedTestGenerator:
    """
    Generates Playwright tests based on roles and templates instead of using AI.
    This approach identifies UI elements by their roles and generates appropriate
    test actions based on predefined templates.
    """

    def __init__(self):
        # Define role-based selectors and actions with expanded coverage for better website compatibility
        self.role_selectors = {
            # Interactive elements - expanded to catch ALL possible buttons
            'button': {
                'selector': 'button, [role="button"], input[type="button"], input[type="submit"], input[type="reset"], input[type="image"], [class*="btn"], [class*="button"], [aria-pressed], [onclick], [onmousedown], [onmouseup], [data-action], [type="button"], [aria-label], [tabindex]:not([tabindex="-1"]), [class*="clickable"], [class*="click"], [class*="trigger"], [class*="control"], [class*="action"]',
                'action': 'click'
            },
            'link': {
                'selector': 'a, [role="link"], [href]:not(link):not(script):not(style), [data-href], [data-link], [data-url], [class*="link"], [class*="nav-item"], [class*="menu-item"]',
                'action': 'click'
            },
            # Form elements - catch ALL input types
            'input': {
                'selector': 'input:not([type="button"]):not([type="submit"]):not([type="reset"]):not([type="hidden"]):not([type="checkbox"]):not([type="radio"]), textarea, [contenteditable="true"], [role="textbox"], [data-input], [aria-multiline="true"], [class*="input"], [class*="field"], [class*="text-field"], [class*="textarea"]',
                'action': 'fill'
            },
            'checkbox': {
                'selector': 'input[type="checkbox"], [role="checkbox"], [aria-checked], [data-checkbox], [class*="checkbox"], [class*="check"]',
                'action': 'check'
            },
            'radio': {
                'selector': 'input[type="radio"], [role="radio"], [data-radio], [class*="radio"]',
                'action': 'check'
            },
            'select': {
                'selector': 'select, [role="combobox"], [role="listbox"], [aria-haspopup="listbox"], [data-select], [class*="select"], [class*="dropdown"], [class*="combobox"]',
                'action': 'select_option'
            },
            # Navigation elements
            'tab': {
                'selector': '[role="tab"], [aria-selected], [data-tab], [class*="tab"], [class*="nav-link"]',
                'action': 'click'
            },
            'menu': {
                'selector': '[role="menu"], [role="menuitem"], [aria-haspopup="menu"], [data-menu], .dropdown, .dropdown-item, .menu-item, [class*="menu"], [class*="dropdown"]',
                'action': 'click'
            },
            # Interactive containers
            'dialog': {
                'selector': '[role="dialog"], [role="alertdialog"], [aria-modal="true"], .modal, .dialog, [data-modal], [class*="modal"], [class*="dialog"], [class*="popup"], [class*="overlay"]',
                'action': 'detect'
            },
            'alert': {
                'selector': '[role="alert"], [aria-live="assertive"], .alert, .notification, [data-alert], [class*="alert"], [class*="notification"], [class*="toast"]',
                'action': 'detect'
            },
            # Forms
            'form': {
                'selector': 'form, [role="form"], [data-form], [class*="form"]',
                'action': 'submit'
            },
            # Additional interactive elements
            'slider': {
                'selector': 'input[type="range"], [role="slider"], [data-slider], [class*="slider"], [class*="range"]',
                'action': 'slide'
            },
            'toggle': {
                'selector': '[role="switch"], .toggle, [data-toggle], [aria-checked], [class*="toggle"], [class*="switch"]',
                'action': 'toggle'
            },
            'datepicker': {
                'selector': 'input[type="date"], [role="date"], [data-datepicker], input[type="datetime-local"], [class*="datepicker"], [class*="date-picker"]',
                'action': 'fill'
            },
            'file': {
                'selector': 'input[type="file"], [role="upload"], [data-upload], [class*="file-input"], [class*="upload"]',
                'action': 'detect'
            },
            # Catch-all for any remaining interactive elements
            'interactive': {
                'selector': '[tabindex]:not([tabindex="-1"]), [class*="interactive"], [class*="selectable"], [class*="hoverable"], [class*="focusable"]',
                'action': 'click'
            }
        }

        # Define templates for different actions with improved error handling
        self.step_templates = {
            'click': "page.locator({selector}).click(timeout=3000)\ntry:\n    page.wait_for_load_state('networkidle', timeout=5000)\nexcept Exception as e:\n    print(f'Navigation wait error: {{e}}')\npage.goto(original_url, timeout=5000)\ntry:\n    page.wait_for_load_state('networkidle', timeout=5000)\nexcept Exception as e:\n    print(f'Return navigation wait error: {{e}}')",
            'fill': "page.locator({selector}).fill(\"test value\")",
            'check': "page.locator({selector}).check()",
            'select_option': "page.locator({selector}).select_option(value='1')",
            'detect': "is_visible = page.locator({selector}).is_visible()",
            'submit': "page.locator({selector}).evaluate(\"form => form.submit()\")",
            'slide': "page.locator({selector}).fill('50')",
            'toggle': "page.locator({selector}).click()"
        }

    def optimize_html(self, html):
        """
        Optimize HTML content for test generation by removing unnecessary elements.
        """
        try:
            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script tags (not needed for UI testing)
            for script in soup.find_all('script'):
                script.decompose()

            # Remove style tags (not needed for UI testing)
            for style in soup.find_all('style'):
                style.decompose()

            # Remove comments
            for comment in soup.find_all(text=lambda text: isinstance(text, str) and text.strip().startswith('<!--')):
                comment.extract()

            # Remove meta tags (not needed for UI testing)
            for meta in soup.find_all('meta'):
                meta.decompose()

            # Remove link tags (CSS, favicons, etc.)
            for link in soup.find_all('link'):
                link.decompose()

            # Remove SVG elements (often decorative)
            for svg in soup.find_all('svg'):
                svg.decompose()

            # Get the optimized HTML
            return soup
        except Exception as e:
            print(f"Error optimizing HTML: {e}")
            # Return original HTML if optimization fails
            return BeautifulSoup(html, 'html.parser')

    def extract_elements_by_role(self, soup):
        """Extract ABSOLUTELY ALL elements from the HTML without any filtering"""
        elements_by_role = {}
        processed_elements = set()  # Track elements we've already processed to avoid duplicates

        # FIRST PASS: Get all buttons and inputs directly using tag selectors
        # This ensures we don't miss any buttons or inputs regardless of attributes
        try:
            # Get all buttons by tag name
            all_buttons = soup.find_all('button')
            if 'button' not in elements_by_role:
                elements_by_role['button'] = []

            for element in all_buttons:
                element_id = self._get_element_unique_id(element)
                processed_elements.add(element_id)

                # Check if the button has SVG content
                has_svg = bool(element.find('svg'))

                # For all buttons, we need better position tracking
                # Get parent information for better selectors
                parent = element.parent
                parent_id = parent.get('id', '') if parent else ''
                parent_class = ' '.join(parent.get('class', [])) if parent and parent.get('class') else ''
                parent_tag = parent.name if parent else ''

                # Get grandparent information for even more specific selectors
                grandparent = parent.parent if parent else None
                grandparent_id = grandparent.get('id', '') if grandparent else ''
                grandparent_class = ' '.join(grandparent.get('class', [])) if grandparent and grandparent.get('class') else ''
                grandparent_tag = grandparent.name if grandparent else ''

                # Count position among siblings
                position = 1
                if parent:
                    for sibling in parent.find_all(recursive=False):
                        if sibling == element:
                            break
                        if sibling.name == element.name:
                            position += 1

                # Get the absolute position path for this button
                # This is a unique identifier based on the DOM structure
                absolute_position = []
                current = element
                while current and current.parent:
                    siblings = current.parent.find_all(recursive=False)
                    pos = 1
                    for sibling in siblings:
                        if sibling == current:
                            break
                        pos += 1
                    absolute_position.insert(0, (current.name, pos))
                    current = current.parent

                # For SVG buttons, also store the SVG path if available
                svg_path = None
                if has_svg:
                    svg = element.find('svg')
                    if svg:
                        path = svg.find('path')
                        if path and path.get('d'):
                            svg_path = path.get('d')[:20]  # Store just the beginning of the path

                element_info = {
                    'tag': 'button',
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                    'name': element.get('name', ''),
                    'type': element.get('type', ''),
                    'value': element.get('value', ''),
                    'placeholder': element.get('placeholder', ''),
                    'href': element.get('href', ''),
                    'text': element.get_text().strip(),
                    'aria-label': element.get('aria-label', ''),
                    'data-testid': element.get('data-testid', ''),
                    'data-cy': element.get('data-cy', ''),
                    'data-qa': element.get('data-qa', ''),
                    'role': element.get('role', ''),
                    'title': element.get('title', ''),
                    'alt': element.get('alt', ''),
                    'action': 'click',
                    'selector': None,
                    'has_svg': has_svg,
                    'position': position,
                    'parent_id': parent_id,
                    'parent_class': parent_class,
                    'parent_tag': parent_tag,
                    'grandparent_id': grandparent_id,
                    'grandparent_class': grandparent_class,
                    'grandparent_tag': grandparent_tag,
                    'absolute_position': absolute_position,
                    'onclick': element.get('onclick', ''),
                    'onmousedown': element.get('onmousedown', '')
                }

                # Add SVG path information if available
                if svg_path:
                    element_info['svg_path'] = svg_path

                # Create a selector for this element
                element_info['selector'] = self._create_selector_for_element(element_info)

                if element_info['selector']:
                    elements_by_role['button'].append(element_info)

            # Get all inputs by tag name
            all_inputs = soup.find_all('input')
            if 'input' not in elements_by_role:
                elements_by_role['input'] = []

            for element in all_inputs:
                input_type = element.get('type', '').lower()
                # Skip hidden inputs
                if input_type == 'hidden':
                    continue

                element_id = self._get_element_unique_id(element)
                processed_elements.add(element_id)

                # Determine the correct role and action based on input type
                if input_type in ('checkbox'):
                    role = 'checkbox'
                    action = 'check'
                elif input_type in ('radio'):
                    role = 'radio'
                    action = 'check'
                elif input_type in ('submit', 'button', 'reset', 'image'):
                    role = 'button'
                    action = 'click'
                else:  # text, email, password, search, tel, url, etc.
                    role = 'input'
                    action = 'fill'

                if role not in elements_by_role:
                    elements_by_role[role] = []

                element_info = {
                    'tag': 'input',
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                    'name': element.get('name', ''),
                    'type': input_type,
                    'value': element.get('value', ''),
                    'placeholder': element.get('placeholder', ''),
                    'href': element.get('href', ''),
                    'text': element.get('placeholder', '') or element.get('value', ''),
                    'aria-label': element.get('aria-label', ''),
                    'data-testid': element.get('data-testid', ''),
                    'data-cy': element.get('data-cy', ''),
                    'data-qa': element.get('data-qa', ''),
                    'role': element.get('role', ''),
                    'title': element.get('title', ''),
                    'alt': element.get('alt', ''),
                    'action': action,
                    'selector': None
                }

                # Create a selector for this element
                element_info['selector'] = self._create_selector_for_element(element_info)

                if element_info['selector']:
                    elements_by_role[role].append(element_info)
        except Exception as e:
            print(f"Error in direct tag extraction: {e}")

        # SECOND PASS: extract elements by role using standard selectors
        for role, role_info in self.role_selectors.items():
            selector = role_info['selector']
            action = role_info['action']

            try:
                # Find elements matching this role's selector
                elements = soup.select(selector)

                if elements:
                    if role not in elements_by_role:
                        elements_by_role[role] = []

                    for element in elements:
                        # Create a unique identifier for this element to avoid duplicates
                        element_id = self._get_element_unique_id(element)

                        # Skip if we've already processed this element
                        if element_id in processed_elements:
                            continue

                        processed_elements.add(element_id)

                        # Extract useful attributes for creating selectors
                        element_info = {
                            'tag': element.name,
                            'id': element.get('id', ''),
                            'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                            'name': element.get('name', ''),
                            'type': element.get('type', ''),
                            'value': element.get('value', ''),
                            'placeholder': element.get('placeholder', ''),
                            'href': element.get('href', ''),
                            'text': element.get_text().strip(),
                            'aria-label': element.get('aria-label', ''),
                            'data-testid': element.get('data-testid', ''),
                            'data-cy': element.get('data-cy', ''),
                            'data-qa': element.get('data-qa', ''),
                            'role': element.get('role', ''),
                            'title': element.get('title', ''),
                            'alt': element.get('alt', ''),
                            'action': action,
                            'selector': None  # Will be filled in later
                        }

                        # Create a selector for this element
                        element_info['selector'] = self._create_selector_for_element(element_info)

                        if element_info['selector']:
                            elements_by_role[role].append(element_info)
            except Exception as e:
                print(f"Error extracting {role} elements: {e}")

        # THIRD PASS: look for additional interactive elements that might have been missed
        try:
            # Split into multiple selectors to avoid malformed selector issues
            event_handlers_selector = (
                "[onclick], [onmousedown], [onmouseup], [onchange], [onfocus], [onblur], "
                "[onkeydown], [onkeyup], [onkeypress], [ondblclick], [ontouchstart], [ontouchend], "
                "[ontouchmove]"
            )

            tabindex_selector = "[tabindex]:not([tabindex=\"-1\"])"
            role_selector = "[role]"

            # Process each selector separately to avoid malformed selector issues
            interactive_elements = []
            interactive_elements.extend(soup.select(event_handlers_selector))
            interactive_elements.extend(soup.select(tabindex_selector))
            interactive_elements.extend(soup.select(role_selector))

            # Process aria attributes separately
            for element in soup.find_all(attrs=lambda attrs: attrs and any(attr.startswith('aria-') for attr in attrs)):
                interactive_elements.append(element)

            # Process all the interactive elements
            if 'interactive' not in elements_by_role:
                elements_by_role['interactive'] = []

            for element in interactive_elements:
                element_id = self._get_element_unique_id(element)
                if element_id in processed_elements:
                    continue

                processed_elements.add(element_id)

                # Determine the most appropriate role based on the element
                if element.name == 'button' or element.get('type') == 'button' or 'btn' in (element.get('class', '') or ''):
                    role = 'button'
                    action = 'click'
                elif element.name == 'a' or element.get('href'):
                    role = 'link'
                    action = 'click'
                elif element.name == 'input':
                    input_type = element.get('type', '').lower()
                    if input_type in ('text', 'email', 'password', 'search', 'tel', 'url'):
                        role = 'input'
                        action = 'fill'
                    elif input_type == 'checkbox':
                        role = 'checkbox'
                        action = 'check'
                    elif input_type == 'radio':
                        role = 'radio'
                        action = 'check'
                    elif input_type in ('submit', 'button', 'reset'):
                        role = 'button'
                        action = 'click'
                    else:
                        role = 'input'
                        action = 'fill'
                else:
                    role = 'clickable'
                    action = 'click'

                if role not in elements_by_role:
                    elements_by_role[role] = []

                element_info = {
                    'tag': element.name,
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                    'name': element.get('name', ''),
                    'type': element.get('type', ''),
                    'value': element.get('value', ''),
                    'placeholder': element.get('placeholder', ''),
                    'href': element.get('href', ''),
                    'text': element.get_text().strip(),
                    'aria-label': element.get('aria-label', ''),
                    'data-testid': element.get('data-testid', ''),
                    'data-cy': element.get('data-cy', ''),
                    'data-qa': element.get('data-qa', ''),
                    'role': element.get('role', ''),
                    'title': element.get('title', ''),
                    'alt': element.get('alt', ''),
                    'action': action,
                    'selector': None
                }

                element_info['selector'] = self._create_selector_for_element(element_info)
                if element_info['selector']:
                    elements_by_role[role].append(element_info)
        except Exception as e:
            print(f"Error in third pass element extraction: {e}")

        # FOURTH PASS: catch-all - get ALL remaining HTML elements that could be interactive
        try:
            # Get all elements that might be interactive but weren't caught by previous passes
            all_elements = soup.select('*')
            for element in all_elements:
                # Skip non-visible or non-interactive elements
                if element.name in ('html', 'head', 'meta', 'link', 'script', 'style', 'br', 'hr'):
                    continue

                element_id = self._get_element_unique_id(element)
                if element_id in processed_elements:
                    continue

                processed_elements.add(element_id)

                # Determine role and action based on tag name
                role = 'interactive'
                action = 'click'

                if element.name == 'button':
                    role = 'button'
                elif element.name == 'a':
                    role = 'link'
                elif element.name == 'input':
                    input_type = element.get('type', '').lower()
                    if input_type in ('text', 'email', 'password', 'search', 'tel', 'url'):
                        role = 'input'
                        action = 'fill'
                    elif input_type == 'checkbox':
                        role = 'checkbox'
                        action = 'check'
                    elif input_type == 'radio':
                        role = 'radio'
                        action = 'check'
                    elif input_type in ('submit', 'button', 'reset'):
                        role = 'button'
                    else:
                        role = 'input'
                        action = 'fill'
                elif element.name == 'select':
                    role = 'select'
                    action = 'select_option'
                elif element.name == 'textarea':
                    role = 'input'
                    action = 'fill'
                elif element.name == 'form':
                    role = 'form'
                    action = 'submit'
                elif element.name in ('div', 'span') and (element.get('class') or element.get('id') or element.get('tabindex')):
                    # Divs and spans with classes, IDs or tabindex might be interactive
                    role = 'clickable'

                if role not in elements_by_role:
                    elements_by_role[role] = []

                element_info = {
                    'tag': element.name,
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                    'name': element.get('name', ''),
                    'type': element.get('type', ''),
                    'value': element.get('value', ''),
                    'placeholder': element.get('placeholder', ''),
                    'href': element.get('href', ''),
                    'text': element.get_text().strip(),
                    'aria-label': element.get('aria-label', ''),
                    'data-testid': element.get('data-testid', ''),
                    'data-cy': element.get('data-cy', ''),
                    'data-qa': element.get('data-qa', ''),
                    'role': element.get('role', ''),
                    'title': element.get('title', ''),
                    'alt': element.get('alt', ''),
                    'action': action,
                    'selector': None
                }

                element_info['selector'] = self._create_selector_for_element(element_info)
                if element_info['selector']:
                    elements_by_role[role].append(element_info)
        except Exception as e:
            print(f"Error in fourth pass element extraction: {e}")

        print(f"Total elements found: {sum(len(elements) for elements in elements_by_role.values())}")
        for role, elements in elements_by_role.items():
            print(f"  - {role}: {len(elements)} elements")

        return elements_by_role

    def _get_element_unique_id(self, element):
        """Create a unique identifier for an element to avoid duplicates"""
        # For buttons, we need to be more careful to avoid filtering out similar buttons
        if element.name == 'button':
            # Try to use id first
            if element.get('id'):
                return f"id:{element['id']}"

            # For buttons, include position information to distinguish similar buttons
            parent = element.parent
            if parent:
                # Count position among siblings
                position = 1
                for sibling in parent.find_all(recursive=False):
                    if sibling == element:
                        break
                    if sibling.name == element.name:
                        position += 1

                # Include parent info in the ID
                parent_id = parent.get('id', '')
                parent_class = ' '.join(parent.get('class', [])) if parent.get('class') else ''

                # Create a more specific ID for buttons
                aria_label = element.get('aria-label', '')
                has_svg = bool(element.find('svg'))

                return f"button:{parent_id}:{parent_class}:{position}:{aria_label}:{has_svg}"

        # For other elements, use the standard approach
        if element.get('id'):
            return f"id:{element['id']}"

        # Use a combination of tag, class, and text content
        tag = element.name
        classes = ' '.join(element.get('class', []) if element.get('class') else [])
        text = element.get_text().strip()[:30]  # Limit text length

        # Add some other attributes if available
        attrs = []
        for attr in ['name', 'type', 'href', 'src', 'aria-label']:
            if element.get(attr):
                attrs.append(f"{attr}:{element[attr]}")

        # Combine everything into a unique string
        return f"{tag}:{classes}:{text}:{':'.join(attrs)}"

    def _create_selector_for_element(self, element_info):
        """
        Create a robust selector for an element based on its attributes.
        Prioritizes unique attributes that are less likely to change.
        """
        try:
            # Add a unique index to the element info to make selectors more specific
            # This helps avoid ambiguous selectors that match multiple elements
            static_counter = getattr(self, '_selector_counter', 0)
            self._selector_counter = static_counter + 1
            element_index = self._selector_counter
            # Try with ID first (most reliable)
            if element_info['id']:
                # Remove any quotes from the ID to avoid selector issues
                clean_id = element_info['id'].replace("'", "").replace('"', '')
                return f"#{clean_id}"

            # Try data-testid or similar test attributes which are often used for testing
            for attr in ['data-testid', 'data-cy', 'data-qa']:
                if attr in element_info and element_info[attr]:
                    clean_attr = element_info[attr].replace("'", "").replace('"', '')
                    return f"[{attr}='{clean_attr}']"

            # Try with aria-label (good for accessibility and often unique)
            if element_info.get('aria-label'):
                clean_aria = element_info['aria-label'].replace("'", "").replace('"', '')
                return f"[aria-label='{clean_aria}']"

            # Try with name attribute
            if element_info['name']:
                tag_name = element_info['tag']
                clean_name = element_info['name'].replace("'", "").replace('"', '')
                return f"{tag_name}[name='{clean_name}']"

            # Try with placeholder for inputs
            if element_info.get('placeholder'):
                clean_placeholder = element_info['placeholder'].replace("'", "").replace('"', '')
                return f"[placeholder='{clean_placeholder}']"

            # Try with role attribute
            if element_info.get('role'):
                tag_name = element_info['tag']
                clean_role = element_info['role'].replace("'", "").replace('"', '')
                return f"[role='{clean_role}']"

            # Try with text content if it's not empty
            if element_info['text']:
                # For links and buttons, we can use text-based selectors
                if element_info['tag'] in ['a', 'button'] or element_info.get('type') in ['submit', 'button', 'reset']:
                    # Limit text length for selector to avoid issues with very long text
                    text = element_info['text'][:50].strip()
                    # Skip common text that might match multiple elements
                    if text and text.lower() not in ['follow', 'about', 'blog', 'home', 'contact', 'services', 'login', 'sign up', 'register']:
                        # Make the selector more specific by adding attributes or nth-match
                        if element_info.get('title'):
                            # Use title attribute for more specificity
                            clean_title = element_info['title'].replace("'", "\\'")
                            return f"{element_info['tag']}[title='{clean_title}']"
                        elif element_info.get('href'):
                            # For links with href, use both text and href for specificity
                            clean_href = element_info['href'].replace("'", "\\'")
                            return f"{element_info['tag']}[href='{clean_href}']:has-text('{text}')"
                        else:
                            # Use nth-match to make the selector more specific
                            # This helps avoid ambiguous selectors that match multiple elements
                            element_index = getattr(self, '_selector_counter', 0) % 10 + 1
                            return f"{element_info['tag']}:has-text('{text}'):nth-match({element_index})"
                    elif text:
                        # For common text, always use additional attributes or nth-match
                        element_index = getattr(self, '_selector_counter', 0) % 10 + 1
                        
                        # If we have attributes, use them for more specificity
                        if element_info.get('title'):
                            clean_title = element_info['title'].replace("'", "\\'")
                            return f"{element_info['tag']}[title='{clean_title}']"
                        elif element_info.get('href'):
                            clean_href = element_info['href'].replace("'", "\\'")
                            return f"{element_info['tag']}[href='{clean_href}']"
                        elif element_info.get('class'):
                            classes = element_info['class'].split()
                            if classes:
                                return f"{element_info['tag']}.{classes[0]}:nth-match({element_index})"
                        else:
                            # Last resort: use nth-match with a higher index to avoid conflicts
                            return f"{element_info['tag']}:has-text('{text}'):nth-match({element_index})"

            # Try with href for links
            if element_info['tag'] == 'a' and element_info.get('href'):
                clean_href = element_info['href'].replace("'", "").replace('"', '')
                # Use just the path part if it's a URL
                if '/' in clean_href:
                    path = clean_href.split('/')[-1]
                    if path:
                        return f"a[href*='{path}']"
                else:
                    return f"a[href='{clean_href}']"

            # Try with type for inputs
            if element_info['tag'] == 'input' and element_info['type']:
                input_type = element_info['type'].replace("'", "").replace('"', '')
                # Add more specificity if possible
                if element_info.get('placeholder') or element_info.get('name'):
                    attr_name = 'placeholder' if element_info.get('placeholder') else 'name'
                    attr_value = element_info.get(attr_name, '').replace("'", "").replace('"', '')
                    return f"input[type='{input_type}'][{attr_name}='{attr_value}']"
                return f"input[type='{input_type}']"

            # Special handling for buttons to ensure we catch all of them
            if element_info['tag'] == 'button':
                # First, try aria-label which is often unique and descriptive
                if element_info.get('aria-label'):
                    clean_aria = element_info['aria-label'].replace("'", "").replace('"', '')
                    return f"button[aria-label='{clean_aria}']"

                # For buttons with text, use the text content
                if element_info['text']:
                    text = element_info['text'][:50].strip()
                    return f"button:has-text('{text}')"

                # Get position and parent information
                position = element_info.get('position', 1)
                parent_id = element_info.get('parent_id', '')
                parent_class = element_info.get('parent_class', '')
                has_svg = element_info.get('has_svg', False)
                svg_path = element_info.get('svg_path', '')

                # For buttons with SVG icons, create very specific selectors
                if has_svg:
                    # If we have SVG path data, use it to create a highly specific selector
                    if svg_path:
                        # Create a selector that targets the specific SVG path
                        # This is extremely precise and will only match the exact button
                        return f"button:has(svg path[d^='{svg_path}'])"

                    # If the button has aria-label, use that (most specific)
                    if element_info.get('aria-label'):
                        clean_aria = element_info['aria-label'].replace("'", "").replace('"', '')
                        return f"button[aria-label='{clean_aria}']"

                    # Create a unique selector based on the button's position in its container
                    # Get the button's immediate parent
                    parent_selector = ''

                    # If we have a parent with ID, use that for context
                    if parent_id:
                        parent_selector = f"#{parent_id}"
                    # If we have a parent with class, use that for context
                    elif parent_class:
                        # Clean the class to avoid selector issues
                        clean_parent_class = parent_class.replace("'", "").replace('"', '')
                        parent_selector = f"[class*='{clean_parent_class}']"

                    # If the button itself has a class
                    if element_info['class']:
                        clean_class = element_info['class'].replace("'", "").replace('"', '')
                        # Create a very specific selector with parent context, class, and position
                        if parent_selector:
                            return f"{parent_selector} button[class*='{clean_class}']:has(svg):nth-of-type({position})"
                        else:
                            return f"button[class*='{clean_class}']:has(svg):nth-of-type({position})"

                    # If we have a parent selector, use it with position
                    if parent_selector:
                        return f"{parent_selector} button:has(svg):nth-of-type({position})"

                    # Last resort for SVG buttons - use a more specific approach with exact position
                    return f"button:has(svg):nth-of-type({position})"

                # Try to create a highly specific selector using absolute position information
                absolute_position = element_info.get('absolute_position', [])
                if absolute_position and len(absolute_position) >= 2:
                    # Create a selector that uses the exact DOM path to this button
                    # This is extremely specific and should only match one element
                    path_parts = []
                    for i, (tag, pos) in enumerate(absolute_position):
                        if i == len(absolute_position) - 1:  # Last element (the button itself)
                            path_parts.append(f"{tag}:nth-child({pos})")
                        else:
                            path_parts.append(f"{tag}:nth-child({pos}) >")
                    return " ".join(path_parts)

                # If we have grandparent information, use it to create a more specific selector
                grandparent_tag = element_info.get('grandparent_tag', '')
                grandparent_class = element_info.get('grandparent_class', '')
                grandparent_id = element_info.get('grandparent_id', '')

                if grandparent_id:
                    # Use grandparent ID for a very specific selector
                    parent_tag = element_info.get('parent_tag', '')
                    if parent_tag and element_info['class']:
                        clean_class = element_info['class'].replace("'", "").replace('"', '')
                        return f"#{grandparent_id} > {parent_tag} > button[class*='{clean_class}']:nth-of-type({position})"
                    elif parent_tag:
                        return f"#{grandparent_id} > {parent_tag} > button:nth-of-type({position})"
                    else:
                        return f"#{grandparent_id} button:nth-of-type({position})"

                if grandparent_class and grandparent_tag:
                    # Use grandparent class and tag for a specific selector
                    clean_grandparent_class = grandparent_class.replace("'", "").replace('"', '')
                    parent_tag = element_info.get('parent_tag', '')

                    if parent_tag and parent_class:
                        clean_parent_class = parent_class.replace("'", "").replace('"', '')
                        if element_info['class']:
                            clean_class = element_info['class'].replace("'", "").replace('"', '')
                            return f"{grandparent_tag}[class*='{clean_grandparent_class}'] > {parent_tag}[class*='{clean_parent_class}'] > button[class*='{clean_class}']:nth-of-type({position})"
                        else:
                            return f"{grandparent_tag}[class*='{clean_grandparent_class}'] > {parent_tag}[class*='{clean_parent_class}'] > button:nth-of-type({position})"

                # For buttons with no SVG, try parent context
                # If we have a parent with class, use that for context
                if parent_class:
                    clean_parent_class = parent_class.replace("'", "").replace('"', '')

                    # If the button has a class
                    if element_info['class']:
                        clean_class = element_info['class'].replace("'", "").replace('"', '')

                        # Create a more specific selector using the parent's tag name if available
                        parent_tag = element_info.get('parent_tag', '')
                        if parent_tag:
                            return f"{parent_tag}[class*='{clean_parent_class}'] > button[class*='{clean_class}']:nth-of-type({position})"
                        else:
                            # Use direct child selector to be more specific
                            return f"[class*='{clean_parent_class}'] > button[class*='{clean_class}']:nth-of-type({position})"

                    # Fallback to position-based selector with parent context
                    parent_tag = element_info.get('parent_tag', '')
                    if parent_tag:
                        return f"{parent_tag}[class*='{clean_parent_class}'] > button:nth-of-type({position})"
                    else:
                        # Use direct child selector to be more specific
                        return f"[class*='{clean_parent_class}'] > button:nth-of-type({position})"

                # If the button has a class
                if element_info['class']:
                    clean_class = element_info['class'].replace("'", "").replace('"', '')
                    return f"button[class*='{clean_class}']:nth-of-type({position})"

                # Try to create a unique selector based on available attributes
                attrs = []
                for attr in ['type', 'name', 'title', 'data-testid', 'data-cy', 'data-qa', 'role']:
                    if element_info.get(attr):
                        clean_attr = element_info[attr].replace("'", "").replace('"', '')
                        if clean_attr:
                            attrs.append(f"[{attr}='{clean_attr}']")
                if attrs:
                    return f"button{''.join(attrs)}:nth-of-type({position})"

                # For buttons with event handlers
                if element_info.get('onclick') or element_info.get('onmousedown'):
                    event_attr = 'onclick' if element_info.get('onclick') else 'onmousedown'
                    clean_attr = element_info[event_attr].replace("'", "").replace('"', '')
                    if clean_attr:
                        return f"button[{event_attr}*='{clean_attr}']:nth-of-type({position})"

                # Last resort: use a very specific position-based selector
                # This ensures we don't miss any buttons
                return f"button:nth-of-type({position})"

            # Try with class if it's not too generic
            if element_info['class']:
                tag_name = element_info['tag']
                # Create a more specific selector with tag and class
                classes = element_info['class'].split()
                if len(classes) > 0:
                    # Use the most specific class (usually the longest one)
                    classes.sort(key=len, reverse=True)
                    specific_class = classes[0]
                    return f"{tag_name}[class*='{specific_class}']"

            # For elements with title or alt text
            if element_info.get('title'):
                clean_title = element_info['title'].replace("'", "").replace('"', '')
                return f"[title='{clean_title}']"

            if element_info.get('alt'):
                clean_alt = element_info['alt'].replace("'", "").replace('"', '')
                return f"[alt='{clean_alt}']"

            # For elements with data attributes
            for key in element_info:
                if key.startswith('data-') and key not in ['data-testid', 'data-cy', 'data-qa'] and element_info[key]:
                    clean_value = element_info[key].replace("'", "").replace('"', '')
                    return f"[{key}='{clean_value}']"
            
            # Handle classes more thoroughly if we have them
            if element_info['class']:
                classes = element_info['class'].split()
                if classes:
                    # Find the most specific class (not utility class)
                    for cls in classes:
                        if len(cls) > 3 and not cls.startswith('w-') and not cls.startswith('h-') and not cls.startswith('p-'):
                            return f"{element_info['tag']}.{cls}"
                    # If all classes are utility classes, use the first one
                    return f"{element_info['tag']}.{classes[0]}"

            # Last resort: tag with index
            # This is not ideal but better than nothing
            return f"{element_info['tag']}"

        except Exception as e:
            print(f"Error creating selector: {e}")
            # Absolute last resort - just use the tag name
            return element_info['tag']

    def generate_test_steps(self, elements_by_role):
        """
        Generate test steps based on the elements found.
        """
        test_steps = []

        # Process forms first to identify form elements
        form_elements = set()
        if 'form' in elements_by_role:
            for form in elements_by_role['form']:
                # Add a comment for form testing
                test_steps.append(f"# Testing form with selector {form['selector']}")
                form_elements.add(form['selector'])

        # Process interactive elements by priority
        priority_order = ['input', 'select', 'checkbox', 'radio', 'button', 'link', 'tab', 'menu', 'dialog', 'alert']

        for role in priority_order:
            if role in elements_by_role:
                test_steps.append(f"\n# Testing {role} elements")
                for element in elements_by_role[role]:
                    # Skip if this element is part of a form we'll test later
                    if element['selector'] in form_elements and role != 'form':
                        continue

                    # Create a step for this element
                    action = element['action']
                    # Use repr() to properly escape the selector string
                    selector_str = repr(element['selector'])

                    # Get the template and format it
                    step_template = self.step_templates[action]

                    # For multi-line templates (like click with go_back), we need to indent each line
                    if '\n' in step_template:
                        lines = step_template.split('\n')
                        formatted_lines = [lines[0].format(selector=selector_str)]
                        for line in lines[1:]:
                            formatted_lines.append(line)
                        step = '\n                '.join(formatted_lines)
                    else:
                        step = step_template.format(selector=selector_str)

                    # Add try/except block for robustness
                    display_text = element['text'] if element['text'] else element['selector']
                    # Sanitize display_text to prevent syntax errors in generated code
                    if display_text:
                        # Replace newlines and tabs with spaces
                        display_text = display_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                        # Replace multiple spaces with a single space
                        display_text = ' '.join(display_text.split())
                        # Escape single quotes
                        display_text = display_text.replace("'", "\\'") 
                        # Limit length to prevent overly long strings
                        display_text = display_text[:100] if len(display_text) > 100 else display_text

                    # For elements that should cause navigation, add page change detection
                    if role in ['button', 'link', 'form'] or action == 'click':
                        test_steps.append(f"try:")
                        test_steps.append(f"    print(f'Testing {role}: {display_text}')")
                        test_steps.append(f"    # Take screenshot before interaction")
                        test_steps.append(f"    before_screenshot = take_screenshot(page, '{role}_{len(test_steps)}_before')")
                        test_steps.append(f"    # Record URL and title before interaction")
                        test_steps.append(f"    before_url = page.url")
                        test_steps.append(f"    before_title = page.title()")
                        test_steps.append(f"    # Perform the action")
                        test_steps.append(f"    {step}")
                        test_steps.append(f"    # Check if the page changed (URL or title)")
                        test_steps.append(f"    after_url = page.url")
                        test_steps.append(f"    after_title = page.title()")
                        test_steps.append(f"    page_changed = after_url != before_url or after_title != before_title")
                        test_steps.append(f"    # Take screenshot after interaction")
                        test_steps.append(f"    after_screenshot = take_screenshot(page, '{role}_{len(test_steps)}_after')")
                        test_steps.append(f"    # Record element effectiveness")
                        test_steps.append(f"    element_tracker.record_element_test(")
                        test_steps.append(f"        page_url=original_url,")
                        test_steps.append(f"        element_type='{role}',")
                        test_steps.append(f"        selector={selector_str},")
                        test_steps.append(f"        description='{display_text}',")
                        test_steps.append(f"        success=True,  # We got this far without exception")
                        test_steps.append(f"        screenshot_before=before_screenshot,")
                        test_steps.append(f"        screenshot_after=after_screenshot,")
                        test_steps.append(f"        page_change_detected=page_changed")
                        test_steps.append(f"    )")
                        test_steps.append(f"    # Go back to original URL if page changed")
                        test_steps.append(f"    if page_changed:")
                        test_steps.append(f"        print(f\"Page changed after interaction! New URL: {{after_url}}\")")
                        test_steps.append(f"        page.goto(original_url, timeout=5000)")
                        test_steps.append(f"        try:")
                        test_steps.append(f"            page.wait_for_load_state('networkidle', timeout=5000)")
                        test_steps.append(f"        except Exception as e:")
                        test_steps.append(f"            print(f'Return navigation wait error: {{e}}')")
                    else:
                        # For other elements (inputs, checkboxes, etc.)
                        test_steps.append(f"try:")
                        test_steps.append(f"    print(f'Testing {role}: {display_text}')")
                        test_steps.append(f"    # Take screenshot before interaction")
                        test_steps.append(f"    before_screenshot = take_screenshot(page, '{role}_{len(test_steps)}_before')")
                        test_steps.append(f"    # Perform the action")
                        test_steps.append(f"    {step}")
                        test_steps.append(f"    # Take screenshot after interaction")
                        test_steps.append(f"    after_screenshot = take_screenshot(page, '{role}_{len(test_steps)}_after')")
                        test_steps.append(f"    # Record element effectiveness")
                        test_steps.append(f"    element_tracker.record_element_test(")
                        test_steps.append(f"        page_url=original_url,")
                        test_steps.append(f"        element_type='{role}',")
                        test_steps.append(f"        selector={selector_str},")
                        test_steps.append(f"        description='{display_text}',")
                        test_steps.append(f"        success=True,  # We got this far without exception")
                        test_steps.append(f"        screenshot_before=before_screenshot,")
                        test_steps.append(f"        screenshot_after=after_screenshot")
                        test_steps.append(f"    )")

                    test_steps.append(f"except Exception as e:")
                    test_steps.append(f"    print(f'Error interacting with {role} element: {{e}}')")
                    test_steps.append(f"    # Record failed interaction")
                    test_steps.append(f"    element_tracker.record_element_test(")
                    test_steps.append(f"        page_url=original_url,")
                    test_steps.append(f"        element_type='{role}',")
                    test_steps.append(f"        selector={selector_str},")
                    test_steps.append(f"        description='{display_text}',")
                    test_steps.append(f"        success=False,")
                    test_steps.append(f"        error_message=str(e)")
                    test_steps.append(f"    )")
                    test_steps.append(f"    # Continue with other elements")

        return test_steps

    def generate_test_script(self, url, html, html_file=None):
        """
        Generate a complete Playwright test script for a given URL and HTML.
        """
        # Parse the HTML
        soup = self.optimize_html(html)

        # Extract elements by role
        elements_by_role = self.extract_elements_by_role(soup)

        # If no interactive elements were found, try a more aggressive approach
        if not elements_by_role or sum(len(elements) for elements in elements_by_role.values()) < 3:
            print(f"Few elements detected, trying fallback detection for {url}")
            # Try a more aggressive element detection approach
            fallback_elements = self._fallback_element_detection(soup)
            if fallback_elements:
                elements_by_role.update(fallback_elements)

        # Store information about the HTML file for reference
        html_file_reference = f"# HTML file: {html_file}" if html_file else ""

        # No limits - test all elements
        for role in elements_by_role:
            elements = elements_by_role[role]
            print(f"Testing all {len(elements)} {role} elements")

        # Generate test steps
        test_steps = self.generate_test_steps(elements_by_role)

        # Build the complete test script
        test_script = f"""
# Playwright test for {url}
# Generated using role-based template approach
{html_file_reference}

from playwright.sync_api import sync_playwright
import os
import sys
import time
import traceback
import json
from datetime import datetime

# Add parent directory to path to import ElementTracker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from element_tracker import ElementTracker

def create_screenshot_dir():
    \"\"\"Create screenshots directory if it doesn't exist\"\"\"
    screenshots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    return screenshots_dir

def take_screenshot(page, name):
    \"\"\"Take a screenshot and save it with timestamp\"\"\"
    screenshots_dir = create_screenshot_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{{name}}_{{timestamp}}.png"
    filepath = os.path.join(screenshots_dir, filename)
    page.screenshot(path=filepath)
    print(f"Screenshot saved: {{filepath}}")
    return filepath

def detect_page_change(before_url, after_url, before_title, after_title):
    \"\"\"Detect if the page has changed after an interaction\"\"\"
    url_changed = before_url != after_url
    title_changed = before_title != after_title
    return url_changed or title_changed

def test_page():
    \"\"\"
    Role-based test for {url}
    This test interacts with UI elements based on their roles.
    \"\"\"
    # Create element tracker to record test results
    element_tracker = ElementTracker(output_dir="test_results")

    with sync_playwright() as p:
        browser = None
        try:
            print(f"Starting test for {url}")

            # Launch browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={{"width": 1280, "height": 720}})
            page = context.new_page()

            # Set a longer default timeout to prevent timeout issues
            page.set_default_timeout(30000)

            # Store the original URL for navigation back after clicks
            original_url = "{url}"

            # Navigate to the URL
            print(f"Navigating to {url}")
            page.goto("{url}", timeout=30000, wait_until="networkidle")

            # Take initial screenshot
            initial_screenshot = take_screenshot(page, "initial_page")

            # Basic assertions
            title = page.title()
            print(f"Page title: {{title}}")
            assert title != "", "Page title should not be empty"

            # Execute test steps for each element type
            {chr(10) + chr(32) * 12 + chr(10).join([chr(32) * 12 + line for line in test_steps])}

            print("Test completed successfully")

        except Exception as e:
            print(f"Test failed: {{e}}")
            traceback.print_exc()
            if 'page' in locals():
                take_screenshot(page, "error_state")
            raise
        finally:
            if browser:
                browser.close()

            # Save element tracking results
            results_path = element_tracker.save_results()
            print(f"Element tracking results saved to: {{results_path}}")

            # Print summary
            summary = element_tracker.get_summary()
            print(f"\\nElement Testing Summary:")
            print(f"Total elements tested: {{summary['total']}}")
            print(f"Successfully interacted: {{summary['successful']}} ({{summary['successful']/max(1, summary['total'])*100:.1f}}%)")
            print(f"Working elements: {{summary['working']}} ({{summary['working']/max(1, summary['total'])*100:.1f}}%)")
            print("\\nBy element type:")
            for element_type, stats in summary['by_type'].items():
                print(f"  {{element_type}}: {{stats['working']}}/{{stats['total']}} working ({{stats['working']/max(1, stats['total'])*100:.1f}}%)")

if __name__ == "__main__":
    test_page()
"""
        return test_script

def generate_tests_with_templates(pages, out_dir="generated_tests"):
    """
    Generate Playwright tests for a list of pages using role-based templates.
    """
    os.makedirs(out_dir, exist_ok=True)
    test_scripts = []
    generator = RoleBasedTestGenerator()

    print(f"[Template] Processing {len(pages)} pages")

    for i, page in enumerate(pages):
        print(f"[Template] Processing page {i+1}/{len(pages)}: {page['url']}")

        # Generate the test with template-based approach
        test_code = generator.generate_test_script(
            url=page['url'],
            html=page['html'],
            html_file=page.get('html_file', None)  # Pass the HTML file path if available
        )

        # Save the test script
        script_path = os.path.join(out_dir, f"test_{i}.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(test_code)

        test_scripts.append(script_path)
        print(f"[Template] Test generated for {page['url']} ({i+1}/{len(pages)})")

    print(f"[Template] Generated {len(test_scripts)} test scripts")
    return test_scripts
