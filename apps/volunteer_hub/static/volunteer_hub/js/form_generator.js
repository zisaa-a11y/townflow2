import { parseOpenApiPostEndpoints } from "./openapi_parser.js";

const scriptTag = document.currentScript;
const schemaUrl = scriptTag?.dataset?.schemaUrl || "/api/schema/";
const container = document.getElementById("post-endpoints-container");
const globalAlert = document.getElementById("global-alert");
const authTokenInput = document.getElementById("auth-token");
const AUTH_TOKEN_STORAGE_KEY = "openapi_form_generator_bearer_token";

const endpointStates = new Map();

function showGlobalAlert(message, variant = "danger") {
    globalAlert.textContent = message;
    globalAlert.className = `alert alert-${variant}`;
}

function getCsrfToken() {
    const cookies = document.cookie ? document.cookie.split(";") : [];
    for (const rawCookie of cookies) {
        const cookie = rawCookie.trim();
        if (cookie.startsWith("csrftoken=")) {
            return decodeURIComponent(cookie.slice("csrftoken=".length));
        }
    }
    return "";
}

function sanitizeForId(value) {
    return String(value).replace(/[^a-zA-Z0-9_-]/g, "_");
}

function normalizeBearerToken(rawToken) {
    if (!rawToken) {
        return "";
    }

    // Remove accidental quotes/backticks and any whitespace/newlines from copy-paste.
    return String(rawToken)
        .replace(/^\s*["'`]+|["'`]+\s*$/g, "")
        .replace(/\s+/g, "")
        .trim();
}

function getBearerToken() {
    return normalizeBearerToken(authTokenInput?.value || "");
}

function applyBearerToken(token) {
    const normalized = normalizeBearerToken(token);
    if (!authTokenInput) {
        return normalized;
    }

    authTokenInput.value = normalized;
    if (normalized) {
        window.localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, normalized);
    } else {
        window.localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
    }
    return normalized;
}

function extractAccessTokenFromResponse(data) {
    if (!data || typeof data !== "object") {
        return "";
    }

    const candidatePaths = [
        "access",
        "token",
        "data.access",
        "data.token",
        "tokens.access",
        "data.tokens.access",
    ];

    for (const path of candidatePaths) {
        const candidate = getByPath(data, path);
        if (typeof candidate === "string" && candidate.trim()) {
            return candidate;
        }
    }

    return "";
}

function shouldAttachBearerToken(path) {
    if (!path) {
        return true;
    }

    // Public auth endpoints should not receive Authorization header.
    const skipPaths = [
        "/api/v1/auth/login/",
        "/api/v1/auth/register/",
        "/api/v1/auth/signup/",
        "/api/v1/auth/refresh/",
        "/api/v1/auth/token/refresh/",
    ];

    return !skipPaths.includes(path);
}

function createElement(tag, className, text) {
    const el = document.createElement(tag);
    if (className) {
        el.className = className;
    }
    if (text !== undefined) {
        el.textContent = text;
    }
    return el;
}

function setByPath(target, path, value) {
    const keys = path.split(".");
    let cursor = target;

    keys.forEach((key, index) => {
        const isLast = index === keys.length - 1;
        if (isLast) {
            cursor[key] = value;
            return;
        }
        if (typeof cursor[key] !== "object" || cursor[key] === null || Array.isArray(cursor[key])) {
            cursor[key] = {};
        }
        cursor = cursor[key];
    });
}

function getByPath(source, path) {
    const keys = path.split(".");
    let cursor = source;

    for (const key of keys) {
        if (cursor === null || cursor === undefined || typeof cursor !== "object") {
            return undefined;
        }
        cursor = cursor[key];
    }

    return cursor;
}

function inferDefault(schema) {
    if (schema.default !== undefined) {
        return schema.default;
    }
    if (schema.enum && schema.enum.length) {
        return schema.enum[0];
    }

    switch (schema.type) {
        case "boolean":
            return false;
        case "integer":
        case "number":
            return null;
        case "array":
            return [];
        case "object": {
            const nested = {};
            const properties = schema.properties || {};
            for (const [key, propSchema] of Object.entries(properties)) {
                nested[key] = inferDefault(propSchema || {});
            }
            return nested;
        }
        default:
            return "";
    }
}

function parsePrimitiveValue(rawValue, schema) {
    if (rawValue === "" || rawValue === null || rawValue === undefined) {
        if (schema?.nullable || schema?.format === "uuid") {
            return null;
        }
        if (!schema || schema.type === "string") {
            return "";
        }
        return null;
    }

    if (schema.type === "integer") {
        const parsed = Number.parseInt(rawValue, 10);
        return Number.isNaN(parsed) ? null : parsed;
    }

    if (schema.type === "number") {
        const parsed = Number.parseFloat(rawValue);
        return Number.isNaN(parsed) ? null : parsed;
    }

    if (schema.type === "boolean") {
        return Boolean(rawValue);
    }

    return rawValue;
}

function parseArrayInput(rawValue, itemSchema) {
    if (!rawValue || !rawValue.trim()) {
        return [];
    }

    if (itemSchema?.type === "object" || itemSchema?.type === "array") {
        try {
            const parsed = JSON.parse(rawValue);
            return Array.isArray(parsed) ? parsed : [];
        } catch (error) {
            return [];
        }
    }

    return rawValue
        .split(",")
        .map((part) => part.trim())
        .filter((part) => part.length > 0)
        .map((item) => parsePrimitiveValue(item, itemSchema || { type: "string" }));
}

function renderSchemaFields({
    mountPoint,
    schema,
    pathPrefix,
    controlRegistry,
    endpointIndex,
}) {
    if (!schema || typeof schema !== "object") {
        return;
    }

    const requiredSet = new Set(schema.required || []);
    const properties = schema.properties || {};

    for (const [name, fieldSchema] of Object.entries(properties)) {
        if (fieldSchema?.readOnly) {
            continue;
        }

        const fieldPath = pathPrefix ? `${pathPrefix}.${name}` : name;
        const isRequired = requiredSet.has(name);
        const labelText = `${name}${isRequired ? " *" : ""}`;
        const wrapper = createElement("div", "mb-3");
        const type = fieldSchema?.type || "string";

        if (type === "object" || fieldSchema?.properties) {
            const fieldset = createElement("fieldset", "nested-fieldset mb-2");
            const legend = createElement("legend", "nested-legend", labelText);
            fieldset.appendChild(legend);
            renderSchemaFields({
                mountPoint: fieldset,
                schema: { type: "object", ...fieldSchema },
                pathPrefix: fieldPath,
                controlRegistry,
                endpointIndex,
            });
            wrapper.appendChild(fieldset);
            mountPoint.appendChild(wrapper);
            continue;
        }

        const label = createElement("label", "form-label", labelText);
        const controlId = `endpoint_${endpointIndex}_${sanitizeForId(fieldPath)}`;
        label.htmlFor = controlId;

        let input;

        if (fieldSchema?.enum?.length) {
            input = createElement("select", "form-select");
            input.id = controlId;
            input.appendChild(new Option("Select...", ""));
            fieldSchema.enum.forEach((optionValue) => {
                input.appendChild(new Option(String(optionValue), String(optionValue)));
            });
        } else if (type === "boolean") {
            const checkWrap = createElement("div", "form-check");
            input = createElement("input", "form-check-input");
            input.type = "checkbox";
            input.id = controlId;
            input.checked = Boolean(fieldSchema.default);

            const checkLabel = createElement("label", "form-check-label", labelText);
            checkLabel.htmlFor = controlId;
            checkWrap.appendChild(input);
            checkWrap.appendChild(checkLabel);
            wrapper.appendChild(checkWrap);
            mountPoint.appendChild(wrapper);

            controlRegistry[fieldPath] = {
                input,
                schema: fieldSchema,
                type,
                isRequired,
            };
            continue;
        } else if (type === "array") {
            input = createElement("textarea", "form-control");
            input.id = controlId;
            input.rows = 3;
            const itemType = fieldSchema?.items?.type || "string";
            input.placeholder = itemType === "object"
                ? "Enter JSON array, e.g. [{\"name\":\"value\"}]"
                : "Comma-separated values, e.g. one,two,three";
        } else {
            input = createElement("input", "form-control");
            input.id = controlId;
            input.type = (type === "integer" || type === "number") ? "number" : "text";
            if (type === "number") {
                input.step = "any";
            }
        }

        if (isRequired) {
            input.required = true;
        }

        if (fieldSchema?.description) {
            const helpText = createElement("div", "form-text", fieldSchema.description);
            wrapper.appendChild(label);
            wrapper.appendChild(input);
            wrapper.appendChild(helpText);
        } else {
            wrapper.appendChild(label);
            wrapper.appendChild(input);
        }

        mountPoint.appendChild(wrapper);

        controlRegistry[fieldPath] = {
            input,
            schema: fieldSchema,
            type,
            isRequired,
        };
    }
}

function readPayloadFromForm(controlRegistry) {
    const payload = {};

    for (const [path, item] of Object.entries(controlRegistry)) {
        const { input, schema, type } = item;
        let value;

        if (type === "boolean") {
            value = input.checked;
        } else if (type === "array") {
            value = parseArrayInput(input.value, schema?.items || {});
        } else if (schema?.enum?.length) {
            value = input.value === "" ? null : parsePrimitiveValue(input.value, schema);
        } else {
            value = parsePrimitiveValue(input.value, schema || { type: "string" });
        }

        setByPath(payload, path, value);
    }

    return payload;
}

function applyPayloadToForm(controlRegistry, payload) {
    for (const [path, item] of Object.entries(controlRegistry)) {
        const value = getByPath(payload, path);
        const { input, schema, type } = item;

        if (type === "boolean") {
            input.checked = Boolean(value);
            continue;
        }

        if (type === "array") {
            if (!Array.isArray(value)) {
                input.value = "";
                continue;
            }
            if (schema?.items?.type === "object" || schema?.items?.type === "array") {
                input.value = JSON.stringify(value, null, 2);
            } else {
                input.value = value.join(",");
            }
            continue;
        }

        if (value === null || value === undefined) {
            input.value = "";
        } else {
            input.value = String(value);
        }
    }
}

function cleanupPayload(value) {
    if (Array.isArray(value)) {
        return value.map(cleanupPayload);
    }

    if (value && typeof value === "object") {
        const cleaned = {};
        for (const [key, nested] of Object.entries(value)) {
            cleaned[key] = cleanupPayload(nested);
        }
        return cleaned;
    }

    return value;
}

function prettyJson(value) {
    return JSON.stringify(value, null, 2);
}

function extractPathParams(path) {
    return Array.from(path.matchAll(/\{([^}]+)\}/g)).map((match) => match[1]);
}

