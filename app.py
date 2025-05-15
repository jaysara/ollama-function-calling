from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import os

#pip install fastapi uvicorn pandas
# To run the server
# uvicorn app:app --reload

# Load CSVs
DATA_DIR = "/mnt/data/mcp_sample"

apps_df = pd.read_csv(os.path.join(DATA_DIR, "application_catalog.csv"))
caps_df = pd.read_csv(os.path.join(DATA_DIR, "capability_catalog.csv"))
consumes_df = pd.read_csv(os.path.join(DATA_DIR, "application_consumes_capability_mapping.csv"))
provides_df = pd.read_csv(os.path.join(DATA_DIR, "application_provides_capability_mapping.csv"))

app = FastAPI(title="MCP Tool Server", description="Tool server to analyze application-capability relationships.")

class CapabilityID(BaseModel):
    capability_id: str

@app.get("/tools/get_applications", response_model=List[str])
def get_applications():
    return apps_df['application_name'].dropna().unique().tolist()

@app.get("/tools/get_capabilities", response_model=List[str])
def get_capabilities():
    return caps_df['name'].dropna().unique().tolist()

@app.post("/tools/find_apps_consuming_capability", response_model=List[str])
def find_apps_consuming_capability(data: CapabilityID):
    filtered = consumes_df[consumes_df['capability_id'] == data.capability_id]
    return filtered['application_name'].dropna().unique().tolist()

@app.post("/tools/find_apps_providing_capability", response_model=List[str])
def find_apps_providing_capability(data: CapabilityID):
    filtered = provides_df[provides_df['capability_id'] == data.capability_id]
    return filtered['application_name'].dropna().unique().tolist()

@app.get("/tools/find_orphan_capabilities", response_model=List[str])
def find_orphan_capabilities():
    provided = set(provides_df['capability_id'].dropna())
    consumed = set(consumes_df['capability_id'].dropna())
    used = provided.union(consumed)
    all_caps = set(caps_df['capability_id'].dropna())
    orphaned = all_caps - used
    return caps_df[caps_df['capability_id'].isin(orphaned)]['name'].tolist()

@app.get("/tools/health")
def health_check():
    return {"status": "ok"}

# To run: uvicorn this_file_name:app --reload
