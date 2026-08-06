#!/usr/bin/env python3
import sys
from typing import Any

import httpx
from datamodel_code_generator import (
    DataModelType,
    Formatter,
    GenerateConfig,
    InputFileType,
    OpenAPIScope,
    TargetPydanticVersion,
    generate,
)
from datamodel_code_generator import (
    Error as DataModelCodegenError,
)

SWAGGER_V2_URL = (
    "https://hou-stage.cfht.hawaii.edu/api-docs/piapi_openapiv2.swagger.json"
)
SWAGGER_CONVERTER_URL = "https://converter.swagger.io/api/convert"

GENERATED_HEADER = "# Auto generated file, do not edit\n# ruff: noqa: E741\n"


def fetch_converted_openapi(swagger_v2_url: str) -> dict[str, Any]:
    response = httpx.get(
        SWAGGER_CONVERTER_URL,
        params={"url": swagger_v2_url},
        timeout=120.0,
        follow_redirects=True,
    )
    response.raise_for_status()
    return response.json()


def normalize_string_int64_to_integer(node: Any) -> None:
    """
    The CFHT spec marks some integer-like fields as:
      {"type": "string", "format": "int64"}
    but the API returns true integers. Normalize schema to integers so that
    the generated pydantic models can be used without schema validation errors.
    """

    if isinstance(node, dict):
        if node.get("type") == "string" and node.get("format") == "int64":
            node["type"] = "integer"

        for value in node.values():
            normalize_string_int64_to_integer(value)

    elif isinstance(node, list):
        for item in node:
            normalize_string_int64_to_integer(item)


def generate_models(openapi_document: dict[str, Any]) -> str:
    config = GenerateConfig(
        input_file_type=InputFileType.OpenAPI,
        input_filename="cfht.openapi3.json",
        openapi_scopes=[OpenAPIScope.Schemas],
        output_model_type=DataModelType.PydanticV2BaseModel,
        base_class="aeonlib.cfht.base_model.CFHTBaseModel",
        target_pydantic_version=TargetPydanticVersion.V2_11,
        use_annotated=True,
        field_constraints=True,
        set_default_enum_member=True,
        snake_case_field=True,
        allow_population_by_field_name=True,
        formatters=[Formatter.BUILTIN],
    )

    result = generate(openapi_document, config=config)
    if not isinstance(result, str):
        raise TypeError(
            "Expected string output from datamodel-code-generator"
            f"got {type(result).__name__}."
        )

    return GENERATED_HEADER + result + "\n"


def main() -> int:
    document = fetch_converted_openapi(SWAGGER_V2_URL)
    normalize_string_int64_to_integer(document)

    generated = generate_models(document)
    _ = sys.stdout.write(generated)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (httpx.HTTPError, DataModelCodegenError, OSError, TypeError) as exc:
        print(f"CFHT model generation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
