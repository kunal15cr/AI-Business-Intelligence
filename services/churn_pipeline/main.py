"""Main entry point for the churn pipeline service."""

from churn_pipeline.config_manager import get_settings, churn_prediction_settings


def main() -> None:
    """Load configuration and run the pipeline."""
    settings = get_settings()

    print("=== CHURN PIPELINE: APPLICATION STARTED ===")
    print(f"Environment: {settings.environment}")
    print(f"MLflow URI: {settings.mlflow_tracking_uri}")
    print(f"Database URL (masked): {churn_prediction_settings.database_url}")
    # To get the real value (e.g. pass to SQLAlchemy), use:
    # db_url = churn_prediction_settings.database_url.get_secret_value()

    # Example of using config values
    trainer_config = settings.model_trainer
    print(f"Hyperparameters: {trainer_config['hyperparameters']}")

    if settings.is_production():
        print("Production mode: running with strict configuration.")
    else:
        print("Debug mode: extra logging enabled.")

    print("===========================================")


if __name__ == "__main__":
    main()
