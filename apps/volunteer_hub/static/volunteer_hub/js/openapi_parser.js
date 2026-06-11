function deepClone(value) {
    return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}

function decodePointerToken(token) {
    return token.replace(/~1/g, "/").replace(/~0/g, "~");
}

export function resolvePointer(schema, ref) {
    if (!ref || typeof ref !== "string" || !ref.startsWith("#/")) {
        return {};
    }

    const parts = ref.slice(2).split("/").map(decodePointerToken);
    let current = schema;

    for (const part of parts) {
        if (!current || typeof current !== "object" || !(part in current)) {
            return {};
        }
        current = current[part];
    }

    return deepClone(current);
}

function mergeRequired(base = [], extra = []) {
    return Array.from(new Set([...(base || []), ...(extra || [])]));
}

function mergeAllOf(schema, node, seenRefs) {
    const combined = {
        type: "object",
        properties: {},
        required: [],
    };

    for (const part of node.allOf || []) {
        const normalized = normalizeSchemaNode(schema, part, seenRefs);
        if (normalized.properties) {
            Object.assign(combined.properties, normalized.properties);
        }
        combined.required = mergeRequired(combined.required, normalized.required || []);
    }

    for (const [key, value] of Object.entries(node)) {
        if (key !== "allOf") {
            combined[key] = value;
        }
    }

    return combined;
}

export function normalizeSchemaNode(schema, node, seenRefs = new Set()) {
    if (!node || typeof node !== "object") {
        return { type: "object", properties: {} };
    }

    if (node.$ref) {
        if (seenRefs.has(node.$ref)) {
            return { type: "object", properties: {} };
        }
        const nextSeen = new Set(seenRefs);
        nextSeen.add(node.$ref);
        const resolved = resolvePointer(schema, node.$ref);
        return normalizeSchemaNode(schema, resolved, nextSeen);
    }

    if (node.allOf) {
        return normalizeSchemaNode(schema, mergeAllOf(schema, node, seenRefs), seenRefs);
    }

    if (node.oneOf && node.oneOf.length > 0) {
        return normalizeSchemaNode(schema, node.oneOf[0], seenRefs);
    }

    if (node.anyOf && node.anyOf.length > 0) {
        return normalizeSchemaNode(schema, node.anyOf[0], seenRefs);
    }

    const normalized = deepClone(node);

    if (normalized.properties && typeof normalized.properties === "object") {
        for (const [prop, child] of Object.entries(normalized.properties)) {
            normalized.properties[prop] = normalizeSchemaNode(schema, child, seenRefs);
        }
    }

    if (normalized.items) {
        normalized.items = normalizeSchemaNode(schema, normalized.items, seenRefs);
    }

    return normalized;
}

function pickRequestContent(content) {
    if (content["application/json"]) {
        return ["application/json", content["application/json"]];
    }

    const firstType = Object.keys(content || {})[0];
    if (firstType) {
        return [firstType, content[firstType]];
    }

    return ["application/json", { schema: { type: "object", properties: {} } }];
}

export function parseOpenApiPostEndpoints(schema) {
    const result = [];
    const paths = schema?.paths || {};

    for (const [path, pathItem] of Object.entries(paths)) {
        if (!pathItem?.post) {
            continue;
        }

        const operation = pathItem.post;
        const content = operation?.requestBody?.content || {};
        const [mediaType, mediaConfig] = pickRequestContent(content);
        const rawSchema = mediaConfig?.schema || { type: "object", properties: {} };

        result.push({
            path,
            method: "POST",
            summary: operation.summary || operation.description || path,
            operationId: operation.operationId || null,
            tags: operation.tags || [],
            mediaType,
            schema: normalizeSchemaNode(schema, rawSchema),
        });
    }

    return result;
}
