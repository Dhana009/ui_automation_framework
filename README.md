# UI Automation Framework - Playwright

Production-grade UI automation framework built with Playwright and Pytest.

**Features:**
- ✅ Scalable to 500+ tests
- ✅ Parallel execution (4-8 workers)
- ✅ Self-healing (waits, retries, recovery)
- ✅ Multi-environment support (dev, qa, prod)
- ✅ Comprehensive reporting (HTML + Slack)
- ✅ Flaky test detection and quarantine

---

## **Quick Start**

### **1. Clone and Setup**
```bash
git clone <repository>
cd ui_automation_framework
pip install -r requirements.txt
playwright install
```

### **2. Run Tests Locally**
```bash
# All tests with 4 workers
pytest tests/ -n 4

# Only smoke tests
pytest tests/ -m smoke

# Specific environment
ENV=qa pytest tests/ -n 4

# View report
open reports/report.html
```

### **3. Run in CI/CD**
```bash
# GitHub Actions handles this automatically
# See .github/workflows/test.yml
```

---

## **Project Structure**

```
ui-automation/
├── tests/              # Test cases (organized by type)
│   ├── smoke/         # Quick 2-3 min tests
│   ├── regression/    # Full regression suite
│   └── e2e/          # End-to-end workflows
├── pages/             # Page Object Model
│   ├── base_page.py  # Common methods
│   ├── components/   # Reusable UI components
│   └── page_objects/ # Individual pages
├── fixtures/          # Pytest fixtures
├── config/            # Environment configs
├── data/              # Test data + factories
├── utils/             # Helper functions
├── conftest.py        # Pytest setup
└── pytest.ini         # Pytest config
```

---

## **Running Different Test Suites**

```bash
# Smoke tests (fast feedback)
pytest tests/ -m "smoke and parallel" -n 4

# Full regression
pytest tests/ -n 4

# Only critical tests
pytest tests/ -m critical -n 8

# Sequential tests only
pytest tests/ -m sequential

# Single test debug
pytest tests/smoke/test_login.py::test_user_login -v -s
```

---

## **Documentation**

- `docs/FRAMEWORK_REFERENCE.md` - Detailed technical reference
- `PROBLEMS_AND_SOLUTIONS.md` - Quick problem lookup
- `ARCHITECTURE_DECISIONS.md` - Design decisions and rationale

---

## **Key Concepts**

### **Explicit Waits (Not Sleep)**
```python
page.wait_for_selector("button", timeout=10000)
```

### **Reuse Browser (Not New Per Test)**
- Fixture scope="module" in parallel
- 500 tests = 4 browsers (not 500!)

### **Unique Data (Factories)**
```python
user = user_factory.create_user()  # Unique per test
```

### **Always Re-locate Elements**
```python
page.click("button")  # Fresh locate every time
```

---

## **CI/CD Setup**

### **GitHub Actions**
```yaml
# Tests run on push/PR
# Automatic reporting
# Slack notifications on failure
```

### **Local Development**
```bash
ENV=dev pytest tests/
# HTML report opens automatically
```

---

## **Troubleshooting**

**Tests are flaky?**
- Add explicit waits
- Check for stale elements
- Add retry logic

**Tests are slow?**
- Check browser reuse (scope="module")
- Reduce workers if resource constrained

**Tests interfere?**
- Add cleanup in fixtures
- Use factories for unique data

---

## **Contributing**

1. Create feature branch
2. Write tests with POM pattern
3. Use markers (@pytest.mark.smoke, etc.)
4. Run: `pytest tests/ -n 4`
5. Submit PR

---

## **Support**

For framework questions, see `FRAMEWORK_REFERENCE.md`
For common problems, see `PROBLEMS_AND_SOLUTIONS.md`

---

**Status:** ✅ Production Ready
**Last Updated:** 2024
**Maintainer:** QA Team

