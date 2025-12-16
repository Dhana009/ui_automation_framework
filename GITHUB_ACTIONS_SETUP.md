# GitHub Actions Setup Guide

Complete guide to run UI Automation Framework on GitHub Actions CI/CD.

---

## **📋 WHAT'S CONFIGURED**

The `.github/workflows/test.yml` workflow includes:

1. **Trigger Events:**
   - On every `push` to main/develop branches
   - On every `pull_request` to main/develop branches
   - Daily schedule at 2 AM UTC
   - Manual trigger via GitHub UI

2. **Test Jobs:**
   - **Main Test Job:** Runs all smoke tests on Python 3.11
   - **Sanity Check:** Validates framework structure

3. **Outputs:**
   - HTML reports (smoke_report.html, final_report.html)
   - Screenshots on failure
   - Test artifacts

---

## **🚀 QUICK START**

### **Step 1: Push to GitHub**

```bash
git init
git add .
git commit -m "Initial framework commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### **Step 2: GitHub Actions Runs Automatically**

Once pushed, GitHub Actions will:
1. Checkout code
2. Install Python 3.11
3. Install dependencies from requirements.txt
4. Install Playwright browsers
5. Run smoke tests
6. Generate HTML report
7. Upload artifacts

### **Step 3: View Results**

Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

Click latest run → See results → Download reports/screenshots

---

## **📊 WORKFLOW STAGES**

### **Stage 1: Environment Setup**
```yaml
- Checkout code
- Install Python 3.11
- Install pip dependencies
- Install Playwright browsers (Chromium only, saves time)
```

### **Stage 2: Run Tests**
```yaml
- Smoke tests: tests/smoke/test_playwright_docs.py
- Regression tests: tests/regression/ (if any)
- Generate HTML report
```

### **Stage 3: Collect Artifacts**
```yaml
- HTML reports → artifacts/test-reports/
- Screenshots (on failure) → artifacts/screenshots/
- Retention: 7 days for reports, 3 days for screenshots
```

### **Stage 4: Sanity Check**
```yaml
- Verify Python imports
- Check directory structure
```

---

## **⚙️ ENVIRONMENT VARIABLES**

The workflow uses:
```yaml
ENV: qa  # Uses config/env/qa.yaml
```

To change environment, edit `.github/workflows/test.yml`:
```yaml
env:
  ENV: dev  # or prod
```

---

## **🔧 CUSTOMIZE FOR YOUR NEEDS**

### **Option 1: Add Slack Notifications** (Optional)

1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Add to GitHub repo secrets: `Settings → Secrets → SLACK_WEBHOOK`
3. Uncomment in workflow

### **Option 2: Run on Different Schedule**

Edit cron in `.github/workflows/test.yml`:
```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM
  # Minute, Hour, Day, Month, Day-of-Week
  # Examples:
  # '0 8 * * *' = Every day at 8 AM
  # '0 8 * * 1' = Every Monday at 8 AM
  # '0 */4 * * *' = Every 4 hours
```

### **Option 3: Run Different Tests**

Edit test command in `.github/workflows/test.yml`:
```yaml
- name: Run smoke tests
  run: |
    pytest tests/smoke/ -v -n 4
    # OR
    # pytest tests/regression/ -v
    # pytest tests/e2e/ -v
    # pytest tests/ -m "smoke and parallel" -v
```

### **Option 4: Change Python Version**

Edit matrix in `.github/workflows/test.yml`:
```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']  # Run on all versions
```

---

## **📈 MONITORING**

### **Check Test Status**

1. Go to: `Actions` tab in GitHub repo
2. See all workflow runs
3. Click any run to see details
4. Check logs, artifacts, screenshots

### **Download Artifacts**

1. Click workflow run
2. Scroll to "Artifacts" section
3. Download `test-reports` or `screenshots`

### **View HTML Report**

1. Download `test-reports` artifact
2. Extract ZIP
3. Open `final_report.html` in browser
4. See detailed test results, durations, status

---

## **🐛 TROUBLESHOOTING**

### **Issue: Tests fail with "Browser not found"**
**Solution:** Workflow already installs Playwright. If fails:
```yaml
- name: Install Playwright
  run: |
    playwright install --with-deps chromium
```

### **Issue: Slow execution**
**Solution:** Reduce workers or use headless mode:
```yaml
pytest tests/smoke/ -n 2 --tb=short
```

### **Issue: Artifacts not saving**
**Solution:** Check workflow has `if: always()`:
```yaml
- name: Upload reports
  if: always()  # Run even if tests fail
```

---

## **✅ VERIFICATION**

After first run, confirm:
- ✅ Workflow runs successfully
- ✅ Tests execute (5 tests should pass)
- ✅ HTML report generated
- ✅ Artifacts available for download
- ✅ No errors in logs

---

## **📝 SAMPLE WORKFLOW RUN**

```
✓ Checkout code
✓ Set up Python 3.11
✓ Install dependencies (15s)
✓ Install Playwright browsers (30s)
✓ Run smoke tests (15s)
  - test_docs_page_loads PASSED
  - test_page_has_content PASSED
  - test_search_input_visible PASSED
  - test_get_started_link_exists PASSED
  - test_navigation_works PASSED
✓ Generate HTML report
✓ Upload artifacts
✓ Sanity check

Total Duration: ~2-3 minutes
```

---

## **🎯 NEXT STEPS**

1. **Push framework to GitHub**
2. **Let GitHub Actions run**
3. **Download HTML report**
4. **Replace selectors for YOUR website**
5. **Update tests for YOUR application**
6. **Commit and push changes**
7. **GitHub Actions runs automatically**

**Done! CI/CD is live! ✅**

---

## **💡 BEST PRACTICES**

1. **Always use `if: always()`** for artifact uploads
2. **Set retention days** to save storage
3. **Use environment variables** for config
4. **Keep CI/CD simple** (don't over-configure)
5. **Test locally first** before pushing
6. **Monitor action logs** for issues
7. **Use branch protection** - require CI passing before merge

---

## **📚 RESOURCES**

- GitHub Actions Docs: https://docs.github.com/en/actions
- Workflow Syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- Cron Schedule: https://crontab.guru/

---

**Framework is ready for production CI/CD! 🚀**

