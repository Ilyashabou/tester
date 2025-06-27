import os
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

class SessionManager:
    """Manages browser sessions for authenticated testing"""
    
    def __init__(self, session_dir="auth_sessions"):
        """Initialize the session manager
        
        Args:
            session_dir: Directory to store session data
        """
        self.session_dir = session_dir
        self.session_file = os.path.join(session_dir, "session_state.json")
        
        # Create the session directory if it doesn't exist
        os.makedirs(session_dir, exist_ok=True)
        
        # Initialize empty session data
        self.session_data = {
            "cookies": [],
            "localStorage": {},
            "sessionStorage": {},
            "domain": None,
            "last_updated": None
        }
        
        # Load existing session if available
        self._load_session()
    
    def _load_session(self):
        """Load session data from file if it exists"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    self.session_data = json.load(f)
                logging.info(f"Loaded existing session for domain: {self.session_data.get('domain')}")
            except Exception as e:
                logging.error(f"Error loading session data: {e}")
    
    def save_session(self, page, domain=None):
        """Save the current browser session
        
        Args:
            page: Playwright page object with active session
            domain: Domain for this session (optional)
        """
        try:
            # Get cookies
            cookies = page.context.cookies()
            
            # Get localStorage and sessionStorage using JavaScript
            local_storage = page.evaluate("() => { let items = {}; for (let i = 0; i < localStorage.length; i++) { const key = localStorage.key(i); items[key] = localStorage.getItem(key); } return items; }")
            session_storage = page.evaluate("() => { let items = {}; for (let i = 0; i < sessionStorage.length; i++) { const key = sessionStorage.key(i); items[key] = sessionStorage.getItem(key); } return items; }")
            
            # Get domain from page URL if not provided
            if not domain:
                url = page.url
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
            
            # Update session data
            self.session_data = {
                "cookies": cookies,
                "localStorage": local_storage,
                "sessionStorage": session_storage,
                "domain": domain,
                "last_updated": self._get_timestamp()
            }
            
            # Save to file
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2)
            
            logging.info(f"Saved authenticated session for domain: {domain}")
            return True
        except Exception as e:
            logging.error(f"Error saving session: {e}")
            return False
    
    def load_session(self, context, url=None):
        """Load saved session into a browser context
        
        Args:
            context: Playwright browser context to load session into
            url: URL to check domain compatibility (optional)
            
        Returns:
            bool: True if session was loaded successfully
        """
        # Check if we have any session data (cookies OR localStorage tokens)
        has_cookies = len(self.session_data.get("cookies", [])) > 0
        has_tokens = 'access_token' in self.session_data.get("localStorage", {})
        
        if not (has_cookies or has_tokens):
            logging.warning("No saved session available")
            return False
        
        try:
            # Check if the URL's domain matches the session domain
            if url:
                from urllib.parse import urlparse
                current_domain = urlparse(url).netloc
                session_domain = self.session_data.get("domain")
                
                if current_domain != session_domain:
                    logging.warning(f"Domain mismatch: Session is for {session_domain}, but trying to use with {current_domain}")
                    # Continue anyway, as some cookies might still be valid
            
            # Add cookies to context if available
            if has_cookies:
                context.add_cookies(self.session_data.get("cookies", []))
                logging.info(f"Loaded {len(self.session_data.get('cookies', []))} cookies from saved session")
            
            # If we have localStorage tokens but no cookies, we'll still return True
            # and rely on apply_storage to set the tokens
            if has_tokens:
                logging.info("Session has authentication tokens in localStorage")
            
            return True
        except Exception as e:
            logging.error(f"Error loading session: {e}")
            return False
    
    def apply_storage(self, page):
        """Apply localStorage and sessionStorage to a page
        
        Args:
            page: Playwright page object to apply storage to
            
        Returns:
            bool: True if storage was applied successfully
        """
        try:
            # Set localStorage items
            local_storage = self.session_data.get("localStorage", {})
            if local_storage:
                script = ""
                for key, value in local_storage.items():
                    # Properly escape single quotes in the value
                    escaped_value = value.replace("'", "\\'") if isinstance(value, str) else value
                    script += f"localStorage.setItem('{key}', '{escaped_value}');\n"
                page.evaluate(f"() => {{ {script} }}")
            
            # Set sessionStorage items
            session_storage = self.session_data.get("sessionStorage", {})
            if session_storage:
                script = ""
                for key, value in session_storage.items():
                    # Properly escape single quotes in the value
                    escaped_value = value.replace("'", "\\'") if isinstance(value, str) else value
                    script += f"sessionStorage.setItem('{key}', '{escaped_value}');\n"
                page.evaluate(f"() => {{ {script} }}")
            
            logging.info(f"Applied {len(local_storage)} localStorage items and {len(session_storage)} sessionStorage items")
            return True
        except Exception as e:
            logging.error(f"Error applying storage: {e}")
            return False
    
    def _get_timestamp(self):
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def clear_session(self):
        """Clear the current session data"""
        self.session_data = {
            "cookies": [],
            "localStorage": {},
            "sessionStorage": {},
            "domain": None,
            "last_updated": None
        }
        
        # Remove the session file if it exists
        if os.path.exists(self.session_file):
            try:
                os.remove(self.session_file)
                logging.info("Session data cleared")
            except Exception as e:
                logging.error(f"Error removing session file: {e}")

# Create a singleton instance for easy import
session_manager = SessionManager()