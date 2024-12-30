from langchain_core.messages import ToolMessage, AIMessage
from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END
from dotenv import load_dotenv
load_dotenv()

def create_agent(llm, tools, system_message: str, default_prompt_used=True):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant, collaborating with other assistants."
                " Use the provided Tools to progress towards answering the question."
                " You have access to the following Tools: {tool_names}.\n{system_message}",
            ) if default_prompt_used else
            (
                "system",
                "{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return (prompt | llm.bind_tools(tools)) if tools else prompt | llm


def agent_node(state, agent, name):
    result = agent.invoke(state)
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        "sender": name,
    }


def router(state):
    if state["messages"][-1].tool_calls:
        tool_call_mapping = {
            "mailSearch": "call_mails_tool",
            "logsSearch": "call_logs_tool",
            "pdfSearch": "call_pdf_tool",
            "pptSearch": "call_ppt_tool",
            "excelCSVSearch": "call_excel_tool"
        }
        return tool_call_mapping.get(state["messages"][-1].tool_calls[0]['name'], "call_tool")
    content = state["messages"][-1].content
    try:
        parsed_json = SimpleJsonOutputParser().parse(content)
        if 'answer' in parsed_json:
            return END
        return parsed_json.get("type", "supervisorAgent")
    except:
        pass
    return "supervisorAgent"