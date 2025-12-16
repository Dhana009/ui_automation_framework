# UI Automation Framework - Industry Standard Reference

**Purpose:** Quick reference for architecture decisions, best practices, and solutions to common problems. Not a guide, but a reference for when stuck or uncertain.

---

## **ARCHITECTURAL DECISIONS (CONFIRMED)**

These decisions were made to ensure scalability, maintainability, and self-healing capabilities for 500+ tests.

### **Decision 1: Page Object Model Structure**
**CHOSEN:** Hierarchical POM (Scalable)
```
pages/
├── base_page.py (common methods)
├── components/ (reusable UI parts)
│   ├── header.py
│   ├── modal.py
│   └── sidebar.py
└── page_objects/ (full pages)
    ├── login_page.py
    ├── dashboard_page.py
    └── products_page.py
```
**Why:** Scales to 500+ tests, reusable components, reduces duplication.

---

### **Decision 2: Self-Healing Strategy**
**CHOSEN:** Combination Approach (Wait + Retry + Stale Recovery)
```
1. Explicit waits (don't use sleep)
2. Auto-retry on transient failures (3 attempts, 2s delay)
3. Stale element recovery (re-locate element if becomes invalid)
```
**Why:** Handles 95% of flakiness issues automatically.

---

### **Decision 3: Layer Independence & Communication**
**CHOSEN:** Loose Coupling
```
Test → Page Object (inherits BasePageClass)
         ↓
      Base Page Methods (click, type, wait, assert)
         ↓
      Utils (waits, assertions, logger, retry)
         ↓
      Config (timeouts, URLs, credentials)
         ↓
      Fixtures (browser, page, logins)
```
**Why:** Each layer has specific job, independent, easy to maintain/scale.

---

### **Decision 4: Test Data Management**
**CHOSEN:** Hybrid Approach (YAML + Factories)
```
YAML (Static):
- User credentials
- Error messages
- Test constants

Factories (Dynamic):
- Unique user accounts per test
- Random product data
- Parallel-safe data generation
```
**Why:** Reusable static data + unique data prevents test conflicts in parallel.

---

### **Decision 5: Configuration Management**
**CHOSEN:** Multi-Option Approach (Env Vars + CLI Args)
```
Option A - Environment Variable:
  ENV=qa pytest tests/

Option B - Command Line:
  pytest tests/ --env=qa --browser=firefox

Option C - Config Files:
  config/env/dev.yaml, qa.yaml, prod.yaml
```
**Why:** Flexibility for different execution scenarios (local, CI/CD, manual).

---

### **Decision 6: Parallel vs Sequential Execution**
**CHOSEN:** Hybrid Model
```
Parallel Tests (400 tests):
- 4-8 workers
- scope="module" fixtures
- ~15 minutes

Sequential Tests (100 tests):
- 1 worker
- scope="session" fixtures
- Dependencies via @pytest.mark.dependency
- ~10 minutes

Total: ~25 minutes for 500 tests
```
**Why:** Balance between speed and maintaining state for dependent tests.

---

### **Decision 7: Fixture Scoping Strategy**
**CHOSEN:** Context-Based Scoping
```
✅ Parallel tests: scope="module" (one browser per test file)
✅ Sequential tests: scope="session" (one browser for entire suite)
✅ Independent tests: scope="function" (new browser per test, if needed)
✅ Cleanup: Always cleanup in fixture teardown (isolation)
```
**Why:** Optimizes performance while maintaining test isolation.

---

### **Decision 8: Error Handling & Logging**
**CHOSEN:** Centralized with Auto-Capture
```
Logging Levels: DEBUG (local) → INFO (CI)
Screenshot: On failure only (saves space)
Logs: Console + file
Retry: 3 attempts with exponential backoff
```
**Why:** Easy debugging, minimal storage, automatic recovery.

---

### **Decision 9: Marker System for Test Organization**
**CHOSEN:** Multi-Level Markers
```
Level 1 - Type: @pytest.mark.smoke, regression, e2e
Level 2 - Execution: @pytest.mark.parallel, sequential
Level 3 - Priority: @pytest.mark.critical, flaky
Level 4 - Feature: @pytest.mark.login, payment, etc.

Run combinations:
  pytest tests/ -m "smoke and parallel" -n 4
  pytest tests/ -m "sequential"
  pytest tests/ -m "critical" -n 8
```
**Why:** Flexible test selection for different scenarios.

---

