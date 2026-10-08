# Ignore undefined attributes for the Django mixin
# mypy: disable-error-code="attr-defined"
# ty: ignore[unresolved-attribute]

from pydantic import BaseModel, TypeAdapter
from pydantic import ValidationError as PydanticValidationError


def omit_none(value):
    """
    Recursively omit None values from dictionaries and lists.
    When django serializes a form, it inserts None values for empty fields. This
    is contrary to what Pydantic expects, which is for the field to not be set at all
    if the default is desired. None is an explicit value.
    """
    if isinstance(value, dict):
        return {key: omit_none(item) for key, item in value.items() if item is not None}
    if isinstance(value, list):
        return [omit_none(item) for item in value]
    return value


class PydanticValidationMixin:
    """Validate django form fields against Pydantic models, enabling re-using
    AEONLib validation logic with Django forms.

    Django fields are bound using the ``pydantic_model`` and ``pydantic_field``
    attributes. See the LCO facility in the TOM Toolkit for an example.
    """

    def _clean_form(self):
        super()._clean_form()
        self.validate_pydantic_fields()

    def validate_pydantic_fields(self):
        """Add Pydantic errors to their bound Django field before _post_clean."""
        from django.core.exceptions import (  # type: ignore[import-not-found, ty:unresolved-import]
            ImproperlyConfigured,
            ValidationError,
        )

        for name, field in self.fields.items():
            if name not in self.cleaned_data:
                continue
            value = self.cleaned_data[name]
            if not field.required and value in field.empty_values:
                continue

            binding = getattr(field, "pydantic_model", None)
            model_field = getattr(field, "pydantic_field", name)
            if binding is None:
                continue

            if not (isinstance(binding, type) and issubclass(binding, BaseModel)):
                raise ImproperlyConfigured(
                    f"{type(self).__name__}.{name}: pydantic_model must be a BaseModel class."
                )
            if model_field not in binding.model_fields:
                raise ImproperlyConfigured(
                    f"{type(self).__name__}.{name}: Pydantic model {binding.__name__} "
                    f"has no field {model_field!r}."
                )

            annotation = binding.model_fields[model_field].rebuild_annotation()
            try:
                TypeAdapter(annotation).validate_python(value)
            except PydanticValidationError as exc:
                self.add_error(
                    name,
                    [
                        ValidationError(error["msg"], code=error["type"])
                        for error in exc.errors()
                    ],
                )
