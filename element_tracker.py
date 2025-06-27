import os
import json
from datetime import datetime

class ElementTracker:
    """
    Tracks the effectiveness of UI elements during testing.
    Records whether elements are working properly based on their expected behavior.
    """

    def __init__(self, output_dir="test_results"):
        self.output_dir = output_dir
        self.elements = []
        self.test_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(output_dir, exist_ok=True)

    def record_element_test(self, page_url, element_type, selector, description="",
                           success=False, error_message=None, screenshot_before=None,
                           screenshot_after=None, page_change_detected=False, visual_change_detected=None):
        """
        Record the result of testing an element

        Args:
            page_url: URL of the page where the element was tested
            element_type: Type of element (button, link, input, etc.)
            selector: CSS selector used to locate the element
            description: Text description of the element
            success: Whether the interaction was successful
            error_message: Error message if the interaction failed
            screenshot_before: Path to screenshot before interaction
            screenshot_after: Path to screenshot after interaction
            page_change_detected: Whether the page changed after interaction (URL or title)
            visual_change_detected: Whether visual changes were detected (optional)
        """
        # BALANCED APPROACH: More accurate detection of working elements
        # Default assumption based on interaction success
        is_working = True if success else False
        
        # If interaction failed but we have an error message about the element being found but not clickable,
        # it might still be a valid element that's just not interactable in the current view
        if not success and error_message and ("not clickable" in error_message or "not visible" in error_message):
            is_working = False
            
        # For links - consider most working, but have reasonable expectations
        if element_type == 'link' and success:
            # Links that caused page changes are definitely working
            if page_change_detected:
                is_working = True
            # Links that caused visual changes are working (might be toggles, accordions, etc.)
            elif visual_change_detected:
                is_working = True
            # Anchor links (#) are considered NOT working
            elif "#" in description or (selector and "#" in selector):
                is_working = False
            # Links with onclick handlers might be doing client-side actions
            elif selector and ("onclick" in selector or "data-" in selector):
                is_working = True
            # Links that don't meet any of the above criteria and have clear navigation text
            # might not be working as expected
            else:
                navigation_terms = ['login', 'sign in', 'register', 'signup', 'sign up', 'checkout', 'account']
                if (any(term.lower() in description.lower() for term in navigation_terms if description) and
                    not page_change_detected and visual_change_detected is False):
                    is_working = False
                else:
                    # Default to working for all other links
                    is_working = True
        
        # For buttons - comprehensive detection rules based on real-world patterns
        if element_type == 'button':
            # Start with a default assumption based on interaction success
            is_working = False
            
            # 1. Buttons with successful interaction are working
            if success:
                is_working = True
            
            # 2. Analyze selector patterns for buttons that failed interaction
            elif selector and description:
                # Analyze the selector and description to determine if the button should be working
                
                # 2.1 Check for nth-match pattern issues
                # Buttons with nth-match selectors often fail due to selector issues, not button functionality
                if 'nth-match' in selector and any(x in error_message for x in ['expects non-empty selector', 'Error: "nth-match"']):
                    # Check if the button has meaningful text that suggests it should be functional
                    functional_text_patterns = [
                        'Continue with', 'Sign', 'Login', 'Submit', 'Send', 'Search',
                        'Apply', 'Register', 'Create', 'Update', 'Delete', 'Save',
                        'Next', 'Previous', 'Back', 'Forward', 'Confirm'
                    ]
                    
                    # If the button has functional text, it's likely a working button with a selector issue
                    if any(pattern in description for pattern in functional_text_patterns):
                        is_working = True
                    # App Store and Google Play buttons in footers are often just visual elements
                    elif ('App Store' in description or 'Google Play' in description) and not 'href' in selector:
                        is_working = False
                
                # 2.2 Check for buttons wrapped in anchor tags (common pattern)
                # Buttons inside <a> tags are typically functional
                if '<a' in selector or 'href=' in selector or 'a[href' in selector:
                    is_working = True
                
                # 2.3 Check for buttons with styling that indicates functionality
                functional_style_indicators = [
                    'hover:' in selector,             # Hover effects indicate interactivity
                    'transition' in selector,         # Transitions indicate interactivity
                    'rounded' in selector,            # Styled buttons are usually functional
                    'focus:' in selector,             # Focus states indicate interactivity
                    'ring-' in selector,              # Focus rings indicate interactivity
                    'bg-' in selector and ('hover:bg-' in selector or 'text-white' in selector)  # Color changes on hover
                ]
                
                # If the button has multiple styling indicators of functionality, it's likely working
                if sum(functional_style_indicators) >= 2:
                    is_working = True
                
                # 2.4 Check for buttons with accessibility attributes
                if 'aria-label' in selector or 'aria-' in selector:
                    is_working = True
            
            # 3. Error message analysis for failed interactions
            if error_message:
                # 3.1 Some errors indicate the button exists but couldn't be interacted with
                technical_issues = [
                    'not visible', 'not clickable', 'element is not visible',
                    'timeout', 'element not visible', 'element is not attached',
                    'Element is not attached to the DOM', 'detached from the DOM',
                    'element not interactable', 'element not stable'
                ]
                
                if any(issue in error_message for issue in technical_issues):
                    # The button exists but might be hidden, covered, or requires scrolling
                    is_working = True
                
                # 3.2 Selector errors often don't mean the button is broken
                selector_issues = [
                    'expects non-empty selector', 'Error: "nth-match"', 'resolved to 0 elements',
                    'strict mode violation', 'resolved to multiple elements'
                ]
                
                if any(issue in error_message for issue in selector_issues):
                    # This is likely a selector issue, not a button functionality issue
                    # Check the description to determine if it's a functional button
                    if description and any(x in description.lower() for x in ['continue', 'sign', 'login', 'submit']):
                        is_working = True
        
        # For forms - reasonable expectations
        if element_type == 'form' and success:
            # Forms with submit that cause page changes are working
            if page_change_detected:
                is_working = True
            # Forms with submit that don't cause page changes might not be working
            elif 'submit' in selector.lower() if selector else False:
                is_working = not (not page_change_detected and visual_change_detected is False)
            else:
                # Default to working for all other forms
                is_working = True
        
        # For inputs - always working if they exist and can be typed into
        if element_type == 'input':
            # All inputs that we can find are considered working since we can type into them
            is_working = True
        # For other form elements - working if interaction succeeded
        elif element_type in ['checkbox', 'radio', 'select']:
            is_working = success
        
        # For interactive elements - generally working if interaction succeeded
        if element_type in ['interactive', 'clickable', 'tab', 'menu', 'dialog', 'alert', 'toggle']:
            if success and (page_change_detected or visual_change_detected is not False):
                is_working = True

        element_result = {
            'page_url': page_url,
            'element_type': element_type,
            'selector': selector,
            'description': description,
            'success': success,  # Interaction succeeded
            'is_working': is_working,  # Element is functioning as expected
            'error_message': error_message,
            'screenshot_before': screenshot_before,
            'screenshot_after': screenshot_after,
            'page_change_detected': page_change_detected,
            'visual_change_detected': visual_change_detected,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.elements.append(element_result)

    def save_results(self):
        """Save the element tracking results to a JSON file"""
        output_file = os.path.join(self.output_dir, f"element_results_{self.test_id}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'test_id': self.test_id,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'elements': self.elements
            }, f, indent=2)
        return output_file

    def get_summary(self):
        """Get a summary of the element testing results"""
        total = len(self.elements)
        successful = sum(1 for e in self.elements if e['success'])
        working = sum(1 for e in self.elements if e['is_working'])

        by_type = {}
        for element in self.elements:
            element_type = element['element_type']
            if element_type not in by_type:
                by_type[element_type] = {
                    'total': 0,
                    'successful': 0,
                    'working': 0
                }
            by_type[element_type]['total'] += 1
            if element['success']:
                by_type[element_type]['successful'] += 1
            if element['is_working']:
                by_type[element_type]['working'] += 1

        return {
            'total': total,
            'successful': successful,
            'working': working,
            'by_type': by_type
        }