### **Decision 10: Self-Healing Techniques**
**CHOSEN:** Multi-Layer Self-Healing
```
1. Selector Fallback:
   - Primary selector (data-testid)
   - Secondary selector (text, class)
   - Tertiary selector (XPath)

2. Stale Element Recovery:
   - Always re-locate, never cache
   - Catch stale errors, retry immediately

3. Auto-Retry:
   - Transient failures: retry 3 times
   - Network glitches: handled automatically

4. Dynamic Waits:
   - Explicit waits (not sleep)
   - Adaptive timeouts based on environment

5. State Recovery:
   - Fixture cleanup (clear cookies, localStorage)
   - Login re-attempt on session loss
```
**Why:** Minimizes manual intervention, increases test reliability.

---

### **Decision 11: Base Page Class Architecture**
**CHOSEN:** Mixin-Ready Single Class (Extensible Design)
```
Current Design:
- Single base_page.py with 34 core methods
- All methods organized by category (waits, interactions, etc.)
- Clean separation within single file

Future Expansion (When Needed):
- Extract methods into mixins (keyboard_mixin.py, mouse_mixin.py, etc.)
- No breaking changes to page objects
- Page objects inherit automatically

Refactoring Trigger:
- When base_page.py exceeds 600 lines
- When organizing into logical modules makes sense
```
**Base Page Methods (34 total):**
- Wait Methods (6): wait_for_element, wait_for_url, wait_for_load_state, etc.
- Interaction Methods (6): click, type_text, fill_text, get_text, get_attribute
- Visibility Checks (5): is_visible, is_element_present, is_enabled, is_checked
- Utility Methods (7): scroll_to_element, hover, take_screenshot, goto, reload, go_back, go_forward
- Page State Methods (3): get_page_title, get_current_url, get_page_source
- Form Methods (3): select_option, check_checkbox, uncheck_checkbox
- Custom Assertions (4): assert_element_visible, assert_text_contains, assert_element_enabled, assert_url_contains

**Future Additions (When Needed):**
- Keyboard Methods: press_key(), keyboard_shortcut()
- Mouse Methods: double_click(), right_click(), drag_and_drop()
- File Upload: upload_file()
- Frame/Alert: switch_to_frame(), accept_alert()
- Window Handling: switch_to_window()

**How to Add Methods in Future:**
```
Step 1: If method < 50 lines and fits category → Add to base_page.py
Step 2: If method is new category → Create mixin file (e.g., keyboard_mixin.py)
Step 3: Mix into BasePage class (no page object changes needed)
Step 4: Page objects automatically inherit new methods
```

**Why:** Keeps framework simple now, scalable later without refactoring page objects.

---

### **Summary of All Decisions**

| Decision | Chosen | Reason |
|----------|--------|--------|
| POM Structure | Hierarchical | Scalable to 500+ tests |
| Self-Healing | Wait + Retry + Recovery | Handles 95% flakiness |
| Layer Communication | Loose Coupling | Independent, maintainable |
| Test Data | Hybrid (YAML + Factories) | Reusable + parallel-safe |
| Configuration | Env Vars + CLI | Flexible execution |
| Execution Model | Hybrid (Parallel + Sequential) | Speed + state management |
| Fixture Scoping | Context-based | Performance optimized |
| Error Handling | Centralized + Auto-Capture | Easy debugging |
| Test Organization | Multi-Level Markers | Flexible selection |
| Self-Healing Techniques | Multi-Layer Approach | Reliability maximized |
| Base Page Architecture | Mixin-Ready Single Class | Simple now, scalable later |

---

## **TOP 3 FEATURES FOR 80% BENEFIT (3-Year SDET Experience)**

These 3 additions solve 80% of real-world automation problems. Implement after core framework.

### **Feature 1: Flaky Test Quarantine System (35% Impact)**

**Problem:** Tests fail intermittently (30% failure rate). Blocks team, wastes time debugging.

**Solution:**
```
- Track pass rate per test
- Pass rate < 95% → Automatically quarantine
- Quarantined tests are skipped
- Team investigates separately
```

**Implementation Details:**
```python
# conftest.py - Track test results
FLAKY_TEST_THRESHOLD = 0.95  # 95% pass rate required

def is_test_flaky(test_name):
    # Read from flaky_tests.json
    if test_name in flaky_registry:
        pass_rate = flaky_registry[test_name]["pass_rate"]
        return pass_rate < FLAKY_TEST_THRESHOLD
    return False

@pytest.fixture(autouse=True)
def quarantine_check(request):
    if is_test_flaky(request.node.name):
        pytest.skip(f"Test quarantined - flaky (pass rate < 95%)")

# After test completes, update pass rate
def update_flaky_status(test_name, passed):
    # Update flaky_tests.json with new pass rate
    pass
```