function flattenDrfErrors(errorValue, prefix = "") {
    if (Array.isArray(errorValue)) {
        return errorValue.flatMap((item) => flattenDrfErrors(item, prefix));
    }

    if (errorValue && typeof errorValue === "object") {
        const lines = [];
        for (const [key, value] of Object.entries(errorValue)) {
            const nextPrefix = prefix ? `${prefix}.${key}` : key;
            lines.push(...flattenDrfErrors(value, nextPrefix));
        }
        return lines;
    }

    if (errorValue === null || errorValue === undefined || errorValue === "") {
        return [];
    }

    return [prefix ? `${prefix}: ${errorValue}` : String(errorValue)];
}

function buildEndpointCard(endpoint, endpointIndex) {
    const card = createElement("section", "card endpoint-card");
    const body = createElement("div", "card-body");

    const title = createElement("h2", "h5 mb-2", endpoint.summary || endpoint.path);
    const subline = createElement("div", "d-flex flex-wrap gap-2 align-items-center mb-3");
    const methodBadge = createElement("span", "badge text-bg-primary", endpoint.method);
    const pathBadge = createElement("span", "badge text-bg-light border path-pill", endpoint.path);
    const mediaTypeBadge = createElement("span", "badge text-bg-secondary", endpoint.mediaType);
    subline.appendChild(methodBadge);
    subline.appendChild(pathBadge);
    subline.appendChild(mediaTypeBadge);

    const modeWrap = createElement("div", "btn-group btn-group-sm mb-3");
    modeWrap.role = "group";

    const formModeId = `mode_form_${endpointIndex}`;
    const jsonModeId = `mode_json_${endpointIndex}`;

    const formModeInput = createElement("input", "btn-check");
    formModeInput.type = "radio";
    formModeInput.name = `mode_${endpointIndex}`;
    formModeInput.id = formModeId;
    formModeInput.checked = true;

    const formModeLabel = createElement("label", "btn btn-outline-primary", "Form Mode");
    formModeLabel.htmlFor = formModeId;

    const jsonModeInput = createElement("input", "btn-check");
    jsonModeInput.type = "radio";
    jsonModeInput.name = `mode_${endpointIndex}`;
    jsonModeInput.id = jsonModeId;

    const jsonModeLabel = createElement("label", "btn btn-outline-primary", "JSON Mode");
    jsonModeLabel.htmlFor = jsonModeId;

    modeWrap.appendChild(formModeInput);
    modeWrap.appendChild(formModeLabel);
    modeWrap.appendChild(jsonModeInput);
    modeWrap.appendChild(jsonModeLabel);

    const formModeWrap = createElement("div", "form-mode-wrap");
    const jsonModeWrap = createElement("div", "json-mode-wrap d-none");

    const formElement = createElement("form", "");
    formElement.noValidate = true;
    const controlRegistry = {};

    const schemaRoot = endpoint.schema?.type === "object"
        ? endpoint.schema
        : { type: "object", properties: { value: endpoint.schema }, required: ["value"] };

    renderSchemaFields({
        mountPoint: formElement,
        schema: schemaRoot,
        pathPrefix: "",
        controlRegistry,
        endpointIndex,
    });

    const pathParams = extractPathParams(endpoint.path);
    const pathParamInputs = {};
    if (pathParams.length) {
        const pathParamsTitle = createElement("h3", "h6 mt-2", "Path Parameters");
        formElement.prepend(pathParamsTitle);

        pathParams.forEach((paramName) => {
            const wrapper = createElement("div", "mb-3");
            const label = createElement("label", "form-label", `${paramName} *`);
            const paramId = `endpoint_${endpointIndex}_path_${sanitizeForId(paramName)}`;
            label.htmlFor = paramId;

            const input = createElement("input", "form-control");
            input.id = paramId;
            input.required = true;
            input.placeholder = `Value for ${paramName}`;

            wrapper.appendChild(label);
            wrapper.appendChild(input);
            formElement.prepend(wrapper);
            pathParamInputs[paramName] = input;
        });
    }

    const jsonEditor = createElement("textarea", "form-control json-editor");
    jsonEditor.spellcheck = false;

    const defaultPayload = cleanupPayload(inferDefault(schemaRoot));
    jsonEditor.value = prettyJson(defaultPayload);
    applyPayloadToForm(controlRegistry, defaultPayload);

    formModeWrap.appendChild(formElement);
    jsonModeWrap.appendChild(jsonEditor);

    const validationList = createElement("ul", "small text-danger mb-2 d-none");
    const submitButton = createElement("button", "btn btn-success", "Submit POST Request");
    submitButton.type = "button";

    const responseTitle = createElement("h3", "h6 mt-3 mb-2", "Response");
    const responseMeta = createElement("div", "small text-secondary mb-2", "No request sent yet.");
    const responseBox = createElement("pre", "response-box", "");

    body.appendChild(title);
    body.appendChild(subline);
    body.appendChild(modeWrap);
    body.appendChild(formModeWrap);
    body.appendChild(jsonModeWrap);
    body.appendChild(validationList);
    body.appendChild(submitButton);
    body.appendChild(responseTitle);
    body.appendChild(responseMeta);
    body.appendChild(responseBox);
    card.appendChild(body);

    const state = {
        endpoint,
        controlRegistry,
        pathParamInputs,
        jsonEditor,
        validationList,
        responseMeta,
        responseBox,
        syncingFromJson: false,
        syncingFromForm: false,
    };

    function syncJsonFromForm() {
        if (state.syncingFromJson) {
            return;
        }

        state.syncingFromForm = true;
        const payload = cleanupPayload(readPayloadFromForm(state.controlRegistry));
        state.jsonEditor.classList.remove("is-invalid");
        state.jsonEditor.value = prettyJson(payload);
        state.syncingFromForm = false;
    }

    function syncFormFromJson() {
        if (state.syncingFromForm) {
            return;
        }

        try {
            const parsed = JSON.parse(state.jsonEditor.value || "{}");
            state.syncingFromJson = true;
            applyPayloadToForm(state.controlRegistry, parsed || {});
            state.jsonEditor.classList.remove("is-invalid");
            state.syncingFromJson = false;
        } catch (error) {
            state.jsonEditor.classList.add("is-invalid");
        }
    }

    formElement.addEventListener("input", syncJsonFromForm);
    formElement.addEventListener("change", syncJsonFromForm);

    let jsonDebounce = null;
    jsonEditor.addEventListener("input", () => {
        window.clearTimeout(jsonDebounce);
        jsonDebounce = window.setTimeout(syncFormFromJson, 220);
    });

    formModeInput.addEventListener("change", () => {
        formModeWrap.classList.remove("d-none");
        jsonModeWrap.classList.add("d-none");
        syncJsonFromForm();
    });

    jsonModeInput.addEventListener("change", () => {
        syncJsonFromForm();
        formModeWrap.classList.add("d-none");
        jsonModeWrap.classList.remove("d-none");
    });

    submitButton.addEventListener("click", async () => {
        validationList.classList.add("d-none");
        validationList.innerHTML = "";

        let payload;
        try {
            payload = JSON.parse(jsonEditor.value || "{}");
            jsonEditor.classList.remove("is-invalid");
        } catch (error) {
            jsonEditor.classList.add("is-invalid");
            responseMeta.textContent = "JSON payload is invalid.";
            responseBox.textContent = String(error.message || error);
            return;
        }

        let url = endpoint.path;
        for (const [paramName, input] of Object.entries(pathParamInputs)) {
            const rawValue = input.value.trim();
            if (!rawValue) {
                responseMeta.textContent = `Path parameter '${paramName}' is required.`;
                responseBox.textContent = "Please fill all path parameters before submitting.";
                return;
            }
            url = url.replace(`{${paramName}}`, encodeURIComponent(rawValue));
        }

        const csrfToken = getCsrfToken();
        const headers = {
            "Content-Type": endpoint.mediaType || "application/json",
            Accept: "application/json",
        };

        if (csrfToken) {
            headers["X-CSRFToken"] = csrfToken;
        }

        const bearerToken = getBearerToken();
        if (bearerToken && shouldAttachBearerToken(endpoint.path)) {
            headers.Authorization = `Bearer ${bearerToken}`;
        }

        try {
            submitButton.disabled = true;
            submitButton.textContent = "Submitting...";

            const response = await fetch(url, {
                method: "POST",
                headers,
                body: JSON.stringify(payload),
                credentials: "same-origin",
            });

            const contentType = response.headers.get("content-type") || "";
            const data = contentType.includes("json")
                ? await response.json()
                : await response.text();

            responseMeta.textContent = `Status: ${response.status} ${response.statusText}`;
            responseBox.textContent = typeof data === "string" ? data : prettyJson(data);

            const accessFromResponse = extractAccessTokenFromResponse(data);
            if (accessFromResponse) {
                applyBearerToken(accessFromResponse);
                responseMeta.textContent = `${responseMeta.textContent} | Access token applied to Bearer Token box`;
            }

            if (!response.ok && data && typeof data === "object") {
                const flattenedErrors = flattenDrfErrors(data);
                if (flattenedErrors.length) {
                    validationList.classList.remove("d-none");
                    flattenedErrors.forEach((line) => {
                        const li = createElement("li", "", line);
                        validationList.appendChild(li);
                    });
                }
            }
        } catch (error) {
            responseMeta.textContent = "Request failed";
            responseBox.textContent = String(error.message || error);
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Submit POST Request";
        }
    });

    endpointStates.set(endpointIndex, state);
    return card;
}

