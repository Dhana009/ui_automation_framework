# Setting Up a New UI Automation Project

This is a production-ready UI automation framework template. Follow these steps to set up a new project for your application.

## Step 1: Clone the Framework

```bash
git clone <your-repo-url> my-ui-automation-project
cd my-ui-automation-project
```

## Step 2: Update Configuration

Edit the config files for your application:

```bash
# Development environment
vi config/env/dev.yaml

# QA environment
vi config/env/qa.yaml

# Production environment
vi config/env/prod.yaml
```

**Update these fields:**
- `base_url`: Your application's URL
- `browser`: Browser settings (chromium, firefox, webkit)
- `timeouts`: Adjust if needed
- `test_data`: Your test user credentials
- `logging`: Logging preferences

Example:
```yaml
base_url: "https://myapp.example.com"
browser:
  name: chromium
  headless: true
  viewport:
    width: 1920
    height: 1080
```

## Step 3: Create Page Objects

Create page objects for your application:

```bash
# Create new page object
touch pages/page_objects/my_page.py
```

Example page object:
```python
from pages.base_page import BasePage

class MyPage(BasePage):
    # Selectors
    HEADER = "h1"
    BUTTON = "button.submit"
    
    # Methods
    def get_header_text(self):
        return self.get_text(self.HEADER)
    
    def click_submit(self):
        self.click(self.BUTTON)
```

## Step 4: Create Tests

Create test files:

```bash
# Create test file
touch tests/smoke/test_my_feature.py
```

Example test:
```python
import pytest
from pages.page_objects.my_page import MyPage

class TestMyFeature:
    @pytest.mark.smoke
    def test_page_loads(self, page):
        my_page = MyPage(page)
        my_page.navigate("/")
        assert my_page.get_header_text() == "Welcome"
    
    @pytest.mark.smoke
    def test_button_click(self, page):
        my_page = MyPage(page)
        my_page.navigate("/")
        my_page.click_submit()
```

## Step 5: Run Tests Locally

```bash
# Run all smoke tests
pytest tests/smoke/ -v

# Run specific test file
pytest tests/smoke/test_my_feature.py -v

# Run with specific marker
pytest -m smoke -v

# Run with Docker
docker build -t my-ui-automation:latest .
docker run --rm -v $(pwd)/reports:/app/reports my-ui-automation:latest
```

## Step 6: Update Test Data Factories (Optional)

Customize test data factories for your needs:

```python
# data/factories/user_factory.py
class UserFactory:
    @staticmethod
    def create_valid_user():
        return {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
```

## Step 7: Set Up GitHub Actions Secrets (Optional)

For CI/CD, add secrets to GitHub:

1. Go to Settings → Secrets and variables → Actions
2. Add secrets:
   - `TEST_USERNAME`: Your test user email
   - `TEST_PASSWORD`: Your test user password
   - `BASE_URL`: Your test environment URL

## Step 8: Configure GitHub Actions

Update `.github/workflows/test.yml` if needed:

```yaml
- name: Run tests
  env:
    ENV: qa  # or dev, prod
  run: |
    docker run --rm \
      -e ENV=${{ env.ENV }} \
      -v ${{ github.workspace }}/reports:/app/reports \
      my-ui-automation:latest
```

## Directory Structure

```
my-ui-automation-project/
├── tests/
│   ├── smoke/           # Quick sanity tests
│   ├── regression/      # Full regression suite
│   └── e2e/            # End-to-end workflows
├── pages/
│   ├── base_page.py    # Core page object class
│   └── page_objects/   # Your page objects
├── fixtures/           # Pytest fixtures (browser, auth, etc)
├── config/
│   └── env/           # Environment configs
├── data/
│   └── factories/     # Test data generators
├── utils/             # Helpers (waits, assertions, logging)
├── Dockerfile         # Docker image
├── conftest.py        # Pytest configuration
└── pytest.ini         # Pytest settings
```

## Framework Features

✅ **Page Object Model** - Organized, maintainable page objects
✅ **Fixtures** - Browser, page, auth, database setup
✅ **Config Management** - Environment-specific configurations
✅ **Retry Logic** - Automatic retry for flaky tests
✅ **Custom Assertions** - Enhanced assertion messages
✅ **Logging** - Structured logging with colors
✅ **Parallel Execution** - Run tests in parallel with pytest-xdist
✅ **Docker** - Consistent environment across machines
✅ **Reports** - HTML test reports with screenshots
✅ **CI/CD Ready** - GitHub Actions integration

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (development)
pytest tests/smoke/ -v

# Run tests in parallel (4 workers)
pytest tests/smoke/ -v -n 4

# Run tests with specific marker
pytest -m smoke -v

# Run tests with HTML report
pytest tests/smoke/ --html=reports/report.html --self-contained-html

# Build Docker image
docker build -t my-ui-automation:latest .

# Run tests in Docker
docker run --rm -v $(pwd)/reports:/app/reports my-ui-automation:latest

# View test logs
cat logs/dev.log
```

## Troubleshooting

### Tests fail to connect to application
- Check `base_url` in config file
- Verify application is running
- Check network connectivity

### Playwright browser not found
```bash
python -m playwright install chromium
```

### Port already in use error
```bash
# Kill process using the port
lsof -ti:8000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :8000   # Windows
```

### Docker build fails
```bash
# Rebuild without cache
docker build --no-cache -t my-ui-automation:latest .
```

## Next Steps

1. Update `README.md` with your project details
2. Create your first page object
3. Write your first test
4. Run tests locally
5. Push to GitHub and verify CI/CD workflow

## Support

Refer to these documentation files:
- `DOCKER_SETUP.md` - Docker usage guide
- `docs/FRAMEWORK_REFERENCE.md` - Architecture decisions
- `docs/PROBLEMS_AND_SOLUTIONS.md` - Common issues
- `QUICK_START.md` - Quick reference