**Data Structure:**
```json
{
  "test_payment_gateway": {
    "total_runs": 100,
    "passed": 68,
    "failed": 32,
    "pass_rate": 0.68,
    "quarantined": true,
    "last_run": "2024-01-15"
  }
}
```

**Benefit:** 
- Real failures get noticed immediately
- Flaky tests don't block CI/CD
- Clear visibility into test reliability

---

### **Feature 2: Test Data Cleanup on Failure (30% Impact)**

**Problem:** Test creates user/order. Test fails. Data never cleaned. Next test conflicts with orphaned data.

**Solution:**
```
- Track all resources created during test
- On test failure → Delete all created resources
- Use API for fast cleanup (not UI)
- Log all cleanup actions
```

**Implementation Details:**
```python
# conftest.py - Global cleanup registry
class CleanupRegistry:
    def __init__(self):
        self.resources = []
    
    def register(self, resource_type, resource_id, cleanup_fn):
        """Register a resource that needs cleanup"""
        self.resources.append({
            "type": resource_type,
            "id": resource_id,
            "cleanup_fn": cleanup_fn
        })
    
    def cleanup_all(self):
        """Execute all cleanup functions"""
        for resource in reversed(self.resources):  # Reverse order
            try:
                resource["cleanup_fn"](resource["id"])
                logger.info(f"Cleaned up {resource['type']} {resource['id']}")
            except Exception as e:
                logger.error(f"Failed to cleanup {resource['type']}: {e}")
        self.resources = []

cleanup_registry = CleanupRegistry()

@pytest.fixture(autouse=True)
def auto_cleanup(request):
    yield
    # Cleanup runs after test completes (pass or fail)
    cleanup_registry.cleanup_all()
```

**Usage in Tests:**
```python
def test_create_user(page, cleanup_registry):
    # Create user via API
    user = create_user("user@example.com")
    
    # Register cleanup
    cleanup_registry.register(
        "user", 
        user["id"], 
        lambda uid: delete_user_api(uid)
    )
    
    # Test continues
    page.goto(dashboard)
    # If test fails here, user is still cleaned up
```

**Benefit:**
- No orphaned test data
- Parallel tests can safely use same environment
- Predictable, isolated test execution

---

### **Feature 3: Smart Retry with Flaky Detection (15% Impact)**

**Problem:** Test fails once, passes on retry. Hard to distinguish real failures from transient ones.

**Solution:**
```
- On test failure, automatically retry (3 attempts)
- If passes on retry → Mark as FLAKY
- If fails all 3 → Mark as BROKEN
- Quarantine flaky tests automatically
```

**Implementation Details:**
```python
# decorators.py - Smart retry decorator
def auto_retry(max_attempts=3, delay=2):
    """
    Retry decorator that detects flaky tests
    If test passes on retry, marks it as flaky
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    
                    # If passed on retry (attempt > 1), mark as flaky
                    if attempt > 1:
                        mark_as_flaky(func.__name__, attempt)
                        logger.warning(f"Test {func.__name__} is FLAKY - passed on attempt {attempt}")
                    
                    return result
                
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt}/{max_attempts} failed for {func.__name__}")
                    
                    if attempt < max_attempts:
                        time.sleep(delay)
                    else:
                        # All attempts failed
                        mark_as_broken(func.__name__)
                        logger.error(f"Test {func.__name__} is BROKEN - all {max_attempts} attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator

# Usage
@auto_retry(max_attempts=3, delay=2)
def test_api_call(page):
    response = page.goto("https://api.example.com/data")
    assert response.status == 200

def mark_as_flaky(test_name, attempt_passed):
    """Update flaky_tests.json"""
    # Record that test passed on attempt X
    pass

def mark_as_broken(test_name):
    """Update broken_tests.json"""
    # Record that test failed all attempts
    pass
```

**Flaky Test Tracking:**
```json
{
  "test_api_call": {
    "status": "FLAKY",
    "passes_on_attempt": 2,
    "frequency": "occasionally fails",
    "first_detected": "2024-01-10"
  },
  "test_payment": {
    "status": "BROKEN",
    "all_attempts_failed": true,
    "failure_reason": "Element not found"
  }
}
```

**Benefit:**
- Distinguish real failures from transient ones
- Automatic flaky test detection
- Team focuses on actual issues

---

## **Implementation Timeline**

