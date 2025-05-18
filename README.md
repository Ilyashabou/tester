# Role-Based UI WebApp Tester

This project crawls a web app, takes screenshots, uses a role-based template approach to generate Playwright tests, executes them, and produces a report with screenshots and results.

## Features

- Optimized HTML processing for faster test generation
- Removes unnecessary elements (scripts, styles, comments) before analysis
- Uses a role-based approach to identify UI elements and generate appropriate test actions
- Generates robust selectors based on element attributes (id, data-testid, name, etc.)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## Usage

```bash
python main.py <base_url>
```

- Example:
  ```bash
  python main.py https://master.d2l4isn05opwbv.amplifyapp.com/
  ```

## Output
- Screenshots: `screenshots/`
- Generated tests: `generated_tests/`
- Test results: `test_results/`
- HTML report: `report.html`

## TODO
- Improve test step coverage
- Add live progress UI (FastAPI/Flask)
- Add support for more AI models
- Enhance error handling and recovery