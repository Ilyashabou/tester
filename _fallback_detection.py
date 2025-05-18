def _fallback_element_detection(self, soup):
    """
    More aggressive element detection for pages where standard detection finds few elements.
    This method tries to find any potentially interactive elements on the page.
    """
    fallback_elements = {}
    
    try:
        # Find all elements with onclick attributes or event handlers
        onclick_elements = soup.select('[onclick], [onmousedown], [onmouseup], [onmouseover]')
        if onclick_elements:
            fallback_elements['clickable'] = []
            for element in onclick_elements[:10]:  # Limit to 10 elements
                element_info = {
                    'tag': element.name,
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                    'text': element.get_text().strip(),
                    'action': 'click',
                    'selector': None
                }
                element_info['selector'] = self._create_selector_for_element(element_info)
                if element_info['selector']:
                    fallback_elements['clickable'].append(element_info)
        
        # Find all elements that look like they might be interactive based on class names
        interactive_classes = soup.select('[class*="btn"], [class*="button"], [class*="link"], [class*="nav"], [class*="menu"], [class*="click"], [class*="select"]')
        if interactive_classes:
            if 'clickable' not in fallback_elements:
                fallback_elements['clickable'] = []
            for element in interactive_classes[:10]:  # Limit to 10 elements
                # Skip if already added via onclick
                if any(e.get('id') == element.get('id') for e in fallback_elements.get('clickable', []) if e.get('id')):
                    continue
                element_info = {
                    'tag': element.name,
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                    'text': element.get_text().strip(),
                    'action': 'click',
                    'selector': None
                }
                element_info['selector'] = self._create_selector_for_element(element_info)
                if element_info['selector']:
                    fallback_elements['clickable'].append(element_info)
        
        # Find all elements with tabindex
        tabindex_elements = soup.select('[tabindex]:not([tabindex="-1"])')
        if tabindex_elements:
            if 'focusable' not in fallback_elements:
                fallback_elements['focusable'] = []
            for element in tabindex_elements[:5]:  # Limit to 5 elements
                element_info = {
                    'tag': element.name,
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                    'text': element.get_text().strip(),
                    'action': 'click',
                    'selector': None
                }
                element_info['selector'] = self._create_selector_for_element(element_info)
                if element_info['selector']:
                    fallback_elements['focusable'].append(element_info)
        
        # As a last resort, find elements that have hover effects (might be interactive)
        hover_elements = soup.select('[class*="hover"]')
        if hover_elements and not fallback_elements:
            fallback_elements['hover'] = []
            for element in hover_elements[:5]:  # Limit to 5 elements
                element_info = {
                    'tag': element.name,
                    'id': element.get('id', ''),
                    'class': ' '.join(element.get('class', [])) if element.get('class') else '',
                    'text': element.get_text().strip(),
                    'action': 'click',
                    'selector': None
                }
                element_info['selector'] = self._create_selector_for_element(element_info)
                if element_info['selector']:
                    fallback_elements['hover'].append(element_info)
                    
        return fallback_elements
    except Exception as e:
        print(f"Error in fallback element detection: {e}")
        return {}