| Phase | What | Duration |
|-------|------|----------|
| **Phase 1** | Core framework (current plan) | Week 1 |
| **Phase 2** | Feature #1: Quarantine System | Week 2 |
| **Phase 3** | Feature #2: Data Cleanup | Week 3 |
| **Phase 4** | Feature #3: Smart Retry | Week 4 |

---

## **Key Files to Add for These Features**

```
utils/
├── flaky_detector.py         # Feature 1 - Flaky tracking
├── cleanup_registry.py       # Feature 2 - Data cleanup
└── smart_retry.py            # Feature 3 - Retry logic

data/
└── flaky_tests.json          # Track flaky tests
└── cleanup_registry.json     # Track what needs cleanup

docs/
└── FLAKY_TEST_GUIDE.md       # Documentation
```

---

## **This Makes You Ahead of 80% of Teams**

**Most Teams Struggle With:**
- ❌ Flaky tests blocking CI/CD pipeline
- ❌ Test data conflicts in parallel execution
- ❌ Inability to distinguish real vs transient failures

**Your Framework Will Have:**
- ✅ Automatic flaky test quarantine
- ✅ Automatic test data cleanup
- ✅ Smart retry with failure classification
- ✅ Team ahead of industry standard

---

---

## **REPORTING STRATEGY (3-Layer Approach)**

### **Layer 1: Local HTML Report**
**When:** Developer runs tests locally
**Command:** `pytest tests/ --html=reports/report.html --self-contained-html`
**Shows:** Pass/fail, screenshots, duration per test
**Benefit:** Instant feedback without terminal parsing

### **Layer 2: CI/CD Dashboard**
**When:** Tests run in GitHub Actions/Jenkins
**Setup:** Generate XML report → CI parses it
**Shows:** Real-time pass/fail in GitHub
**Benefit:** No external tools needed

### **Layer 3: Slack Alert**
**When:** Tests fail
**Setup:** Webhook posts to Slack channel
**Shows:** Failed test names, pass/fail stats, link to report
**Benefit:** Team alerted immediately

---

## **Implementation Timeline for Reporting**

| Phase | What | Tool |
|-------|------|------|
| Phase 1 | Local HTML reports | pytest-html |
| Phase 2 | GitHub Actions CI/CD | GitHub Actions |
| Phase 3 | Slack alerts | Webhook |
| Phase 4+ | Trend dashboard, email, Allure (optional) | Later |

---

## **Reporting Setup Summary**

```
Developer:
  pytest tests/ → HTML report opens locally

CI/CD:
  GitHub Actions → Runs tests → XML report → Shows in GitHub

Team Alert:
  On failure → Slack notification → Click → View report

Result:
  Everyone sees results in their preferred place
```

---

## **SECTION 1: FRAMEWORK ARCHITECTURE**

### **Q1.1: What's the Production-Level Folder Structure?**

```
ui-automation/
├── tests/
│   ├── smoke/           # Quick smoke tests
│   ├── regression/      # Full regression suite
│   └── e2e/            # End-to-end workflows
├── pages/
│   ├── base_page.py    # Common methods for all pages
│   ├── components/     # Reusable UI components
│   └── page_objects/   # Individual page classes
├── fixtures/
│   ├── browser_fixtures.py    # Browser setup/teardown
│   └── auth_fixtures.py       # Login/auth fixtures
├── config/
│   ├── env/
│   │   ├── dev.yaml
│   │   ├── qa.yaml
│   │   └── prod.yaml
│   └── settings.py     # Config loader
├── data/
│   ├── test_data.yaml
│   └── factories/
│       ├── user_factory.py
│       └── product_factory.py
├── utils/
│   ├── waits.py        # Wait strategies
│   ├── assertions.py   # Custom assertions
│   ├── logger.py       # Logging setup
│   ├── retry.py        # Retry decorators
│   ├── validators.py   # Data validation
│   ├── decorators.py   # Custom decorators
│   └── constants.py    # Constants
├── reports/            # Test reports
├── screenshots/        # Failure screenshots
├── logs/              # Log files
├── conftest.py        # Pytest configuration
├── pytest.ini         # Pytest settings
├── requirements.txt
└── README.md
```

**Industry Standard:** This structure scales to 500+ tests with parallel execution support.

---

### **Q1.2: What Goes in conftest.py?**

All reusable fixtures:
- Browser fixture (launch/close)
- Page fixture (create page)
- Login fixtures (authenticated sessions)
- Worker-specific login assignment
- Auto-cleanup hooks
- Screenshot on failure hooks

**Never put:** Test logic, assertions, or page object definitions here.

---

### **Q1.3: What Goes in base_page.py?**

