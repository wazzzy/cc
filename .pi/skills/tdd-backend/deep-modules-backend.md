# Deep Modules — Backend

From "A Philosophy of Software Design":

**Deep module** = small interface + lots of implementation

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid)

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing interfaces, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Django Examples

**Custom Manager** — hides complex queryset logic behind a simple call:

```python
# Deep: hides filtering, annotation, prefetch complexity
active_orders = Order.objects.active_for_user(user)

# Shallow: caller must know internal structure
active_orders = Order.objects.filter(
    status="active", user=user
).select_related("items").annotate(...)
```

**Service class** — hides multi-step orchestration behind one method:

```python
# Deep
class CheckoutService:
    def complete(self, cart, payment_method) -> Order:
        ...  # validates, charges, creates order, sends email

# Shallow (caller orchestrates everything)
def checkout_view(request):
    validate_cart(cart)
    charge_payment(payment_method, cart.total)
    order = create_order(cart)
    send_confirmation_email(order)
```

**Utility module** — hides formatting/parsing complexity:

```python
# Deep
from myapp.utils import format_currency  # handles locale, rounding, symbols

# Shallow
f"${amount:.2f}"  # scattered everywhere, no centralised logic
```
