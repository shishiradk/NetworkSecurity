import os
import sys
from urllib.parse import urlparse
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models,
)
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

# DagsHub setup
# os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/krishnaik06/networksecurity.mlflow"
# os.environ["MLFLOW_TRACKING_USERNAME"] = "krishnaik06"
# os.environ["MLFLOW_TRACKING_PASSWORD"] = "7104284f1bb44ece21e0e2adb4e36a250ae3251f"


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, model_name: str, best_model, classification_metric):
        # mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
        # tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision = classification_metric.precision_score
            recall = classification_metric.recall_score
            
            
            # mlflow.log_param("model_name", model_name)
            mlflow.log_metric("f1_score", classification_metric.f1_score)
            mlflow.log_metric("precision", classification_metric.precision_score)
            mlflow.log_metric("recall", classification_metric.recall_score)

            # if tracking_url_type_store != "file":
            #     mlflow.sklearn.log_model(best_model, "model", registered_model_name=model_name)
            # else:
            mlflow.sklearn.log_model(best_model, "model")

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree": {'criterion': ['gini', 'entropy', 'log_loss']},
            "Random Forest": {'n_estimators': [8, 16, 32, 128, 256]},
            "Gradient Boosting": {
                'learning_rate': [0.1, 0.01, 0.05, 0.001],
                'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
                'n_estimators': [8, 16, 32, 64, 128, 256],
            },
            "Logistic Regression": {},
            "AdaBoost": {'learning_rate': [0.1, 0.01, 0.001], 'n_estimators': [8, 16, 32, 64, 128, 256]},
        }

        model_report = evaluate_models(
            X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, param=params
        )

        best_model_name = max(model_report, key=model_report.get)
        best_model = models[best_model_name]
        logging.info(f"Best model selected: {best_model_name}")

        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        train_metrics = get_classification_score(y_true=y_train, y_pred=y_train_pred)
        test_metrics = get_classification_score(y_true=y_test, y_pred=y_test_pred)
        

        self.track_mlflow(best_model_name, best_model, train_metrics)
        self.track_mlflow(best_model_name, best_model, test_metrics)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path), exist_ok=True)
        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)

        #  Save the correct object (previously you were saving the class itself)
        save_object(self.model_trainer_config.trained_model_file_path, obj=network_model)
        save_object("final_model/model.pkl", best_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=train_metrics,
            test_metric_artifact=test_metrics,
        )

        logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            return self.train_model(X_train, y_train, X_test, y_test)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