Common methods inherited by all pages:
- click_element(selector)
- type_text(selector, text)
- wait_for_element(selector)
- is_visible(selector)
- scroll_to_element(selector)
- take_screenshot()
- get_text(selector)
- element_exists(selector)

**Pattern:** All page objects inherit from BasePageClass.

---

## **SECTION 2: CONFIGURATION MANAGEMENT**

### **Q2.1: How to Manage Multi-Environment Configs?**

```yaml
# config/env/dev.yaml
base_url: "http://localhost:3000"
browser:
  name: "chromium"
  headless: false
  slow_mo: 100
timeouts:
  page_load: 30
  element_wait: 10
logging:
  level: "DEBUG"
  to_file: true
```

```yaml
# config/env/qa.yaml
base_url: "http://qa.example.com"
browser:
  name: "chromium"
  headless: true
timeouts:
  page_load: 45
  element_wait: 15
logging:
  level: "INFO"
  to_file: true
```

**Industry Practice:** Load config from environment variable.
```bash
ENV=qa pytest tests/
```

---

### **Q2.2: How to Switch Environments Without Changing Tests?**

Load config once in conftest.py fixture:
```python
from config.settings import config

# All tests access: config.base_url, config.timeouts, etc.
# Change environment = one ENV variable
```

---

## **SECTION 3: FIXTURES & SESSION MANAGEMENT**

### **Q3.1: Fixture Scopes for Different Scenarios**

| Scope | Use Case | When |
|-------|----------|------|
| **function** | New browser per test | Independent tests, need isolation |
| **module** | One browser per test file | Related tests in same file |
| **session** | One browser for all tests | Sequential test suite |

**Industry Practice:** Use `scope="module"` for most parallel execution (best balance).

---

### **Q3.2: How to Assign Logins to Parallel Workers Automatically?**

```python
# conftest.py
LOGIN_POOL = [
    {"email": "user_1@example.com", "password": "pass1"},
    {"email": "user_2@example.com", "password": "pass2"},
    {"email": "user_3@example.com", "password": "pass3"},
    {"email": "user_4@example.com", "password": "pass4"},
]

@pytest.fixture(scope="session")
def get_worker_login():
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "master")
    if worker_id == "master":
        login = LOGIN_POOL[0]
    else:
        worker_num = int(worker_id[2:])
        login = LOGIN_POOL[worker_num % len(LOGIN_POOL)]
    return login
```

**How It Works:**
- pytest-xdist sets PYTEST_XDIST_WORKER environment variable
- Worker 1 (gw0) gets LOGIN_POOL[0]
- Worker 2 (gw1) gets LOGIN_POOL[1]
- Automatic, no manual assignment

---

### **Q3.3: How to Handle Login/Browser Failures?**

```python
@pytest.fixture(scope="module")
def authenticated_page(page, get_worker_login):
    try:
        page.goto(config.base_url)
    except Exception as e:
        pytest.skip(f"Browser launch failed: {e}")
    
    for attempt in range(1, 4):
        try:
            login(page, get_worker_login["email"], get_worker_login["password"])
            break
        except Exception as e:
            if attempt == 3:
                pytest.skip(f"Login failed after 3 attempts: {e}")
            time.sleep(2)
    
    yield page
    
    # Cleanup
    page.context.clear_cookies()
    page.evaluate("localStorage.clear()")
```

**Result:** If login fails, all tests using fixture are SKIPPED (not wasted).

---

## **SECTION 4: PARALLEL EXECUTION**

### **Q4.1: How Many Workers to Use?**

**Industry Standard:**
```
4-8 workers = optimal balance
- 4 workers = 500 tests in ~15 minutes
- 8 workers = 500 tests in ~10 minutes
- More workers = diminishing returns, resource overhead
```

**Command:**
```bash
pytest tests/ -n 4              # 4 workers
pytest tests/ -n auto           # Auto-detect CPU cores
pytest tests/ -n 8              # Explicit 8 workers
```

---

### **Q4.2: How Many Logins to Define?**

**Rule:** Define at least as many logins as max workers you'll use.

```
Running with 4 workers? Define 4+ logins
Running with 8 workers? Define 8+ logins

Having extra logins is fine (they won't be used)
Having fewer logins = they cycle via modulo
```

---

### **Q4.3: Do We Launch New Browser Per Test?**

**NO.** This is a common misconception.

**What Industry Does:**
- 1 browser PER WORKER (not per test)
- Fixture scope="module" REUSES browser across tests
- Each test in worker uses same browser session
- Browser launch happens once per worker

