# Problems & Solutions - Quick Reference

**Purpose:** Fast lookup. Problem? Find it. Solution? There it is. No fluff.

---

## **PROBLEM 1: Test Failures - Can't Debug**
**Cause:** No logs, no screenshots
**Solution:** Auto-screenshot on failure + structured logging
```
- On failure → Screenshot saved
- On failure → Full logs saved
- Reference in test report
```

---

## **PROBLEM 2: Tests Fail Randomly (30% Pass Rate)**
**Cause:** Flaky waits, no explicit waits, sleep(5)
**Solution:** Explicit waits + retry logic
```
- Use page.wait_for_selector() NOT sleep()
- Waits only as long as needed
- Add @auto_retry decorator (3 attempts)
```

---

## **PROBLEM 3: Can't Run 500 Tests Fast**
**Cause:** Sequential execution = slow
**Solution:** Parallel execution with pytest-xdist
```
- pytest tests/ -n 4 (4 workers)
- 500 tests = ~15 minutes (not hours)
- Each worker gets own browser + login
```

---

## **PROBLEM 4: Tests Interfere with Each Other (Parallel)**
**Cause:** Shared state, same test data, same user
**Solution:** Test isolation + unique data
```
- Each test gets fresh browser (scope="function")
- Clear cookies/localStorage in cleanup
- Use factories for unique user per test
```

---

## **PROBLEM 5: Database Full of Orphaned Test Data**
**Cause:** Test creates user → fails → user never deleted
**Solution:** Automatic cleanup on failure
```
- Track resources created
- On test failure → Auto-delete created resources
- Use API cleanup (fast, not UI)
```

---

## **PROBLEM 6: Same Test Fails Once, Passes Next Time**
**Cause:** Transient failure (network glitch)
**Solution:** Smart retry with flaky detection
```
- Fail? Retry 3 times
- Passes on retry? Mark as FLAKY
- Fails all 3? Mark as BROKEN
- Auto-quarantine flaky tests
```

---

## **PROBLEM 7: Selectors Break After UI Changes**
**Cause:** Hardcoded selectors like #button_12345 (dynamic IDs)
**Solution:** Robust selector strategies
```
- Use data-testid="button" (best)
- Use text: "button:text('Click Me')"
- Use xpath as fallback
- Never rely on ID attributes
```

---

## **PROBLEM 8: Element Not Found, But Element Exists**
**Cause:** Element exists in DOM but not visible
**Solution:** Check visibility, not just existence
```
- Wait for visible: page.wait_for_selector("button", state="visible")
- Check is_visible() before click
- Scroll to element if needed
```

---

## **PROBLEM 9: Login Fails, But Tests Still Run**
**Cause:** Tests assume login succeeded
**Solution:** Fixture failure skips all dependent tests
```
- Login in fixture
- If login fails → pytest.skip()
- All tests using fixture → SKIPPED
- No wasted test execution
```

---

## **PROBLEM 10: Stale Element Error Mid-Test**
**Cause:** Element reference cached, DOM updated
**Solution:** Always re-locate element
```
- ❌ element = page.query_selector("button")
     time.sleep(1)  # DOM changes
     element.click()  # STALE!

- ✅ page.click("button")  # Fresh locate every time
```

---

## **PROBLEM 11: Tests Pass Locally, Fail in CI/CD**
**Cause:** Timing differences, resource constraints
**Solution:** Environment-specific config + timeouts
```
- if CI: timeout = 20s (slower)
- if local: timeout = 10s (faster)
- Force same config: ENV=qa pytest
- Increase workers in CI
```

---

## **PROBLEM 12: API Takes 5 Seconds to Load Data**
**Cause:** No wait for network completion
**Solution:** Wait for network idle
```
- page.wait_for_load_state("networkidle")
- page.wait_for_response(lambda r: "api/users" in r.url)
- Element won't exist until API returns
```

---

## **PROBLEM 13: Too Many Logins = Slow Tests**
**Cause:** New browser + new login per test
**Solution:** Reuse browser with scope="module"
```
- Old: 500 tests = 500 browsers = 500 logins = SLOW
- New: 500 tests = 4 browsers = 4 logins (4 workers)
- Reuse browser across tests in same worker
```

---

## **PROBLEM 14: Parallel Tests Use Same Login = Conflict**
**Cause:** All tests use same user account
**Solution:** Auto-assign unique login per worker
```
- Define login pool: [user1, user2, user3, user4]
- Worker 1 → user1
- Worker 2 → user2
- Automatic, no manual assignment
```

---

