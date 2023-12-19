import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from numpy import dot
from numpy.linalg import norm
from pandas import DataFrame

from app.utils.logging_util import logger
from app.utils.openai_util import OpenAIUtil


def get_cosine_similarity(a, b):
    """Calculates the cosine similarity for embedding search"""
    return dot(a, b) / (norm(a) * norm(b))


class EmbeddingUtil(object):
    """Singleton util class to create embeddings and search for keywords in the icd10 catalog"""

    _instance = None
    icd10_symptoms: DataFrame
    embedding_column: str = "openai_embedding"
    openai_util: OpenAIUtil = None
    # path to the icd-10 PKL files. Can be set or left blank
    data_folder_path: str
    data_file_name: str

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EmbeddingUtil, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        data_folder_path: str = "app/data/catalogs/",
        data_file_name: str = "icd10gm_symptoms.pkl",
    ):
        if hasattr(self, "_initialized"):
            return
        # load env variables
        load_dotenv()
        if os.getenv("OPENAI_API_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_API_KEY")

        # check if folder/file paths exist
        self.data_folder_path = data_folder_path
        self.data_file_name = data_file_name
        if not os.path.exists(os.path.join(self.data_folder_path)):
            raise EnvironmentError(f"PKL path does not exist: {self.data_folder_path}")
        icd10_file_path = os.path.join(self.data_folder_path, self.data_file_name)
        if not os.path.exists(icd10_file_path):
            raise EnvironmentError(
                f"ICD-10 PKL File does not exist at path: {icd10_file_path}"
            )

        self.openai_util = OpenAIUtil()
        self.icd10_symptoms = pd.read_pickle(
            os.path.join(self.data_folder_path, self.data_file_name)
        )
        # check if the embeddings exist already
        if self.embedding_column not in self.icd10_symptoms.columns:
            logger.warning("icd10 file has no embeddings, the search wont work")

        logger.info("Created EmbeddingUtil")

    def create_icd10_symptoms_embeddings(self):
        """Creates the embeddings for the symptoms (category R) and saves them into the original PKL"""
        self.icd10_symptoms[self.embedding_column] = self.icd10_symptoms[
            "klassentitel"
        ].apply(lambda x: self.openai_util.get_embedding(x))
        self.icd10_symptoms.to_pickle(
            os.path.join(self.data_folder_path, self.data_file_name),
        )

    def search(self, df: DataFrame, text: str, n=10):
        """Generic function to search a dataframe that has an embeddings column"""
        if self.embedding_column not in df.columns:
            raise Exception(
                f"Dataframe has no embeddings (column {self.embedding_column}), please create embeddings first"
            )
        embedding = self.openai_util.get_embedding(text)
        df["similarities"] = df[self.embedding_column].apply(
            lambda x: get_cosine_similarity(np.array(x), embedding)
        )

        return df.nlargest(n, "similarities")