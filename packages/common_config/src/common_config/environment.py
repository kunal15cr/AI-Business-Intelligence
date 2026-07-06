from enum import StrEnum
class Environment(StrEnum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"
    @property
    def is_production(self) -> bool:
        return self is Environment.PRODUCTION