## **PROBLEM 15: Can't Run Specific Tests**
**Cause:** Always run all 500 tests
**Solution:** Marker system for filtering
```
- @pytest.mark.smoke
- @pytest.mark.critical
- pytest tests/ -m "smoke and parallel" -n 4
- Run exactly what you need
```

---

## **PROBLEM 16: Dependent Tests Run Out of Order**
**Cause:** Parallel execution = random order
**Solution:** Dependency markers + sequential execution
```
- @pytest.mark.dependency()
- @pytest.mark.dependency(depends=["test_1"])
- If test_1 fails → test_2 SKIPPED
- Run: pytest tests/ -m sequential
```

---

## **PROBLEM 17: Test Environment Down = False Failures**
**Cause:** Tests fail because app is unavailable
**Solution:** Pre-test environment health check
```
- Before test suite → Check if app is online
- Check critical services are running
- If env down → Skip tests, don't fail
```

---

## **PROBLEM 18: Can't Tell Real Failure from Flaky**
**Cause:** Same test fails 30% of time
**Solution:** Quarantine unreliable tests
```
- Track pass rate per test
- Pass rate < 95% → Quarantine
- Quarantined tests SKIPPED
- Team investigates later
```

---

## **PROBLEM 19: Team Doesn't Know Framework Status**
**Cause:** No visibility into test results
**Solution:** HTML reports + metrics dashboard
```
- HTML report per test run
- Pass/fail trends over time
- Flaky test reports
- Performance regression alerts
```

---

## **PROBLEM 20: Framework Not Scalable**
**Cause:** Monolithic, tightly coupled layers
**Solution:** Layered architecture with loose coupling
```
- Test → Page Object → Utils → Config → Fixtures
- Each layer independent
- Change one layer ≠ affect others
- Reuse across entire framework
```

---

## **SOLUTION SUMMARY TABLE**

| # | Problem | Solution | Benefit |
|---|---------|----------|---------|
| 1 | Can't debug failures | Auto-screenshot + logs | Quick debugging |
| 2 | Random failures | Explicit waits + retry | Reliable tests |
| 3 | Slow execution | Parallel (4 workers) | 25 min for 500 tests |
| 4 | Tests interfere | Test isolation + unique data | No conflicts |
| 5 | Orphaned data | Auto-cleanup | Clean environment |
| 6 | Can't distinguish failures | Smart retry + quarantine | Focus on real issues |
| 7 | Selectors break | Robust selector strategy | Stable tests |
| 8 | Element not found | Check visibility | Prevent errors |
| 9 | Failed login wastes time | Fixture skip on failure | No wasted execution |
| 10 | Stale elements | Always re-locate | Prevent errors |
| 11 | CI failures | Env config + timeouts | Consistent results |
| 12 | Missing async waits | Wait for network | Reliable element access |
| 13 | Too many logins | Browser reuse | Fast execution |
| 14 | Login conflicts | Auto-assign per worker | Safe parallelism |
| 15 | Can't filter tests | Marker system | Run what you need |
| 16 | Dependent tests break | Dependency markers | Maintain order |
| 17 | False env failures | Health checks | Real insights |
| 18 | Can't identify flaky tests | Auto-quarantine | Reliable pipeline |
| 19 | No visibility | Reports + dashboard | Insights |
| 20 | Not scalable | Layered architecture | Grows to 1000+ tests |

---

## **ARCHITECTURE AT A GLANCE**

```
Test Layer
    ↓
Page Object Model (Hierarchical)
    ↓
Base Page (Common Methods)
    ↓
Utils (Waits, Assertions, Logger, Retry)
    ↓
Config (URLs, Timeouts, Credentials)
    ↓
Fixtures (Browser, Page, Logins, Cleanup)
    ↓
Playwright Browser
```

**Each layer:** Independent, focused job, reusable.

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

## **QUICK START CHECKLIST**

```
✅ Explicit waits (no sleep)
✅ Reuse browser (scope="module")
✅ Unique data per test (factories)
✅ Test isolation (cleanup fixtures)
✅ Retry logic (3 attempts)
✅ Auto-screenshot on failure
✅ Structured logging
✅ Marker system (smoke, regression, etc)
✅ Parallel execution (4-8 workers)
✅ Data cleanup on failure
✅ Local HTML reports (pytest-html)
✅ CI/CD integration (GitHub Actions)
✅ Slack alerts on failure

= Production-ready framework for 500+ tests with reporting
```

---

## **THIS FILE IS YOUR FAST REFERENCE**

Problem? Find it above.
Solution? Right there.
Implement? Look in FRAMEWORK_REFERENCE.md for details.

Keep this file open while building framework.

