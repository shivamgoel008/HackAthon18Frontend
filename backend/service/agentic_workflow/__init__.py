import functools

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import SimpleJsonOutputParser
from langgraph.graph import END
from langchain_community.agent_toolkits.load_tools import load_tools
from langgraph.prebuilt import ToolNode
from service.agentic_workflow.agents.base_agent import BaseAgent
from service.agentic_workflow.prompts import prompts
from service.agentic_workflow.utils import create_agent, agent_node, router
from utils import get_llm
from service.agentic_workflow.agents.tools import helpDocsSearch, logsAndEmailSearch, logsSearch, mailsSearch, \
    pdfSearch, pptSearch, excelCSVSearch


class TriageAssistant(BaseAgent):
    def __init__(self):
        webSearchTool = [load_tools(["serpapi"])[-1]]
        webSearchToolNode = ToolNode(webSearchTool)


        helpDocsSearchTool = [helpDocsSearch]
        helpDocsSearchToolNode = ToolNode(helpDocsSearchTool)

        logsAndEmailSearchTool = [logsAndEmailSearch]
        logsAndEmailSearchToolNode = ToolNode(logsAndEmailSearchTool)

        logsSearchTool = [logsSearch]
        logsSearchToolNode = ToolNode(logsSearchTool)

        mailsSearchTool = [mailsSearch]
        mailsSearchToolNode = ToolNode(mailsSearchTool)

        pdfSearchTool = [pdfSearch]
        pdfSearchToolNode = ToolNode(pdfSearchTool)

        pptSearchTool = [pptSearch]
        pptSearchToolNode = ToolNode(pptSearchTool)

        excelCSVSearchTool = [excelCSVSearch]
        excelCSVSearchToolNode = ToolNode(excelCSVSearchTool)

        supervisorAgent = create_agent(get_llm(), [],
                                       prompts['supervisorAgent'])

        supervisorAgentNode = functools.partial(agent_node, agent=supervisorAgent, name="supervisorAgent")

        webSearchAgent = create_agent(get_llm(), webSearchTool,
                                      prompts['webSearchAgent'])

        webSearchAgentNode = functools.partial(agent_node, agent=webSearchAgent, name="webSearchAgent")

        helpDocsSearchAgent = create_agent(get_llm(), helpDocsSearchTool,
                                           prompts['helpDocsSearchAgent'])

        helpDocsSearchAgentNode = functools.partial(agent_node, agent=helpDocsSearchAgent,
                                                    name="helpDocsSearchAgent")

        logsAndEmailSearchAgent = create_agent(get_llm(), [logsAndEmailSearch, logsSearch, mailsSearch],
                                               prompts['logsAndEmailSearchAgent'])

        logsAndEmailSearchAgentNode = functools.partial(agent_node, agent=logsAndEmailSearchAgent,
                                                        name="logsAndEmailSearchAgent")

        nodes = [
            {"name": "supervisorAgent", "value": supervisorAgentNode},
            {"name": "webSearchAgent", "value": webSearchAgentNode},
            {"name": "helpDocsSearchAgent", "value": helpDocsSearchAgentNode},
            {"name": "logsAndEmailSearchAgent", "value": logsAndEmailSearchAgentNode},
            {"name": "webSearchTool", "value": webSearchToolNode},
            {"name": "helpDocsSearchTool", "value": helpDocsSearchToolNode},
            {"name": "logsAndEmailSearchTool", "value": logsAndEmailSearchToolNode},
            # {"name": "logsSearchAgent", "value": logsASearchAgentNode},
            {"name": "logsSearchTool", "value": logsSearchToolNode},
            # {"name": "mailsSearchAgent", "value": mailsSearchAgentNode},
            {"name": "mailsSearchTool", "value": mailsSearchToolNode},
            # {"name": "pdfSearchAgent", "value": pdfSearchAgentNode},
            {"name": "pdfSearchTool", "value": pdfSearchToolNode},
            # {"name": "pptSearchAgent", "value": pptSearchAgentNode},
            {"name": "pptSearchTool", "value": pptSearchToolNode},
            # {"name": "excelCSVSearchAgent", "value": excelCSVSearchAgent},
            {"name": "excelCSVSearchTool", "value": excelCSVSearchToolNode}

        ]
        conditional_edges = [
            {
                "source": "supervisorAgent",
                "target": router,
                "conditions": {
                    "webSearchAgent": "webSearchAgent",
                    "helpDocsSearchAgent": "helpDocsSearchAgent",
                    "logsAndEmailSearchAgent": "logsAndEmailSearchAgent",
                    "supervisorAgent": END,
                    END: END
                }
            },
            {
                "source": "webSearchAgent",
                "target": router,
                "conditions": {
                    "call_tool": "webSearchTool",
                    "supervisorAgent": "supervisorAgent",
                    END: END
                }
            },
            {
                "source": "helpDocsSearchAgent",
                "target": router,
                "conditions": {
                    "call_tool": "helpDocsSearchTool",
                    "call_pdf_tool": "pdfSearchTool",
                    "call_ppt_tool": "pptSearchTool",
                    "call_excel_tool": "excelCSVSearchTool",
                    "supervisorAgent": "supervisorAgent",
                    END: END
                }
            },
            {
                "source": "logsAndEmailSearchAgent",
                "target": router,
                "conditions": {
                    "call_tool": "logsAndEmailSearchTool",
                    "call_logs_tool": "logsSearchTool",
                    "call_mails_tool": "mailsSearchTool",
                    "supervisorAgent": "supervisorAgent",
                    END: END
                }
            },
            {
                "source": "helpDocsSearchTool",
                "target": "helpDocsSearchAgent"
            },
            {
                "source": "pdfSearchTool",
                "target": "helpDocsSearchAgent"
            },
            {
                "source": "pptSearchTool",
                "target": "helpDocsSearchAgent"
            },
            {
                "source": "excelCSVSearchTool",
                "target": "helpDocsSearchAgent"
            },
            {
                "source": "webSearchTool",
                "target": "webSearchAgent"
            },
            {
                "source": "logsAndEmailSearchTool",
                "target": "logsAndEmailSearchAgent"
            },
            {
                "source": "logsSearchTool",
                "target": "logsAndEmailSearchAgent"
            },
            {
                "source": "mailsSearchTool",
                "target": "logsAndEmailSearchAgent"
            }
        ]

        super().__init__(nodes, conditional_edges, "supervisorAgent")

    def query(self, prompt: str):
        chat = {
            "messages": [HumanMessage(content=prompt)],
        }
        events = self.graph.invoke(
            {
                "messages": chat["messages"]
            },
            {"recursion_limit": 10}
        )
        final_response = events["messages"][-1].content
        try:
            parsed_answer = SimpleJsonOutputParser().parse(final_response)
            if parsed_answer.get('answer', None):
                return parsed_answer['answer']
        except:
            pass
        return final_response

if __name__=='__main__':
    triage_assistant = TriageAssistant()
    print(triage_assistant.query("which  services are using crowstrike can you check in logs, please check in logs only"))