**Result:**
```
500 tests with 4 workers
= 4 browsers, NOT 500 browsers
= 4 logins, NOT 500 logins
```

---

### **Q4.4: How to Mix Parallel + Sequential Tests?**

```bash
# Run all tests
pytest tests/ -n 4

# Runs:
# 1. All parallel tests with 4 workers (0-10 min)
# 2. All sequential tests sequentially (10-25 min)
# 3. Total: ~25 minutes
```

**Mark tests in code:**
```python
@pytest.mark.parallel
def test_smoke_1():
    pass

@pytest.mark.sequential
def test_user_journey_step_1():
    pass
```

---

### **Q4.5: How to Run Specific Tests with Markers?**

```bash
pytest tests/ -m sequential                    # Sequential tests only
pytest tests/ -m parallel                      # Parallel tests only
pytest tests/ -m smoke                         # Smoke tests only
pytest tests/ -m "smoke and parallel" -n 4    # Smoke tests, parallel, 4 workers
pytest tests/ -m "critical" -n 8              # Critical tests, 8 workers
```

---

## **SECTION 5: SEQUENTIAL TESTS WITH DEPENDENCIES**

### **Q5.1: How to Mark Test Dependencies?**

```python
@pytest.mark.dependency()
def test_01_user_registration():
    register_user("user@example.com")

@pytest.mark.dependency(depends=["test_01_user_registration"])
def test_02_verify_email():
    verify_email("user@example.com")

@pytest.mark.dependency(depends=["test_02_verify_email"])
def test_03_complete_profile():
    complete_profile("user@example.com")
```

**Requires:** `pip install pytest-dependency`

---

### **Q5.2: What Happens When Parent Test Fails?**

**Result:** All child tests are SKIPPED.

```
test_01: PASS ✓
  ├─ test_02: Runs → PASS ✓
  │   ├─ test_03: Runs → PASS ✓
  │   └─ test_04: Runs → FAIL ✗
  │       └─ test_05: SKIPPED (parent failed)
  └─ test_06: Runs → PASS ✓

Benefit: Saves time, no wasted execution on failed dependencies.
```

---

## **SECTION 6: TEST DATA MANAGEMENT**

### **Q6.1: Static vs Dynamic Test Data**

**Static (test_data.yaml):**
```yaml
valid_user:
  email: "user@example.com"
  password: "password123"
  name: "John Doe"

error_messages:
  invalid_email: "Please enter valid email"
  login_failed: "Invalid credentials"
```

**Dynamic (Factories):**
```python
# user_factory.py
def create_user():
    return {
        "email": f"user_{uuid.uuid4()}@example.com",
        "password": "password123",
        "name": f"User {random.randint(1, 9999)}"
    }
```

**When to Use:**
- Static: Same user every test
- Dynamic: Unique user per test (parallel, no conflicts)

---

### **Q6.2: How to Use Test Data in Tests?**

```python
def test_login(authenticated_page):
    # Data already in config
    email = config.test_data["valid_user"]["email"]
    
    # OR unique data
    user = user_factory.create_user()
    login(authenticated_page, user["email"], user["password"])
```

---

## **SECTION 7: FLAKINESS HANDLING (CRITICAL)**

### **Q7.1: Explicit Waits - Industry Standard**

**Problem:** `sleep(5)` wastes time, tests fail randomly.

**Solution:**
```python
# Wait for element to be present
page.wait_for_selector("button", timeout=10000)

# Wait for element to be visible
page.wait_for_selector("button", state="visible")

# Wait for specific URL
page.wait_for_url("**/dashboard")

# Wait for network idle (all requests done)
page.wait_for_load_state("networkidle")

# Wait for API response
page.wait_for_response(lambda resp: "api/users" in resp.url)
```

**Key Point:** Waits only as long as needed, not fixed time.

---

### **Q7.2: Stale Element References**

**Problem:** Element becomes invalid, "Element no longer attached to DOM".

**Solution:**
```python
# ❌ DON'T cache element
element = page.query_selector("button")
time.sleep(1)  # DOM changes
element.click()  # STALE!

# ✅ Always re-locate
page.click("button")  # Fresh locate every time
page.click("button")  # Fresh locate every time
```

**Industry Practice:** Never store element references, always re-locate.

---

### **Q7.3: Async/Network Operations**

**Problem:** Page loads data via API. Element doesn't exist until data arrives.

**Solution:**
```python
# Wait for network idle (all API calls done)
page.wait_for_load_state("networkidle")

# Wait for element (won't exist until API returns)
page.wait_for_selector(".data-loaded")

# Wait for specific API
page.wait_for_response(lambda resp: "api/users" in resp.url and resp.status == 200)
```

