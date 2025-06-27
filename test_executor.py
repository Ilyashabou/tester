import subprocess
import os
import sys
import importlib.util
import json
import glob
from pathlib import Path
import time

def execute_tests(test_scripts, out_dir="test_results", visual_mode=False):
    os.makedirs(out_dir, exist_ok=True)
    results = []

    for script in test_scripts:
        script_name = Path(script).stem
        screenshot_path = os.path.join(out_dir, f"{script_name}_after.png")

        # Clear any previous element tracking results
        for old_result in glob.glob(os.path.join(out_dir, "element_results_*.json")):
            try:
                os.remove(old_result)
            except:
                pass

        if visual_mode:
            # Run in visual mode - modify the script to run with headless=False
            try:
                # Load the test file
                test_path = os.path.abspath(script)

                # Read the original code
                with open(test_path, 'r', encoding='utf-8') as f:
                    original_code = f.read()

                # Modify the code to run in non-headless mode with comprehensive security disabling and add delays
                modified_code = original_code.replace(
                    "browser = p.chromium.launch(headless=True",
                    "browser = p.chromium.launch(headless=False"
                )
                
                # Add delays between actions for better visibility
                modified_code = modified_code.replace(
                    "# Continue with other elements",
                    "# Continue with other elements\n                time.sleep(1)  # Add delay for visibility"
                )

                # Write to a temporary file
                temp_path = test_path.replace('.py', '_visual.py')
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(modified_code)

                # Run the modified test directly (not using subprocess to see output in real-time)
                print(f"\nRunning test visually: {script_name}")
                print("Press Ctrl+C to stop the test and continue to the next one.\n")

                # Load and run the modified module
                try:
                    spec = importlib.util.spec_from_file_location("test_module", temp_path)
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)

                    # Run the test
                    test_module.test_page()
                    success = True
                    output = "Test ran in visual mode"
                except Exception as e:
                    success = False
                    output = f"Error running test visually: {str(e)}"
                    import traceback
                    output += "\n" + traceback.format_exc()

                # Don't remove the temporary file so it can be inspected if needed
                # os.remove(temp_path)

            except KeyboardInterrupt:
                print("\nTest stopped by user. Moving to next test...")
                success = False
                output = "Test stopped by user"
            except Exception as e:
                success = False
                output = f"Error running test visually: {str(e)}"
                import traceback
                output += "\n" + traceback.format_exc()
        else:
            # Run in normal mode (headless)
            try:
                # Create a modified version of the test script that explicitly calls save_results()
                with open(script, 'r', encoding='utf-8') as f:
                    original_code = f.read()
                
                # Check if the script already has a call to save_results()
                if 'element_tracker.save_results()' not in original_code:
                    # Add explicit call to save_results() before any return statements
                    modified_code = original_code.replace(
                        'return',
                        'element_tracker.save_results()\n    return'
                    )
                    
                    # Also add it at the end of the test_page function in case there's no return
                    modified_code = modified_code.replace(
                        'def test_page():\n',
                        'def test_page():\n    try:\n'
                    )
                    modified_code = modified_code.replace(
                        'with sync_playwright() as p:',
                        'with sync_playwright() as p:\n        try:'
                    )
                    
                    # Add a finally block to ensure save_results is called
                    if 'finally:' not in modified_code:
                        modified_code += "\n        finally:\n            try:\n                element_tracker.save_results()\n            except Exception as save_error:\n                print(f'Error saving element results: {save_error}')\n"
                    
                    # Write the modified script
                    temp_script = script.replace('.py', '_with_save.py')
                    with open(temp_script, 'w', encoding='utf-8') as f:
                        f.write(modified_code)
                    
                    # Use the modified script
                    script_to_run = temp_script
                else:
                    script_to_run = script
                
                # Run the test script
                print(f"Running test script: {script_to_run}")
                
                # Instead of using subprocess, load and run the module directly like in visual mode
                # This ensures the ElementTracker instance is in the same process
                try:
                    print("Loading test module directly to ensure element tracking works properly")
                    spec = importlib.util.spec_from_file_location("test_module", script_to_run)
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    
                    # Run the test
                    test_module.test_page()
                    success = True
                    output = "Test ran successfully in direct execution mode"
                except Exception as direct_error:
                    print(f"Error in direct execution: {direct_error}")
                    # Fall back to subprocess if direct execution fails
                    result = subprocess.run(["python", script_to_run], capture_output=True, text=True, timeout=180)
                    success = result.returncode == 0
                    output = result.stdout + "\n" + result.stderr
                
                # Clean up temporary script
                if script_to_run != script and os.path.exists(script_to_run):
                    try:
                        os.remove(script_to_run)
                    except:
                        pass
                        
            except Exception as e:
                success = False
                output = str(e)

        # Find element tracking results
        element_results = []
        element_results_files = glob.glob(os.path.join(out_dir, "element_results_*.json"))
        
        # Debug output to help diagnose issues
        print(f"Looking for element results in: {out_dir}")
        print(f"Found {len(element_results_files)} element results files: {element_results_files}")
        
        if element_results_files:
            try:
                # Sort by modification time to get the most recent file
                element_results_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                latest_file = element_results_files[0]
                print(f"Loading element results from: {latest_file}")
                
                with open(latest_file, 'r', encoding='utf-8') as f:
                    element_data = json.load(f)
                    element_results = element_data.get('elements', [])
                    print(f"Loaded {len(element_results)} element results")
            except Exception as e:
                print(f"Error loading element results: {e}")
        else:
            print("No element results files found. Check if element_tracker.save_results() is being called.")

        # Add result
        results.append({
            "script": script,
            "success": success,
            "output": output,
            "screenshot": screenshot_path if os.path.exists(screenshot_path) else None,
            "element_results": element_results,
            "url": get_url_from_script(script)
        })

    return results

def get_url_from_script(script_path):
    """Extract the URL from a test script"""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "original_url =" in line:
                    url = line.split("=")[1].strip().strip('"').strip("'")
                    return url
    except:
        pass
    return "Unknown URL"