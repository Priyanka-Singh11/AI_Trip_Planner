from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition



class GraphBuilder():
    def __init__(self):
        pass




    self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self,state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]#question asked by user
        input_question = [self.system_prompt] + user_question#input given to the agent
        response = self.llm_with_tools.invoke(input_question)#output by llm after choosing teh appropriate llm to reply
        return {"messages": [response]}


    def build_grapg(self):
#adding nodes and edges to the graph so that it can behave like a react agent whenever required
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)
        self.graph = graph_builder.compile()
        return self.graph
        



    def __call__(self):
#to call the above build_graph function
        return self.build_graph()

