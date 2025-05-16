from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AEON_", env_file=".env")

    # Las Cumbres Observatory
    lco_token: str = ""
    lco_api_root: str = "https://observe.lco.global/api/"

    # SOAR
    soar_token: str = ""
    soar_api_root: str = "https://observe.lco.global/api/"

    # European Southern Observatory
    eso_environment: str = "demo"
    eso_username: str = ""
    eso_password: str = ""


settings = Settings()
