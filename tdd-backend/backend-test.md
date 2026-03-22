# Good and Bad Tests

## Good Test Case

```python
from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import Post

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="securepass"
        )

    def test_create_post(self):
        post = Post.objects.create(
            title="Test Title",
            content="Test Content",
            author=self.user
        )

        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.author.username, "testuser")
        self.assertIsNotNone(post.id)
```

### Why this is good:

* Uses `setUp()` to avoid repetition
* Tests **one clear behavior**
* Uses meaningful assertions
* Independent and deterministic
* No external dependencies

---

## Bad Test Case

```python
from django.test import TestCase
from myapp.models import Post

class PostTest(TestCase):

    def test_post(self):
        post = Post.objects.create(title="Hello")

        assert post.title == "Hello"
        assert post.id != None
```

### Why this is bad:

* Missing required fields (may fail unpredictably)
* Uses raw `assert` instead of Django assertions
* No setup (hard to scale)
* Tests multiple things vaguely
* No real validation of business logic

---

## Another Quick Comparison

### Good (Focused API Test)

```python
from rest_framework.test import APITestCase
from django.urls import reverse

class PostAPITest(APITestCase):

    def test_create_post(self):
        url = reverse("post-list")
        data = {"title": "New Post", "content": "Body"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "New Post")
```

### Bad (Unclear API Test)

```python
def test_api(self):
    response = self.client.post("/posts/", {"title": "x"})
    assert response.status_code == 200
```

---

## Key Rules

* One test = one behavior
* Always assert **expected outcomes**, not just existence
* Use Django test utilities (`TestCase`, `APITestCase`)
* Avoid hardcoded URLs → use `reverse()`
* Keep tests isolated (no dependency on other tests)

---
