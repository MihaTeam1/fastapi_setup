import os
from .base import Settings

module = os.environ.get("SETTINGS_MODULE")

if module == 'production':
    from .production import Settings as AdditionalSettings
elif module == 'development':
    from .development import Settings as AdditionalSettings
elif module == 'test':
    from .test import Settings as AdditionalSettings

settings = Settings(module=AdditionalSettings, _env_file=AdditionalSettings.Config.env_file)


