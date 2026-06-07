from __future__ import annotations

from copy import deepcopy
from typing import Any


class OpenApiPostParser:
    """Parses an OpenAPI schema dictionary and extracts POST endpoint payload schemas."""

    def __init__(self, schema: dict[str, Any]):
        self.schema = schema

    def parse_post_endpoints(self) -> list[dict[str, Any]]:
        endpoints: list[dict[str, Any]] = []
        paths = self.schema.get("paths", {})

        for path, path_item in paths.items():
            post_operation = (path_item or {}).get("post")
            if not post_operation:
                continue

            request_body = post_operation.get("requestBody", {})
            content = request_body.get("content", {})
            media_type = self._pick_media_type(content)
            schema_node = (content.get(media_type) or {}).get("schema", {})

            endpoints.append(
                {
                    "path": path,
                    "operation_id": post_operation.get("operationId"),
                    "summary": post_operation.get("summary") or post_operation.get("description") or path,
                    "tags": post_operation.get("tags", []),
                    "media_type": media_type,
                    "schema": self._normalize_schema(schema_node),
                }
            )

        return endpoints

    def _pick_media_type(self, content: dict[str, Any]) -> str:
        if "application/json" in content:
            return "application/json"
        if content:
            return next(iter(content.keys()))
        return "application/json"

    def _normalize_schema(self, schema_node: dict[str, Any]) -> dict[str, Any]:
        if not schema_node:
            return {"type": "object", "properties": {}}

        resolved = self._resolve_refs(schema_node)
        if "allOf" in resolved:
            resolved = self._merge_all_of(resolved)

        # Keep parser output predictable for dynamic UI rendering.
        if resolved.get("type") != "object" and "properties" not in resolved:
            return {"type": "object", "properties": {"value": resolved}, "required": ["value"]}

        return resolved

    def _resolve_refs(self, value: Any, seen: set[str] | None = None) -> Any:
        if seen is None:
            seen = set()

        if isinstance(value, list):
            return [self._resolve_refs(item, seen) for item in value]

        if not isinstance(value, dict):
            return value

        if "$ref" in value:
            ref = value["$ref"]
            if ref in seen:
                return {}
            seen_with_ref = set(seen)
            seen_with_ref.add(ref)
            target = self._resolve_pointer(ref)
            return self._resolve_refs(target, seen_with_ref)

        return {key: self._resolve_refs(item, seen) for key, item in value.items()}

    def _resolve_pointer(self, ref: str) -> Any:
        if not ref.startswith("#/"):
            return {}

        pointer_parts = ref[2:].split("/")
        current: Any = self.schema

        for part in pointer_parts:
            token = part.replace("~1", "/").replace("~0", "~")
            if not isinstance(current, dict) or token not in current:
                return {}
            current = current[token]

        return deepcopy(current)

    def _merge_all_of(self, schema_node: dict[str, Any]) -> dict[str, Any]:
        merged: dict[str, Any] = {"type": "object", "properties": {}, "required": []}

        for item in schema_node.get("allOf", []):
            resolved_item = self._resolve_refs(item)
            if "allOf" in resolved_item:
                resolved_item = self._merge_all_of(resolved_item)

            for key, value in resolved_item.get("properties", {}).items():
                merged["properties"][key] = value

            for field in resolved_item.get("required", []):
                if field not in merged["required"]:
                    merged["required"].append(field)

        for key, value in schema_node.items():
            if key == "allOf":
                continue
            merged[key] = value

        return merged
