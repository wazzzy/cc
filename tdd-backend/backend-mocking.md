# Mocking Guide

## When to Use Mocking

Use mocking when your code depends on:

* External APIs (payments, LLMs, third-party services)
* Slow operations (network, file I/O)
* Non-deterministic behavior (time, randomness)

---

## Good Mock Example

```python
from django.test import TestCase
from unittest.mock import patch
from myapp.services import send_notification

class NotificationTest(TestCase):

    @patch("myapp.services.requests.post")
    def test_send_notification(self, mock_post):
        mock_post.return_value.status_code = 200

        result = send_notification("hello")

        self.assertTrue(result)
        mock_post.assert_called_once()
```

### Why this is good:

* Mocks **external HTTP call**, not internal logic
* Uses correct import path (`myapp.services.requests.post`)
* Verifies both **result and interaction**

---

## Bad Mock Example

```python
from unittest.mock import patch

@patch("requests.post")
def test_notification(mock_post):
    mock_post.return_value.status_code = 200
```

### Why this is bad:

* Wrong patch location (won’t actually mock where used)
* No assertions
* Doesn’t test any real function

---

## Another Example (Django + Time)

### Good

```python
from unittest.mock import patch
from django.test import TestCase
from myapp.utils import is_expired

class ExpiryTest(TestCase):

    @patch("myapp.utils.now")
    def test_is_expired(self, mock_now):
        mock_now.return_value = 100

        self.assertTrue(is_expired(50))
```

---

### Bad

```python
def test_expired():
    assert is_expired(50)
```

### Why:

* Depends on real time → flaky test

---

## Rules for Mocking

* Mock **only external dependencies**, not your own logic
* Always patch **where it is used**, not where it comes from
* Keep mocks simple (avoid over-mocking)
* Always assert behavior (`called`, `called_once`, args)
* Prefer real objects unless mocking is necessary

---

## Avoid Mocking

* Django ORM (`models`, `querysets`)
* Simple pure functions
* Business logic you actually want to test
