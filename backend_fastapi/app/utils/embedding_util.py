import ast
import os

from dotenv import load_dotenv
from numpy import dot
from numpy.linalg import norm
from pandas import DataFrame
import numpy as np
import pandas as pd

from app.utils.logging_util import logger
from app.utils.openai_util import OpenAIUtil


def convert_to_array(embedding_str):
    """Used to convert a string from the csv back into a np array"""
    try:
        return np.array(ast.literal_eval(embedding_str))
    except:
        print("Malformed DATA!!")
        return np.zeros(768)


def get_cosine_similarity(a, b):
    """Calculates the cosine similarity for embedding search"""
    return dot(a, b) / (norm(a) * norm(b))


class EmbeddingUtil(object):
    """Singleton util class to create embeddings and search for keywords in the icd10 catalog"""

    _instance = None
    icd10_symptoms: DataFrame
    embedding_column: str = "ada_embedding"
    openai_util: OpenAIUtil = None
    # path to the icd-10 csv files. Can be set or left blank
    csv_folder_path: str

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EmbeddingUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, csv_folder_path: str = "app/data/catalogs/"):
        if hasattr(self, "_initialized"):
            return
        # load env variables
        load_dotenv()
        if os.getenv("OPENAI_API_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_API_KEY")

        # check if folder/file paths exist
        self.csv_folder_path = csv_folder_path
        if not os.path.exists(os.path.join(self.csv_folder_path)):
            raise EnvironmentError(f"CSV path does not exist: {self.csv_folder_path}")
        icd10_file_path = os.path.join(self.csv_folder_path, "icd10gm_symptoms.csv")
        if not os.path.exists(icd10_file_path):
            raise EnvironmentError(
                f"ICD-10 CSV File does not exist at path: {icd10_file_path}"
            )

        self.openai_util = OpenAIUtil()
        self.icd10_symptoms = pd.read_csv(
            os.path.join(self.csv_folder_path, "icd10gm_symptoms.csv"), sep=","
        )
        # if the embeddings exist already, convert them back into an ndArray
        if self.embedding_column in self.icd10_symptoms.columns:
            self.icd10_symptoms[self.embedding_column] = self.icd10_symptoms[
                self.embedding_column
            ].apply(convert_to_array)
        else:
            logger.warning("icd10 file has no embeddings, the search wont work")

        logger.info("Created EmbeddingUtil")

    def create_icd10_symptoms_embeddings(self):
        """Creates the embeddings for the symptoms (category R) and saves them into the original csv"""
        self.icd10_symptoms[self.embedding_column] = self.icd10_symptoms["V9"].apply(
            lambda x: self.openai_util.get_embedding(x)
        )
        self.icd10_symptoms.to_csv(
            os.path.join(self.csv_folder_path, "icd10gm_symptoms.csv")
        )

    def search(self, df: DataFrame, text: str, n=10):
        """Generic function to search a dataframe that has an embeddings column"""
        if self.embedding_column not in df.columns:
            raise Exception(
                f"Dataframe has no embeddings (column {self.embedding_column}), please create them first"
            )
        embedding = self.openai_util.get_embedding(text)
        df["similarities"] = df[self.embedding_column].apply(
            lambda x: get_cosine_similarity(np.array(x), embedding)
        )

        res = df.sort_values("similarities", ascending=False).head(n)
        return res
