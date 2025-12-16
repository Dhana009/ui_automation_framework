# UI Automation Framework - Playwright

Production-grade UI automation framework template built with Playwright and Pytest.

**Status:** ✅ **READY TO CLONE AND USE**

> This is a **template framework** - Clone it and start building tests for your application immediately!

---

## **⚡ Quick Start (5 minutes)**

See `QUICK_START.md` for complete setup guide.

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install

# 2. Run tests
pytest tests/smoke/test_playwright_docs.py -v

# 3. View report
open reports/report.html
```

---

## **📚 Documentation**

| Document | Purpose |
|----------|---------|
| **SETUP_NEW_PROJECT.md** | 🚀 **START HERE** - Clone and customize for your app |
| **QUICK_START.md** | 5-minute setup guide |
| **DOCKER_SETUP.md** | Docker usage and local testing |
| **FRAMEWORK_REFERENCE.md** | Complete technical reference |
| **PROBLEMS_AND_SOLUTIONS.md** | Quick problem lookup |
| **GITHUB_ACTIONS_SETUP.md** | CI/CD integration guide |

---

## **✨ Features**

- ✅ **Scalable**: 500+ tests with 4-8 parallel workers
- ✅ **Self-Healing**: Automatic waits, retries, stale element recovery
- ✅ **Multi-Environment**: dev, qa, prod configs
- ✅ **Production Ready**: Full logging, reporting, CI/CD
- ✅ **Maintainable**: Page Object Model + Base Page (39 methods)
- ✅ **Complete Utilities**: Waits, assertions, retry, validators, decorators
- ✅ **Test Data**: Dynamic factories (user, product, order)
- ✅ **Docker Ready**: Consistent environment across machines
- ✅ **CI/CD Ready**: GitHub Actions workflow included

---

## **🎯 Architecture**

```
8 Production Layers:
1. Tests (smoke, regression, e2e)
2. Page Objects (with 100+ inherited methods)
3. Base Page (39 methods - all inherited)
4. Utils (waits, assertions, retry, validators, decorators)
5. Configuration (dev/qa/prod)
6. Fixtures (browser, auth, database, server)
7. Pytest Setup (markers, hooks, parallel)
8. Logging & Reporting (HTML, console, file)
```

---

## **🚀 GitHub Actions Setup**

CI/CD is **already configured** in `.github/workflows/test.yml`

### **How It Works:**

1. **Push code** to GitHub
2. **Actions runs automatically** on push/PR
3. **Tests execute** in Docker container
4. **Reports generated** (HTML + screenshots)
5. **Results available** for download

See `GITHUB_ACTIONS_SETUP.md` for complete setup.

---

## **📁 Project Structure**

```
ui_automation_framework/
├── tests/                  # Test suites
│   ├── smoke/             # Quick tests ✅
│   ├── regression/        # Full suite (ready)
│   └── e2e/              # End-to-end (ready)
├── pages/                 # Page Object Model
│   ├── base_page.py      # 39 core methods
│   ├── components/       # Reusable parts (ready)
│   └── page_objects/     # Your page objects go here
├── fixtures/             # Pytest fixtures (4 types)
├── config/               # Multi-environment configs
├── utils/                # All utilities complete
├── data/                 # Test data & factories
├── docs/                 # Documentation
├── .github/workflows/    # GitHub Actions CI/CD
├── Dockerfile            # Docker setup
├── conftest.py           # Pytest config
├── pytest.ini            # Pytest settings
└── requirements.txt      # Dependencies
```

---

## **🎓 Common Commands**

```bash
# Run all tests
pytest tests/ -v

# Run smoke tests only
pytest tests/smoke/ -v

# Parallel execution (4 workers)
pytest tests/ -n 4 -v

# Stop on first failure
pytest tests/ -x -v

# Single test
pytest tests/smoke/test_playwright_docs.py::TestPlaywrightDocs::test_docs_page_loads -v

# With HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Different environment
ENV=dev pytest tests/ -v
ENV=qa pytest tests/ -v
ENV=prod pytest tests/ -v

