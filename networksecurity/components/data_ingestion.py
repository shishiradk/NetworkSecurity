from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


## configuration of the data ingestion config

from networksecurity.entity.config_entity import DataIngestionConfig

import os,sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from dotenv import load_doenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_Ingestion_config:DataIngestionConfig):
        try:

            self.data_ingestion_config=data_Ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    def export_collection_ad_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            
        
        
    def initiate_data_ingestion(self):
        try:
            dataframe=pd.read_csv(MONGO
            raise NetworkSecurityException
            