# Deep Modules — Frontend

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

- Can I reduce the number of props/params?
- Can I simplify the hook/component API?
- Can I hide more complexity inside?

## Frontend Examples

**Deep hook** — hides data fetching, caching, error state behind a simple interface:

```typescript
// Simple interface
const { user, loading } = useUser(id);

// vs shallow: caller must manage fetch, error, cache themselves
```

**Deep component** — hides layout/logic complexity behind minimal props:

```typescript
// Simple interface
<DataTable rows={rows} onSelect={handleSelect} />

// vs shallow: caller must wire up sorting, pagination, selection state
```
