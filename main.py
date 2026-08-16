from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

app = FastAPI()#object for fast api endpoint

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):#validating the query that will come by user
    question: str

@app.post("/query")#fast api end point 
async def query_travel_agent(query:QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")#object
        react_app=graph()#calling function in agent_workflow notebook __call__
        #react_app = graph.build_graph()

        png_graph = react_app.get_graph().draw_mermaid_png()#this is teh graph that is going to be saved
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages={"messages": [query.question]}# I'll be getting my query from my state
       
#I am invoking my query and checking it with the output 
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
 # till here  
 # then I will return that particular final output     
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

