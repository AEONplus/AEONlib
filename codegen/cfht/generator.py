#!/usr/bin/env python3
import sys
from typing import Any

import httpx
import yaml
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

OPENAPI_SPEC_URL = "https://hou-stage.cfht.hawaii.edu/api-docs/pi_api.yaml"
GENERATED_HEADER = "# Auto generated file, do not edit\n# ruff: noqa: E741\n"


def generate_models(openapi_document: dict[str, Any]) -> str:
    config = GenerateConfig(
        input_file_type=InputFileType.OpenAPI,
        input_filename="cfhtopenapi.yaml",
        openapi_scopes=[OpenAPIScope.Schemas],
        output_model_type=DataModelType.PydanticV2BaseModel,
        base_class="aeonlib.cfht.base_model.CFHTBaseModel",
        target_pydantic_version=TargetPydanticVersion.V2_11,
        use_annotated=True,
        field_constraints=True,
        set_default_enum_member=True,
        snake_case_field=True,
        allow_population_by_field_name=True,
        type_overrides={"DoubleValue": "aeonlib.cfht.types.DoubleValue"},
        formatters=[Formatter.BUILTIN],
    )

    result = generate(openapi_document, config=config)
    if not isinstance(result, str):
        raise TypeError(
            "Expected string output from datamodel-code-generator "
            f"got {type(result).__name__}."
        )

    return GENERATED_HEADER + result + "\n"


def main() -> int:
    response = httpx.get(OPENAPI_SPEC_URL)
    response.raise_for_status()
    document = yaml.safe_load(response.content)
    generated = generate_models(document)
    _ = sys.stdout.write(generated)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (yaml.YAMLError, DataModelCodegenError, OSError, TypeError) as exc:
        print(f"CFHT model generation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