---

### **Q7.4: Retry Logic for Transient Failures**

**Problem:** Network glitch causes failure. Same test passes on retry.

**Solution:**
```python
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def login_with_retry(page, user, password):
    login(page, user, password)  # Retries 3 times if fails

# OR in fixture
for attempt in range(1, 4):
    try:
        login(page, user, password)
        break
    except Exception as e:
        if attempt == 3:
            raise
        time.sleep(2)  # Wait before retry
```

**Result:** Transient failures are handled automatically.

---

### **Q7.5: Test Isolation - Cleanup Between Tests**

**Problem:** Test 1 creates user. Test 2 expects clean state. User still exists.

**Solution:**
```python
@pytest.fixture(scope="function")
def authenticated_page(page):
    # Setup
    page.goto(base_url)
    login(page, user, password)
    
    yield page
    
    # Cleanup (always runs)
    page.context.clear_cookies()
    page.evaluate("localStorage.clear()")
    page.evaluate("sessionStorage.clear()")
    logout(page)  # If needed
```

**Result:** Each test gets clean state, no data leakage.

---

### **Q7.6: Element Visibility vs Existence**

**Problem:** Element exists in DOM but hidden (display: none). Can't click.

**Solution:**
```python
# Check existence
exists = page.query_selector("button") is not None

# Check visibility
is_visible = page.is_visible("button")

# Wait for visibility (not just existence)
page.wait_for_selector("button", state="visible")

# Check if clickable
is_clickable = page.is_enabled("button") and page.is_visible("button")
```

---

### **Q7.7: Dynamic Selectors**

**Problem:** IDs change every page load. Hard to select reliably.

**Solution:**
```python
# ❌ BAD - Uses dynamic ID
page.click("#button_12345")

# ✅ GOOD - Uses stable attributes
page.click("button:text('Login')")           # By text
page.click("button[type='submit']")          # By type
page.click("div.login button")               # By class
page.click("[data-testid='login-button']")   # By test ID (best)
page.click("//button[contains(text(), 'Login')]")  # XPath
```

**Industry Practice:** Use `data-testid` attributes for stable selectors.

---

### **Q7.8: Scroll to Element**

**Problem:** Element exists but off-screen. Click fails.

**Solution:**
```python
# Scroll into view
page.locator("button").scroll_into_view()
page.click("button")

# For sticky headers blocking view
page.evaluate("""
    document.querySelector('button').scrollIntoView({
        block: 'center'
    });
""")
page.click("button")
```

---

### **Q7.9: Screenshots & Logs on Failure**

**Problem:** Test fails. No evidence. Can't debug.

**Solution:**
```python
# Auto-screenshot on failure
@pytest.fixture(scope="function")
def page(browser, request):
    p = browser.new_page()
    yield p
    if hasattr(request, 'node') and request.node.rep_call.failed:
        p.screenshot(path=f"screenshots/{request.node.name}_FAILED.png")
    p.close()

# Logging
from utils.logger import get_logger
logger = get_logger(__name__)

def test_login(page):
    logger.info("Starting login")
    page.goto(base_url)
    logger.info("Navigated to login page")
    page.fill("input[name='email']", "user@example.com")
    logger.info("Filled email")
```

**Result:** Failed tests have screenshot + full log trail for debugging.

---

### **Q7.10: CI/CD Failures (Tests Pass Locally, Fail in CI)**

**Common Causes & Solutions:**

```
1. TIMING DIFFERENCE
   └─ CI is slower, increase timeouts
   
   if os.getenv("CI"):
       timeout = 20000  # CI: 20s
   else:
       timeout = 10000  # Local: 10s

2. RESOURCE CONSTRAINTS
   └─ Use fewer workers, headless mode
   
   # CI: pytest.ini
   addopts = -n 2 --headless

3. ENVIRONMENT DIFFERENCE
   └─ Force same config
   
   ENV=qa pytest tests/

4. MISSING DEPENDENCIES
   └─ Playwright browsers not installed
   
   # CI script:
   playwright install

5. NETWORK ISSUES
   └─ Add retry logic, increase network timeout
   
   @retry(stop=stop_after_attempt(3))
   def test_api_call():
       pass
```

---

## **SECTION 8: UTILS & HELPERS**

### **Q8.1: What Should Utils Contain?**

