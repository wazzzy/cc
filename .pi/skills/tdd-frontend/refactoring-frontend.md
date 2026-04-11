# Refactor Candidates — Frontend

After TDD cycle, look for:

- **Duplication** → Extract hook or utility function
- **Long components** → Break into smaller components (keep tests on the parent's public interface)
- **Prop drilling** → Introduce context or lift state to a custom hook
- **Shallow modules** → Combine or deepen (e.g. merge related hooks)
- **Feature envy** → Move logic to where data lives (co-locate with the component that owns the state)
- **Primitive obsession** → Introduce typed value objects or enums
- **Inline logic in JSX** → Extract to a named function or derived variable
- **Existing code** the new code reveals as problematic
