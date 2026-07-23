import contextvars

# Holds the correlation ID for the current async context
correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="-")

# Base keys to redact globally
BASE_SENSITIVE_KEYS = {"password", "token", "authorization", "secret", "api_key", "credit_card"}

def make_redactor(extra_keys: set[str] = None):
    """Creates a structlog processor that masks sensitive keys."""
    sensitive = BASE_SENSITIVE_KEYS | (extra_keys or set())
    
    def redact(logger, method_name, event_dict):
        for key in list(event_dict.keys()):
            if any(s in key.lower() for s in sensitive):
                event_dict[key] = "***REDACTED***"
        return event_dict
    
<<<<<<< HEAD
    return redact
=======
    return redact
>>>>>>> 6cb085790f1e84c507e530b2162f12ed35fe840b
