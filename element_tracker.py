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
        # Determine if the element is "working" based on its type and behavior
        is_working = success  # By default, if we can interact with it, it's working

        # For links, we need a more flexible approach
        if element_type == 'link' and success:
            # Consider links working by default if they can be clicked successfully
            is_working = True

            # Links that contain "#" are anchor links that don't change the page
            if "#" in description or (selector and "#" in selector):
                is_working = True  # Anchor links are considered working if interaction succeeded

            # Links with certain text patterns are expected to navigate
            navigation_indicators = ['login', 'sign', 'register', 'checkout', 'buy',
                                    'purchase', 'download', 'upload', 'submit']

            # Check if link description suggests it should navigate
            should_navigate = any(indicator in description.lower() for indicator in navigation_indicators) if description else False

            # If the link should navigate but didn't change the page, mark it as not working
            if should_navigate and not page_change_detected:
                is_working = False

        # For buttons, consider them working if:
        # 1. They caused a page change, OR
        # 2. They were successfully clicked (might trigger JS actions without page change)
        if element_type == 'button' and success:
            # Some buttons are expected to navigate
            navigation_indicators = ['login', 'sign', 'submit', 'continue', 'next', 'previous',
                                    'back', 'proceed', 'checkout', 'buy', 'purchase', 'register']

            # Check if button description suggests it should navigate
            should_navigate = any(indicator in description.lower() for indicator in navigation_indicators) if description else False

            if should_navigate:
                # For buttons that should navigate, check if page changed
                is_working = page_change_detected
            else:
                # For other buttons, consider them working if interaction succeeded
                is_working = True

        # For forms, we expect page changes or form submissions
        if element_type == 'form' and success:
            is_working = page_change_detected

        # For inputs, checkboxes, etc., success means they're working
        if element_type in ['input', 'checkbox', 'radio', 'select'] and success:
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
