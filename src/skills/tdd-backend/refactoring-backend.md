# Refactor Candidates — Backend

After TDD cycle, look for:

- **Duplication** → Extract function, service method, or manager method
- **Long views** → Move business logic into service classes; views should only orchestrate (parse request → call service → return response)
- **Fat models** → Extract logic into managers, service classes, or utility modules; models should focus on data shape and simple properties
- **Shallow modules** → Combine or deepen (e.g. merge thin utility functions into a service class)
- **Feature envy** → Move logic to where data lives (e.g. move order total calculation onto the Order model or its manager)
- **Primitive obsession** → Introduce value objects or dataclasses (e.g. `Money`, `Address`) instead of passing raw `int`/`str`
- **Hidden framework coupling** → Extract pure Python logic out of Django views/models so it can be tested without request/ORM setup
- **Existing code** the new code reveals as problematic