async function loadOpenApiSchema() {
    try {
        const response = await fetch(schemaUrl, {
            headers: {
                Accept: "application/vnd.oai.openapi+json, application/json;q=0.9",
            },
            credentials: "same-origin",
        });

        if (!response.ok) {
            throw new Error(`Schema fetch failed with ${response.status}`);
        }

        const schema = await response.json();
        const postEndpoints = parseOpenApiPostEndpoints(schema);

        if (!postEndpoints.length) {
            showGlobalAlert("No POST endpoints found in the OpenAPI schema.", "warning");
            return;
        }

        globalAlert.className = "alert alert-success";
        globalAlert.textContent = `Loaded ${postEndpoints.length} POST endpoints from ${schemaUrl}.`;

        postEndpoints.forEach((endpoint, index) => {
            const card = buildEndpointCard(endpoint, index);
            container.appendChild(card);
        });
    } catch (error) {
        showGlobalAlert(`Unable to initialize form generator: ${error.message || error}`, "danger");
    }
}

if (authTokenInput) {
    const savedToken = window.localStorage.getItem(AUTH_TOKEN_STORAGE_KEY) || "";
    if (savedToken) {
        authTokenInput.value = savedToken;
    }

    authTokenInput.addEventListener("input", () => {
        applyBearerToken(authTokenInput.value);
    });

    authTokenInput.addEventListener("blur", () => {
        applyBearerToken(authTokenInput.value);
    });
}

loadOpenApiSchema();
