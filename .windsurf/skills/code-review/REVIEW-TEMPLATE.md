---

## 📄 `REVIEW-TEMPLATE.md` — Code Review Checklist (AI-Assisted)

```md
# Code Review Template

## Summary
- What problem does this change solve?
- Is this the right level of abstraction?

---

## Architecture
- [ ] Responsibilities are clearly separated
- [ ] No cross-layer leakage
- [ ] Design aligns with existing patterns

---

## Correctness
- [ ] Logic matches requirements
- [ ] Edge cases handled
- [ ] No dead or unused code

---

## Readability & Maintainability
- [ ] Code is easy to follow
- [ ] Naming is clear and consistent
- [ ] No unnecessary indirection

---

## Typing & Interfaces
- [ ] Public APIs are typed
- [ ] Models are explicit
- [ ] No misleading types

---

## Error Handling & Logging
- [ ] Errors are handled intentionally
- [ ] Logs add diagnostic value
- [ ] No silent failures

---

## Security
- [ ] Input validation present
- [ ] AuthZ/AuthN boundaries respected
- [ ] No secrets or insecure defaults

---

## Performance
- [ ] No obvious inefficiencies
- [ ] Async used correctly (if applicable)
- [ ] No premature optimization

---

## AI-Specific Checks
- [ ] No hallucinated APIs or libraries
- [ ] AI verbosity reduced
- [ ] Generated code aligns with project style

---

## Tests & Docs
- [ ] Tests cover meaningful behavior
- [ ] Docs explain non-obvious decisions

---

## Final Verdict
- [ ] Approve
- [ ] Approve with comments
- [ ] Request changes
