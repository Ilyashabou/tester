import os
import json
import logging
from session_manager import session_manager

logging.basicConfig(level=logging.DEBUG)

print('Session file exists:', os.path.exists('auth_sessions/session_state.json'))

# Check session data directly from file
try:
    with open('auth_sessions/session_state.json', 'r') as f:
        data = json.load(f)
    print('Domain in session:', data.get('domain'))
    print('Number of cookies:', len(data.get('cookies', [])))
    print('localStorage keys:', list(data.get('localStorage', {}).keys()))
except Exception as e:
    print(f'Error reading session file directly: {e}')

# Check session data from session_manager
print('\nSession data from session_manager:')
print('Session file path:', session_manager.session_file)
print('Domain in session_manager:', session_manager.session_data.get('domain'))
print('Number of cookies in session_manager:', len(session_manager.session_data.get('cookies', [])))
print('localStorage keys in session_manager:', list(session_manager.session_data.get('localStorage', {}).keys()))