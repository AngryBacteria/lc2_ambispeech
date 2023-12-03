import ast
import os

import openai
from dotenv import load_dotenv
from openai.embeddings_utils import cosine_similarity
from pandas import DataFrame
import numpy as np
import pandas as pd

from app.utils.logging_util import logger


def convert_to_array(embedding_str):
    try:
        # Convert the string representation of the embedding back to a numpy array
        return np.array(ast.literal_eval(embedding_str))
    except:
        print("Malformed DATA!!")
        return np.zeros(768)


class EmbeddingUtil(object):
    """Singleton util class to create embeddings and search for keywords in the icd10 catalog"""

    _instance = None
    icd10: DataFrame
    embedding_model: str = "text-embedding-ada-002"
    embedding_column: str = "ada_embedding"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EmbeddingUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        if os.getenv("OPENAI_KEY") is None:
            raise EnvironmentError(".env file is missing the OPENAI_KEY")
        else:
            openai.api_key = os.getenv("OPENAI_KEY")
            self.icd10 = pd.read_csv("../data/catalogs/icd10gm_symptoms.csv", sep=",")
            # if the embeddings exist already, convert them back into an ndArray
            if self.embedding_column in self.icd10.columns:
                self.icd10[self.embedding_column] = self.icd10[self.embedding_column].apply(
                    convert_to_array
                )
            else:
                logger.warning("icd10 file has no embeddings, the search wont work")

            logger.info("Created EmbeddingUtil")

    def get_embedding(self, text):
        return (
            openai.Embedding.create(input=[text], model=self.embedding_model)
            .data[0]
            .embedding
        )

    def create_icd10_embeddings(self):
        self.icd10[self.embedding_column] = self.icd10["V9"].apply(
            lambda x: self.get_embedding(x)
        )
        self.icd10.to_csv("../data/catalogs/icd10gm_embeddings.csv")

    def search_functions(self, df, text, n=10):
        if self.embedding_column not in df.columns:
            raise Exception(
                f"Dataframe has no embeddings (column {self.embedding_column}), please create them first"
            )
        embedding = self.get_embedding(text)
        df["similarities"] = df[self.embedding_column].apply(
            lambda x: cosine_similarity(np.array(x), embedding)
        )

        res = df.sort_values("similarities", ascending=False).head(n)
        return res
