# Interface Design for Testability — Backend

Good interfaces make testing natural:

1. **Accept dependencies, don't create them**

```python
# Testable
def process_order(order, payment_gateway):
    return payment_gateway.charge(order.amount)

# Hard to test
def process_order(order):
    gateway = StripeGateway()
    return gateway.charge(order.amount)
```

Pass dependencies so they can be mocked in tests.

2. **Return results, don't rely on side effects**

```python
# Testable
def calculate_discount(cart):
    return cart.total * 0.1

# Hard to test
def apply_discount(cart):
    cart.total -= cart.total * 0.1
```

Returning values makes assertions simple and predictable.

3. **Small surface area**

* Fewer methods = fewer tests
* Fewer parameters = simpler setup

```python
# Simple interface
class PricingService:
    def calculate(self, cart):
        ...

# Complex interface
class PricingService:
    def calculate(self, cart, user, coupons, region, time, db_conn):
        ...
```

4. **Use function signatures as interfaces**

Python doesn't require formal interfaces—your function signature *is the contract*.

```python
def send_message(user_id: int, text: str) -> bool:
    ...
```

Keep signatures clear and minimal.

5. **Design for easy mocking**

```python
# Testable
def send_notification(message, client):
    return client.send(message)

# Hard to test
def send_notification(message):
    import requests
    requests.post("https://api.example.com", json={"msg": message})
```

External calls should always be injectable.

6. **Keep business logic separate from Django framework code**

```python
# Testable (pure logic)
def calculate_total(items):
    return sum(item.price for item in items)

# Django view just orchestrates
def checkout_view(request):
    total = calculate_total(get_items(request))
    return Response({"total": total})
```

Makes logic testable without database or request setup.

7. **Avoid hidden state / global dependencies**

```python
# Hard to test
def get_discount():
    return settings.DISCOUNT_RATE

# Better
def get_discount(rate):
    return rate
```

Explicit inputs = predictable tests.

## Summary

* Pass dependencies (don't instantiate inside)
* Return values instead of mutating state
* Keep interfaces small and clear
* Separate business logic from Django layers
* Make external interactions injectable
