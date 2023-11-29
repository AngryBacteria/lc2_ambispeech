import os

import openai
import pandas as pd
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding

load_dotenv()
openai.app_info = os.getenv("OPENAI_API_KEY")

datafile_path = "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\natural_language_processing\\kataloge\\LOINC_German_shortened.csv"

df = pd.read_csv(datafile_path)
df = df.head(10)
df["combined"] = (
    "LOINC_NUM: " + str(df.LOINC_NUM).strip() +
    "; COMPONENT: " + str(df.COMPONENT).strip() +
    "; LONG_COMMON_NAME: " + str(df.LONG_COMMON_NAME).strip() +
    "; RELATEDNAMES2: " + str(df.RELATEDNAMES2).strip()
)

df["embedding"] = df.combined.apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))

df.to_csv("test_embedding.csv")