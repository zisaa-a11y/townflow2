# FORM_GENERATOR.md

## Project Overview

The OpenAPI Form Generator is a server-rendered Django page that discovers all POST APIs from DRF Spectacular schema output (`/api/schema/`) and creates one interactive Bootstrap 5 card per endpoint.

It supports:

- Dynamic endpoint discovery (no hardcoded endpoint list)
- Dynamic payload field generation from `requestBody` schema
- Supported field types: string, integer, float/number, boolean, enum, array, nested object
- Form Mode and JSON Mode with two-way synchronization
- Live request submission to real API endpoints
- Response and DRF validation error display

Primary URL:

- `/api/v1/volunteer-hub/form-generator/`

---

## Architecture Explanation

The feature has 4 layers:

1. Django Route Layer
- Adds a URL for the form generator page.
- Keeps existing DRF router endpoints unchanged.

2. Django View Layer
- Serves a template and injects `schema_url` from Django URL reversing.
- Template does not hardcode schema path directly.

3. OpenAPI Parsing Layer
- JavaScript parser (`openapi_parser.js`) fetches and parses `/api/schema/`.
- Detects all POST operations from `paths`.
- Resolves `$ref`, `allOf`, `oneOf`, and `anyOf` for request schemas.
- Python parser utility (`openapi_parser.py`) is provided for backend reuse/testing.

4. Dynamic UI/Submission Layer
- Generates cards and controls from parsed schema.
- Synchronizes Form Mode and JSON Mode.
- Sends real POST requests to selected endpoint URLs.
- Displays success/error payloads and flattened DRF validation errors.

---

## Folder Structure

New/updated files:

- `apps/volunteer_hub/urls.py` (updated)
- `apps/volunteer_hub/views.py` (updated)
- `apps/volunteer_hub/openapi_parser.py` (new)
- `apps/volunteer_hub/templates/volunteer_hub/form_generator.html` (new)
- `apps/volunteer_hub/static/volunteer_hub/js/openapi_parser.js` (new)
- `apps/volunteer_hub/static/volunteer_hub/js/form_generator.js` (new)
- `FORM_GENERATOR.md` (new)

---

## Installation Steps

1. Pull latest code.
2. Ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

3. Apply migrations if required (not required for this feature itself):

```bash
python manage.py migrate
```

4. Collect static files for production:

```bash
python manage.py collectstatic --noinput
```

5. Restart application service (Gunicorn/uWSGI/Passenger, depending on your deployment).

---

## Configuration Instructions

1. Ensure DRF Spectacular schema endpoint is enabled in `config/urls.py`:
- `/api/schema/`

2. Ensure static files are served correctly in production:
- `STATIC_ROOT`
- web server static mapping

3. Optional authentication:
- If APIs require bearer token, use the `Bearer Token` input on the page.
- If session auth is used, CSRF token is sent automatically via cookie extraction.

4. Access page:
- `/api/v1/volunteer-hub/form-generator/`

---

## How Schema Parsing Works

### Data Source

The frontend fetches schema from:

- `/api/schema/`

with `Accept: application/vnd.oai.openapi+json, application/json`.

### POST Endpoint Detection

Algorithm:

1. Read `schema.paths`.
2. For each path item, check if `post` exists.
3. Extract:
- `path`
- `summary` / `description`
- `operationId`
- `tags`
- request body content type (prefer `application/json`)
- request body schema

### Schema Normalization

The parser resolves and normalizes:

- `$ref`: JSON pointer resolution from `#/components/...`
- `allOf`: merged into single object shape
- `oneOf` / `anyOf`: first branch fallback for rendering compatibility
- nested `properties` and `items`

Output is a consistent schema object suitable for recursive field rendering.

---

## How Dynamic Form Generation Works

For each POST endpoint, the UI creates one card containing:

- Endpoint metadata badges (method, path, media type)
- Mode toggle (Form Mode / JSON Mode)
- Form section generated recursively from schema
- JSON editor section
- Submit button
- Response panel + validation list

### Field Type Mapping