# Run with Docker
docker build -t ui-automation:latest .
docker run --rm -v $(pwd)/reports:/app/reports ui-automation:latest
```

---

## **🔧 How to Use This Template**

### **For YOUR Website:**

1. **Clone this repo**
   ```bash
   git clone <this-repo> my-ui-tests
   cd my-ui-tests
   ```

2. **Update configuration** (`config/env/dev.yaml`)
   ```yaml
   base_url: "https://myapp.com"
   browser:
     name: chromium
     headless: true
   ```

3. **Create page object**
   ```python
   # pages/page_objects/my_app_page.py
   from pages.base_page import BasePage
   
   class MyAppPage(BasePage):
       LOGIN_BTN = "button[data-testid='login']"
       
       def login(self, email, password):
           self.fill_text("input[name='email']", email)
           self.fill_text("input[name='password']", password)
           self.click(self.LOGIN_BTN)
   ```

4. **Write test**
   ```python
   # tests/smoke/test_my_app.py
   from pages.page_objects.my_app_page import MyAppPage
   
   class TestMyApp:
       @pytest.mark.smoke
       def test_login(self, page):
           app = MyAppPage(page)
           app.goto("/")
           app.login("user@example.com", "password")
   ```

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

**See `SETUP_NEW_PROJECT.md` for detailed step-by-step guide.**

---

## **✅ What's Included**

| Component | Status |
|-----------|--------|
| Test Framework | ✅ Complete |
| Page Objects | ✅ Ready |
| Fixtures (Browser, Auth, DB, Server) | ✅ Complete |
| Utils (Waits, Assertions, Retry, Validators, Decorators) | ✅ Complete |
| Test Data Factories | ✅ Complete |
| Configuration System | ✅ Complete |
| CI/CD Workflow | ✅ Ready |
| Docker Setup | ✅ Ready |
| Documentation | ✅ Complete |

---

## **🏆 Framework Highlights**

### **Self-Healing**
- Explicit waits (no sleep)
- Auto-retry on failure (3 attempts)
- Stale element recovery
- Dynamic wait strategies

### **Parallel Execution**
- 4-8 workers supported
- 500 tests in ~15 minutes
- Browser reuse per worker
- Unique test data per test

### **Production Ready**
- Structured logging (DEBUG/INFO/ERROR)
- HTML reports (auto-generated)
- Screenshots on failure
- Multi-environment support
- GitHub Actions CI/CD
- Docker containerization

### **Developer Friendly**
- Page Object Model for maintainability
- Base Page with 39 common methods
- Custom utilities for complex scenarios
- Comprehensive documentation
- Example tests to learn from

---

## **📊 Framework Verification**

```
Local Machine Test Results:
$ pytest tests/smoke/test_playwright_docs.py -v
✓ test_docs_page_loads (2s)
✓ test_page_has_content (2s)
✓ test_search_input_visible (1s)
✓ test_get_started_link_exists (2s)
✓ test_navigation_works (3s)
======== 5 passed in 10.5s ========

GitHub Actions: ✅ Working
Docker Build: ✅ Working
All Systems: ✅ GO
```

---

## **🚀 Next Steps**

1. **Read** `SETUP_NEW_PROJECT.md` for detailed setup
2. **Clone** this repo to your own GitHub
3. **Customize** config for your application
4. **Create** page objects for your pages
5. **Write** your first test
6. **Run** tests locally
7. **Push** to GitHub (CI/CD runs automatically!)

---

## **📞 Support**

- **Getting Started?** → `SETUP_NEW_PROJECT.md`
- **Quick Setup?** → `QUICK_START.md`
- **Technical Questions?** → `FRAMEWORK_REFERENCE.md`
- **Problem Solving?** → `PROBLEMS_AND_SOLUTIONS.md`
- **Docker Help?** → `DOCKER_SETUP.md`
- **CI/CD Setup?** → `GITHUB_ACTIONS_SETUP.md`

---

**Framework Status:** ✅ **PRODUCTION READY - TEMPLATE READY**
**Last Updated:** December 2025
**Python:** 3.9+
**Browser:** Chromium (Playwright)
**CI/CD:** GitHub Actions Ready
**Deployment:** Docker Ready
