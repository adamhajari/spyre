# Spyre Improvement Tracker

## Critical Security

- [x] **1. RCE via `eval()`** — `server.py` used `eval("self." + params['output_id'] + "(params)")` in 6 places. Replaced with `_call_output_method()` using `getattr()` + `isidentifier()` validation.
- [x] **2. XSS via unescaped HTML** — `server.py:232` used `df.to_html(escape=False)`. Changed to `escape=True`.
- [x] **3. HTML injection in `getHTML()`** — user-defined `getHTML()` returns unescaped HTML with no sanitization. Document the risk and add a note in the docstring.

## Code Quality

- [ ] **4. Mutable default arguments** — `inputs=[], outputs=[], controls=[]` as default params in `Root.__init__()` and as class variables on `App`. Replace with `None` and assign empty list in body.
- [ ] **5. Deprecated `sys.setdefaultencoding()` hack** — `View.py:8-14` does `importlib.reload(sys)` then calls `sys.setdefaultencoding()`. Remove entirely; unnecessary in Python 3.
- [ ] **6. Broad `except Exception` swallowing errors** — generic try/except around dispatch calls hides actual failures. Narrow to specific exceptions or re-raise.

## Dependencies & Packaging

- [x] **7. No version pins** — `numpy`, `pandas`, `cherrypy`, `jinja2`, `matplotlib` all unpinned. Added lower-bound pins in `setup.py`.
- [x] **8. `six` is a dead dependency** — Python 2 compat lib, unused. Removed from `setup.py`.

## Testing

- [ ] **9. ~19% test coverage** — only 111 lines of tests for 571 lines of core logic. Add edge case tests, security tests, upload tests.
- [ ] **10. CI is dead** — `.travis.yml` targets Python 2.7 and 3.4 (both EOL). Replace with GitHub Actions.

## Misc

- [ ] **11. Deprecated `Site` class** — marked deprecated in `server.py` but never removed.
- [ ] **12. Path traversal risk** — `View.py:55` joins `spinnerFile` to `APP_PATH` without validating the path stays within the directory.
