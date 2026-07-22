from pydantic import BaseModel, ConfigDict


class CFHTBaseModel(BaseModel):
    """Base model for CFHT generated schemas.
    This allows us to configure all derived classes
    if necessary
    """

    model_config = ConfigDict(coerce_numbers_to_str=False)