- `string` -> text input
- `integer` -> number input (integer)
- `number` -> number input (`step=any`)
- `boolean` -> checkbox
- `enum` -> select dropdown
- `array` -> textarea
- primitive array: comma-separated values
- object/array of objects: JSON array input
- `object` / nested object -> grouped fieldset rendered recursively

### Path Parameters

If endpoint path includes placeholders like `/items/{id}/action/`, dynamic path parameter inputs are generated and substituted before request submission.

---

## How Form Mode and JSON Mode Synchronization Works

Two-way synchronization logic:

1. Form -> JSON
- Every form `input/change` event rebuilds payload object from controls.
- JSON textarea is updated with pretty-printed payload.

2. JSON -> Form
- JSON editor input is debounced.
- Valid JSON updates corresponding form controls by path.
- Invalid JSON marks the editor invalid but does not break the UI.

3. Mode Toggle
- Form Mode shows form controls.
- JSON Mode shows JSON editor.
- Data remains synchronized regardless of mode switch.

This guarantees a single consistent payload representation.

---

## How to Add New APIs

No code change is required for most POST APIs.

When a new POST endpoint is added to DRF and appears in Spectacular schema:

1. Add serializer/viewset/view as usual.
2. Ensure request body schema is documented.
3. Refresh `/api/v1/volunteer-hub/form-generator/`.
4. New endpoint card appears automatically.

Best practice for maximum compatibility:

- Prefer clear serializer field definitions.
- Avoid ambiguous schema definitions when possible.
- Use explicit requestBody for custom APIViews.

---

## Troubleshooting

### 1. "Unable to initialize form generator"

Possible causes:

- `/api/schema/` not reachable
- Auth/network/proxy issue
- Schema returned as non-JSON for the request

Checks:

- Open `/api/schema/` directly
- Verify response status and content-type
- Check browser network panel

### 2. No cards shown

Possible causes:

- No POST endpoints in schema
- POST operations missing requestBody

Checks:

- Inspect schema `paths` for `post`
- Ensure DRF Spectacular correctly documents your POST APIs

### 3. Request returns 403 CSRF

- Confirm `csrftoken` cookie exists (session-auth use case)
- Ensure CSRF trusted origins are configured correctly
- If token auth is used, provide Bearer token

### 4. Validation errors not clear

- DRF errors are flattened recursively and shown as a list.
- Check raw response block for full nested payload.

### 5. Path parameter endpoints fail

- Fill generated path parameter inputs before submitting.
- Ensure parameter format (UUID/int/slug) is valid.

### 6. Static files not loading in production

- Run `collectstatic`
- Confirm web server static mapping to `STATIC_ROOT`
- Verify browser can load JS assets under `/static/`

---

## Example Screenshots / Placeholders

Replace placeholders below with real screenshots from your environment.

1. Page loaded with endpoint cards

![Form Generator Overview](docs/images/form-generator-overview.png)

2. Form Mode example (nested object + arrays)

![Form Mode Example](docs/images/form-generator-form-mode.png)

3. JSON Mode example

![JSON Mode Example](docs/images/form-generator-json-mode.png)

4. Validation error display example

![Validation Error Example](docs/images/form-generator-errors.png)

If image files are not yet available, keep these paths as placeholders for documentation pipelines.

---

## Future Improvements

1. Add support for multipart/form-data and file uploads.
2. Add request authentication presets (JWT/local storage/session profile).
3. Persist last payload per endpoint in local storage.
4. Add response schema-aware renderer and diff view.
5. Add endpoint search/filter by tag/path/operationId.
6. Add schema version selector for multi-environment testing.
7. Add retry/circuit-breaker UX for unstable endpoints.
8. Add optional backend endpoint that pre-parses schema and caches normalized POST contracts.
9. Add automated frontend tests for parser and sync logic.
10. Add i18n strings for multilingual UI.

---

## Notes for Production Use

- This implementation does not hardcode API endpoint definitions.
- It reads current OpenAPI schema at runtime.
- If schema changes, UI adapts on next page load.
- Security posture depends on endpoint-level authentication/authorization rules already enforced by DRF.
