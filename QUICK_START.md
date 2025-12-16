# Quick Start Guide

Get the framework running in 5 minutes.

---

## **🚀 LOCAL SETUP (5 minutes)**

### **1. Clone Repository**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd ui_automation_framework
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Install Playwright Browsers**
```bash
playwright install
```

### **4. Run Tests Locally**
```bash
# Run smoke tests (Playwright docs website)
pytest tests/smoke/test_playwright_docs.py -v

# Run with HTML report
pytest tests/smoke/test_playwright_docs.py -v --html=reports/report.html

# Run with 4 workers (parallel)
pytest tests/smoke/test_playwright_docs.py -v -n 4

# Run all tests
pytest tests/ -v
```

### **5. View Report**
```bash
# Report opens automatically or navigate to:
reports/report.html
```

---

## **☁️ GITHUB ACTIONS SETUP (3 steps)**

### **1. Push to GitHub**
```bash
git add .
git commit -m "Framework ready"
git push origin main
```

### **2. GitHub Actions Runs Automatically**
- Go to `Actions` tab
- See workflow running
- Wait for completion

### **3. Download Results**
- Click workflow run
- Download `test-reports` artifact
- Open HTML report

---

## **📝 COMMON COMMANDS**

```bash
# Run specific test file
pytest tests/smoke/test_playwright_docs.py -v

# Run specific test
pytest tests/smoke/test_playwright_docs.py::TestPlaywrightDocs::test_docs_page_loads -v

# Run with markers
pytest tests/ -m smoke -v
pytest tests/ -m "smoke and parallel" -v

# Run parallel (4 workers)
pytest tests/ -n 4 -v

# Run with timeout (1 minute)
pytest tests/ --timeout=60 -v

# Stop on first failure
pytest tests/ -x -v

# Verbose output
pytest tests/ -vv

# Show print statements
pytest tests/ -s

# Run tests matching pattern
pytest tests/ -k "test_docs" -v

# Generate report
pytest tests/ --html=reports/report.html --self-contained-html
```

---

## **🎯 NEXT: CUSTOMIZE FOR YOUR WEBSITE**

### **Step 1: Create New Page Object**
```python
# pages/page_objects/my_app_page.py
from pages.base_page import BasePage

class MyAppPage(BasePage):
    # Define selectors
    LOGIN_BUTTON = "button[data-testid='login']"
    USERNAME_INPUT = "input[name='username']"
    
    def __init__(self, page):
        super().__init__(page)
    
    def login(self, username, password):
        self.fill_text(self.USERNAME_INPUT, username)
        # ... more steps
```

### **Step 2: Create Test**
```python
# tests/smoke/test_my_app.py
import pytest
from pages.page_objects.my_app_page import MyAppPage

@pytest.mark.smoke
class TestMyApp:
    def test_login(self, page):
        app = MyAppPage(page)
        app.goto("https://myapp.com")
        app.login("user@example.com", "password")
```

### **Step 3: Run Tests**
```bash
pytest tests/smoke/test_my_app.py -v
```

---

## **📚 DOCUMENTATION**

- `FRAMEWORK_REFERENCE.md` - Complete reference guide
- `PROBLEMS_AND_SOLUTIONS.md` - Quick problem lookup
- `GITHUB_ACTIONS_SETUP.md` - CI/CD guide
- `README.md` - Project overview

---

## **✅ VERIFY EVERYTHING WORKS**

Run this to verify framework:
```bash
# 1. Check imports
python -c "from pages.base_page import BasePage; print('✓ Framework OK')"

# 2. Run sample tests
pytest tests/smoke/test_playwright_docs.py -v

# 3. Check reports generated
ls reports/report.html
```

---

## **🎓 FRAMEWORK STRUCTURE**

```
ui_automation_framework/
├── tests/                  # Test suites
│   ├── smoke/
│   ├── regression/
│   └── e2e/
├── pages/                  # Page Object Model
│   ├── base_page.py
│   ├── components/
│   └── page_objects/
├── fixtures/              # Pytest fixtures
├── config/                # Configuration
├── utils/                 # Utilities (waits, assertions, etc.)
├── data/                  # Test data & factories
├── conftest.py           # Pytest setup
├── pytest.ini            # Pytest config
└── requirements.txt      # Dependencies
```

---

## **💡 TIPS**

1. **Always use explicit waits** (not sleep)
2. **Use BasePage methods** (click, fill_text, wait_for_element)
3. **Create factories** for unique test data
4. **Use markers** to organize tests
5. **Check logs** for debugging
6. **Take screenshots** on failure (automatic)

---

## **❓ NEED HELP?**

- Check `PROBLEMS_AND_SOLUTIONS.md`
- Check logs in `reports/` and `screenshots/`
- Review sample tests in `tests/smoke/`
- Check GitHub Actions logs

---

**Framework is ready! Start testing! 🚀**

