#!/bin/env sh
set -euxo pipefail
# The CFHT API uses OAS 2.0 use the online Swagger converter to convert to OAS 3.0
curl -L \
    "https://converter.swagger.io/api/convert?url=https://hou-stage.cfht.hawaii.edu/api-docs/piapi_openapiv2.swagger.json" \
    --create-dirs \
    -o build/cfht.openapi3.json

# Generate Pydantic models from the OpenAPI 3.0 spec
datamodel-codegen \
    --input "build/cfht.openapi3.json" \
    --input-file-type openapi \
    --openapi-scopes schemas \
    --output src/aeonlib/cfht/models.py \
    --output-model-type pydantic_v2.BaseModel \
    --snake-case-field \
    --use-annotated \
    --set-default-enum-member \
    --formatters builtin

# Ignore some ruff rules that are not relevant for generated code
sed -i '1s/^/# Auto generated file, do not edit\n# ruff: noqa: E741\n/' src/aeonlib/cfht/models.py
