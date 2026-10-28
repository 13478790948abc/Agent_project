from langchain.agents import create_agent
from model.factory import chat_model
from agent.tools.agent_tools import (fetch_external_data, rag_summarize, get_current_month,
                               get_user_id, get_user_location, fill_context_for_report, get_weather)
from utils.prompt_loader import load_system_prompts
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[fill_context_for_report, fetch_external_data, rag_summarize, get_weather,
                    get_current_month, get_user_id, get_user_location],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    def execute_stream(self, query):
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        # 第三个参数context就是上下文 runtime中的信息
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            lastest_message = chunk["messages"][-1]
            if lastest_message.content:
                yield lastest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在我所在的地区下如何保养"):
        print(chunk, end="", flush=True)