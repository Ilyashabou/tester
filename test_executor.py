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

                # Modify the code to run in non-headless mode and add delays
                modified_code = original_code.replace(
                    "browser = p.chromium.launch(headless=True)",
                    "browser = p.chromium.launch(headless=False)"
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
                spec = importlib.util.spec_from_file_location("test_module", temp_path)
                test_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(test_module)

                # Run the test
                test_module.test_page()
                success = True
                output = "Test ran in visual mode"

                # Clean up the temporary file
                os.remove(temp_path)

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
                # Run the test script
                result = subprocess.run(["python", script], capture_output=True, text=True, timeout=120)
                success = result.returncode == 0
                output = result.stdout + "\n" + result.stderr
            except Exception as e:
                success = False
                output = str(e)

        # Find element tracking results
        element_results = []
        element_results_files = glob.glob(os.path.join(out_dir, "element_results_*.json"))
        if element_results_files:
            try:
                with open(element_results_files[0], 'r', encoding='utf-8') as f:
                    element_data = json.load(f)
                    element_results = element_data.get('elements', [])
            except Exception as e:
                print(f"Error loading element results: {e}")

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