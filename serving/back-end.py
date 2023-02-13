from http import HTTPStatus
from statistics import mode
from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
import uvicorn

# OCR
from PIL import Image
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from cli import LatexOCR

# DPR
from DPR import *
from tokenizers import Tokenizer
import torch
from transformers import DPRConfig, DPRQuestionEncoder
from pydantic import BaseModel
from elasticsearch import Elasticsearch

es = Elasticsearch(
    cloud_id="MathMatch:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDJmYzA4YmQ1ZTg5YjQ5NGFhODg4YjVmZjE2YWQxODE5JGVlN2U4ZjI4ODQ0ZTRlYzBhYTE2ZjdhNTAwZWQ4YjRk",
    basic_auth=("elastic", "rvUUGH364TvAj6tyS9Y3fitD")
    )

app = FastAPI()
OCR_model = None
# DPR_model = None

# Load OCR model
# @app.on_event('startup')
# async def load_OCR():
#     global OCR_model
#     if OCR_model is None:
#         OCR_model = LatexOCR()

    

# Load DPR model
def load_DPR(model_path):
    config = DPRConfig.from_pretrained(model_path)
    encoder = DPRQuestionEncoder.from_pretrained(
    model_path, config=config,
    ignore_mismatched_sizes=True
    )
    return encoder

# Check status
def root():
    response = {
        'message': HTTPStatus.OK.phrase,
        'status-code': HTTPStatus.OK,
        'data': {}
    }
    return response

def elasticsearch(embedding):
    global es

    body ={
    'size':30, 
    "query": {
        "script_score": {
        "query" : {
            "match_all": {}
            },
        
        "script": 
        {
            "source": "cosineSimilarity(params.query_vector, 'embedding')", 
            "params": 
            {
            "query_vector": embedding
            }
        }
        }
        }
        \
    }
    latex = es.search(index='latex_embedding', body=body)
    res = {}
    latex_info = latex['hits']['hits']
    for i in range(len(latex_info)):
        id = latex_info[i]['_id']
        info = latex_info[i]['_source']
        doc_id = info['doc_id']
        body = {
            'query': {
                    'match': {
                            'doc_id': doc_id
                        }
                }
        }
        doc = es.search(index='doc_info', body=body)
        doc_info = doc['hits']['hits'][0]['_source']
        body = {'id': id, 'link': doc_info['link'], 'title': doc_info['title'], 'latex':info['latex'], 'summary':doc_info['summary'], 'embedding':info['embedding'], 'timestamp':info['timestamp']}
        res[i] = body
    return res
## get result
@app.get("/OCR/")
async def img_to_latex(file: UploadFile = File(...)) -> str:
    global OCR_model
    if OCR_model is None:
        OCR_model = LatexOCR()
    image = Image.open(file.file)
    return OCR_model(image)

class latex_check(BaseModel):
    latex: str

@app.get("/Search/")
async def embedding(data: latex_check):     # latex str 받아오기
    device = torch.device("cuda" if torch.cuda.is_available()
                        else "mps" if torch.backends.mps.is_available() else "cpu")
    model_path = 'C:\GOME\pix2tex\pix2tex\DPR\ep0_acc0.847'
    tokenizer_path = 'C:\GOME\pix2tex\pix2tex\DPR\dpr_tokenizer-bpe.json'
    tokenizer = Tokenizer.from_file(tokenizer_path)
    latex_code = data.latex
    input_token = tokenizer.encode(latex_code)
    input = {}
    input['input_ids'] = torch.tensor(input_token.ids).unsqueeze(dim=0).to(device)
    input['token_type_ids'] = torch.tensor(input_token.type_ids).unsqueeze(dim=0).to(device)
    input['attention_mask'] = torch.tensor(input_token.attention_mask).unsqueeze(dim=0).to(device)

    encoder = load_DPR(model_path)
    encoder = encoder.to(device)
    with torch.no_grad():
        output = encoder(**input).pooler_output.tolist()    # (1, 384)
    
    # elasticsearch
    res = elasticsearch(output[0])
    return res


# if __name__ == "__main__":
    #     uvicorn.run("back-end:app", host="0.0.0.0", port=5000, reload=True)