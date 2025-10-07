from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys,os

if __name__=="__main__":
    try:
        TrainingPipelineConfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion process")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()