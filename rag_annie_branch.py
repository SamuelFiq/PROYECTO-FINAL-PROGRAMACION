# -*- coding: utf-8 -*-
"""RAG_ANNIE_BRANCH

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ufOHc_1iyvbgune5NRA27JbOiYmdjRV8
"""

pip install pinecone-client

!pip install -qU \
  transformers==4.31.0 \
  sentence-transformers==2.2.2 \
  datasets==2.14.0 \
  accelerate==0.21.0 \
  einops==0.6.1 \
  langchain==0.0.240 \
  xformers==0.0.20 \
  bitsandbytes==0.41.0

from torch import cuda
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

embed_model = HuggingFaceEmbeddings(
    model_name=embed_model_id,
    model_kwargs={'device': device},
    encode_kwargs={'device': device, 'batch_size': 32}
)

docs = [
    "this is one document",
    "and another document"
]

embeddings = embed_model.embed_documents(docs)

print(f"We have {len(embeddings)} doc embeddings, each with "
      f"a dimensionality of {len(embeddings[0])}.")

import os
from pinecone import Pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = os.environ.get('PINECONE_API_KEY') or 'be227b3a-d248-411d-8808-00b17f911811'

# configure client
pc = Pinecone(api_key=api_key)

from pinecone import ServerlessSpec

cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'

spec = ServerlessSpec(cloud=cloud, region=region)

index_name = 'llama-2-rag'

# check if index already exists (it shouldn't if this is first time)
if index_name not in pc.list_indexes().names():
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=len(embeddings[0]),  # dimensionality of text-embedding-ada-002
        metric='cosine',
        spec=spec
    )
# connect to index
index = pc.Index(index_name)
# view index stats
index.describe_index_stats()