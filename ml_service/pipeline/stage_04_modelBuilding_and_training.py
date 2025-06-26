from ml_service.config.configuration import ConfigurationManager
from ml_service.components.modelBuilding_and_evaluation import ModelBuildingAndEvaluation
from ml_service.logging import logger
from ml_service.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH

import dagshub
dagshub.init(repo_owner='phoenixarjun007', repo_name='SalesNexus', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)


class ModelBuildingAndEvaluationTrainingPipeline:
    """Pipeline for Training, Evaluating Model, and Creating Submission."""
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
        model_and_eval_config = config_manager.get_modelBuilding_and_evaluation_config()

        process = ModelBuildingAndEvaluation(model_and_eval_config)

        metrics = process.run_pipeline()
        logger.info(f"✅ Evaluation Done! Metrics saved to {model_and_eval_config.metrics_file}")

        process.create_submission(model_and_eval_config.input_test_file,
                                "submission_XgBoost_model1.csv")


if __name__ == "__main__":
    STAGE_NAME = "Model Building and Evaluation Stage"
    try:
        logger.info("*******************************")
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = ModelBuildingAndEvaluationTrainingPipeline()
        pipeline.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e