**waits.py:**
```python
def wait_for_element(page, selector, timeout=None):
    timeout = timeout or config.timeouts["element_wait"] * 1000
    page.wait_for_selector(selector, timeout=timeout)

def wait_for_text(page, text, timeout=None):
    timeout = timeout or config.timeouts["element_wait"] * 1000
    page.wait_for_function(f"document.body.textContent.includes('{text}')")
```

**assertions.py:**
```python
def assert_element_visible(page, selector):
    assert page.is_visible(selector), f"Element not visible: {selector}"

def assert_text_contains(page, selector, text):
    content = page.text_content(selector)
    assert text in content, f"Text '{text}' not found"
```

**logger.py:**
```python
def get_logger(name):
    logger = logging.getLogger(name)
    # Configure logging
    return logger
```

**decorators.py:**
```python
def retry(max_attempts=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
```

---

## **SECTION 9: PYTEST CONFIGURATION**

### **Q9.1: pytest.ini Settings**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = 
    -v
    -n 4
    --maxfail=5
    --tb=short
    --strict-markers

markers =
    smoke: Quick smoke tests
    regression: Full regression
    sequential: Sequential tests (order matters)
    parallel: Can run parallel
    critical: Critical tests
```

---

## **SECTION 10: COMMON SCENARIOS**

### **Q10.1: Running Different Test Suites**

```bash
# All tests (parallel first, then sequential)
pytest tests/ -n 4

# Only smoke tests in parallel
pytest tests/ -m "smoke and parallel" -n 4

# Only regression tests sequentially
pytest tests/ -m "regression and sequential"

# Only critical tests (fast feedback)
pytest tests/ -m critical -n 8

# Quick check before commit (2-3 minutes)
pytest tests/ -m "smoke and parallel" -n 4

# Full pre-release testing (30+ minutes)
pytest tests/ -n 4
```

---

### **Q10.2: Debugging a Failed Test**

```bash
# Run single test with full output
pytest tests/smoke/test_login.py::test_user_login -v -s

# Run with extra debug logging
pytest tests/smoke/test_login.py -v -s --log-cli-level=DEBUG

# Stop on first failure
pytest tests/ --maxfail=1

# Show full traceback
pytest tests/ --tb=long
```

---

### **Q10.3: Identifying Flaky Tests**

```bash
# Run same test 10 times
for i in {1..10}; do
    pytest tests/smoke/test_login.py::test_user_login
done

# If fails randomly = FLAKY
# Add explicit waits, retry logic, or dependencies
```

---

## **SECTION 11: TROUBLESHOOTING REFERENCE**

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Test sometimes passes, sometimes fails | Flaky waits, missing explicit waits | Add explicit waits, remove sleep() |
| Element not found | Element not loaded yet, wrong selector | Add wait, use robust selector |
| Stale element error | Element cached, DOM updated | Always re-locate, don't cache |
| Login fails sporadically | Network issue, transient | Add retry logic in fixture |
| Tests pass locally, fail in CI | Timing, environment, resources | Increase timeouts, match configs |
| All tests skip when login fails | Good! Fixture design working | Expected behavior |
| Parallel tests interfere | Shared state, same data | Use fixtures scope="function", unique data |
| Tests too slow | Too many logins, new browser per test | Use scope="module", reuse browser |

---

## **SECTION 12: QUICK DECISION TREE**

**When to use fixture scope="function"?**
- Independent tests needing isolation
- Small test suites (< 50 tests)

**When to use fixture scope="module"?**
- Parallel execution (most common)
- Related tests in same file

**When to use fixture scope="session"?**
- Sequential dependent tests
- Single large workflow

**When to use scope="function" with retry?**
- Tests that might fail due to network
- Integration with external services

**When to mark tests @pytest.mark.sequential?**
- Tests depend on each other's data
- Tests that modify shared state
- Multi-step user journeys

**When to mark tests @pytest.mark.parallel?**
- Independent tests
- Can run in any order
- No shared data

**When to use explicit waits?**
- ALWAYS (never use sleep())
- Async operations, API calls
- Elements that take time to load

**When to add retry logic?**
- Network operations
- Transient failures
- Integration tests with external services

---

## **FINAL CHECKLIST**

```
✅ Framework structure decided
✅ Config system understood
✅ Fixtures & scoping clear
✅ Parallel execution strategy set
✅ Sequential tests with dependencies known
✅ Test data management decided
✅ Flakiness handling covered (10 key issues)
✅ Utils organized
✅ Pytest configuration ready
✅ Troubleshooting reference available

Ready to BUILD!
```

---

**This document is a REFERENCE, not a guide.**
Use it when stuck on decisions, best practices, or troubleshooting.
Keep it handy during framework development and maintenance.

