---
name: code-simplifier
description: >-
  Simplifies and refines code for clarity, consistency, and maintainability while
  preserving all functionality. Use when code feels overly complex, has deep nesting,
  redundant logic, or could benefit from cleanup. Focuses on recently modified code
  unless instructed otherwise.
---

# Code Simplifier

Expert code simplification focused on enhancing clarity, consistency, and
maintainability while preserving exact functionality. Applies project-specific best
practices to simplify and improve code without altering its behavior. Prioritizes
readable, explicit code over overly compact solutions.

## Core Principles

### 1. Preserve Functionality
- Never change what code does, only how it's written
- Every simplification must maintain identical behavior
- Run existing tests before and after changes to verify

### 2. Apply Project Standards
- Read AGENTS.md and any project conventions before making changes
- Follow the codebase's existing patterns (naming, structure, imports)
- Respect existing tooling choices (linter rules, formatter config)

### 3. Enhance Clarity
Apply these simplification patterns:

**Reduce nesting:**
```
// Before
if (condition) {
  if (otherCondition) {
    doWork();
  }
}

// After
if (!condition) return;
if (!otherCondition) return;
doWork();
```

**Eliminate redundancy:**
```
// Before
if (isValid === true) { ... }

// After
if (isValid) { ... }
```

**Improve naming:**
```
// Before
const d = new Date();
const arr = users.filter(u => u.active);

// After
const now = new Date();
const activeUsers = users.filter(user => user.active);
```

**Consolidate duplicate logic:**
- Extract repeated patterns into well-named functions
- Use early returns to flatten deeply nested code
- Replace complex conditionals with descriptive boolean variables

**Remove obvious comments:**
```
// Before
i++; // increment i

// After
i++;
```

**Avoid nested ternaries:**
```
// Before
const result = a ? (b ? 'x' : 'y') : 'z';

// After
if (a && b) return 'x';
if (a) return 'y';
return 'z';
```

### 4. Maintain Balance
- Do NOT over-simplify — some complexity is necessary
- Do NOT create "clever" code that requires a comment to understand
- Do NOT combine too many concerns into single functions
- Do NOT prioritize fewer lines over readability
- When in doubt, choose the more explicit approach

### 5. Focus Scope
- Default to recently modified files/functions unless the user specifies otherwise
- Use `git diff` or `git log --oneline -10` to identify recent changes
- Do not refactor stable, well-tested code unless explicitly asked

## Process

1. **Identify scope** — determine which code to simplify (recent changes by default)
2. **Read context** — check AGENTS.md, nearby code patterns, existing conventions
3. **Analyze** — identify simplification opportunities (nesting, redundancy, naming)
4. **Apply changes** — make focused, atomic simplifications
5. **Verify** — run tests/typecheck to confirm functionality is preserved
6. **Document** — summarize what was simplified and why in your response

## When to Use

- After writing new code — as a cleanup pass
- During code review — to suggest concrete simplifications
- When touching old code — opportunistic improvement
- When the user says "clean this up", "simplify", "refactor", or "make this clearer"
- When code has accumulated complexity over multiple iterations

## When NOT to Use

- Performance-critical hot paths where "clever" code is justified and documented
- Generated code that shouldn't be manually modified
- Code that is about to be deleted or replaced
- When the user explicitly says "don't refactor" or "leave the structure"
