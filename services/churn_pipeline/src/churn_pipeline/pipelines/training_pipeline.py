import mlflow

from churn_pipeline.config_manager.config import get_settings
from churn_pipeline.data.ingestion import DataIngestion
from churn_pipeline.data.validation import DataValidation
from churn_pipeline.features.transformations import DataTransformation
from churn_pipeline.logging.logging import configure_logging, get_logger
from churn_pipeline.models.evaluator import ModelEvaluator
from churn_pipeline.models.trainer import ModelTrainer

if __name__ == "__main__":
    settings = get_settings()
    configure_logging(service_name="churn_pipeline", level="INFO", enable_file_logging=True)
    logger = get_logger("churn_pipeline")

    # MLflow Setup
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment("Customer_Churn_Prediction")

    logger.info("=== STARTING CHURN TRAINING PIPELINE ===")

    with mlflow.start_run(run_name="churn_training_pipeline"):
        try:
            # Log Configuration
            mlflow.log_params(settings.model_trainer["hyperparameters"])

            ingestion = DataIngestion(settings.data_ingestion)
            train_path, test_path = ingestion.initiate_ingestion()

            validation = DataValidation(settings.data_validation)
            if not validation.validate(train_path, test_path):
                raise ValueError("Data validation failed.")

            transformation = DataTransformation()
            X_train, X_test, y_train, y_test = transformation.initiate_transformation(train_path, test_path)

            trainer = ModelTrainer(settings.model_trainer)
            model = trainer.train(X_train, y_train)

            evaluator = ModelEvaluator(settings.model_evaluation)
            f1_score = evaluator.evaluate(model, X_test, y_test)

            # Log Metrics & Model to MLflow
            mlflow.log_metric("f1_score", f1_score)

            if f1_score >= settings.model_evaluation["expected_f1_score"]:
                logger.info(f"Model ACCEPTED (F1: {f1_score}). Registering to MLflow.")
                # mlflow.xgboost.log_model(model, "model")  # Uncomment when using real model
            else:
                logger.warning(f"Model REJECTED (F1: {f1_score}). Did not meet threshold.")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
