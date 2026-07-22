ERROR_CATALOG = {

    "CONFIG_001": {
        "description": "Configuration missing",
        "retryable": False,
    },

    "DB_001": {
        "description": "Database unavailable",
        "retryable": True,
    },

    "FILE_001": {
        "description": "Dataset missing",
        "retryable": False,
    },

    "GENAI_001": {
        "description": "Embedding failed",
        "retryable": True,
    },

    "MCP_001": {
        "description": "Tool execution failed",
        "retryable": True,
    },
}