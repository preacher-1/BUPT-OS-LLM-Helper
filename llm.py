from zhipuai import ZhipuAI, ZhipuAIError
import datetime
import logging

from rich import print as rprint
from rich.markdown import Markdown, MarkdownIt
from rich.console import Console
from rich.live import Live

from prompt import system_prompt, get_user_prompt


class CLILLM:
    def __init__(self, api_key, model, stream, prompt, log):
        self.model = model
        self.stream = stream
        self.prompt = prompt
        self.log = log
        if log:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)

        self.client = ZhipuAI(api_key=api_key)
        self.message_history = [{"role": "system", "content": system_prompt}]
        self.console = Console()

    def make_message(self, question: str, role: str = "user", enhance=False):
        message = {
            "role": role,
            "content": question if not enhance else get_user_prompt(question),
        }  # get_user_prompt(question),
        return message

    def chat_stream(self, question: str, promptenhance=False):
        # 日志记录
        if self.log:
            self.logger.info(
                datetime.datetime.now().strftime("%m-%d %H:%M:%S")
                + " (User)"
                + question
            )

        try:
            self.message_history.append(
                self.make_message(question, "user", promptenhance)
            )
            # 流式响应
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.message_history,
                tools=[{"type": "web_search", "web_search": {"search_result": True}}],
                stream=True,
            )
            # 打印系统响应
            assistant_response = ""
            with Live(
                vertical_overflow="ellipsis", console=self.console
            ) as lv:
                for chunk in stream:
                    if self.log:
                        self.logger.info(
                            datetime.datetime.now().strftime("%m-%d %H:%M:%S")
                            + " "
                            + str(chunk.choices[0].delta)
                        )
                    if (content := chunk.choices[0].delta.content) is not None:
                        assistant_response += content
                        lv.update(Markdown(assistant_response))
                        # md.markup += content
                        # md.parsed = parser.parse(md.markup)
                        # console.print(content, end="")
            self.message_history.append(
                self.make_message(assistant_response, "assistant")
            )
        except KeyboardInterrupt:
            self.console.print("Canceled", style="bold red")
            if self.message_history[-1]["role"] == "user":
                self.message_history.pop()
        except ZhipuAIError as e:
            self.console.print("ZhipuAIError:", e, style="bold red")
            assistant_response = ""

    def chat_non_stream(self, question: str, promptenhance=False):
        try:
            if self.log:
                # 日志记录
                self.logger.info(
                    datetime.datetime.now().strftime("%m-%d %H:%M:%S")
                    + " (User)"
                    + question
                )

            self.console.print("(System)", style="bold green")
            self.message_history.append(
                self.make_message(question, "user", promptenhance)
            )  # 加入对话历史

            # 非流式响应
            with self.console.status("[bold green]等待API返回中...") as status:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.message_history,
                    tools=[
                        {"type": "web_search", "web_search": {"search_result": True}}
                    ],
                )

            # 打印系统响应
            content = response.choices[0].message.content
            if self.log:
                self.logger.info(
                    datetime.datetime.now().strftime("%m-%d %H:%M:%S")
                    + " "
                    + str(response.choices[0].message)
                )
            self.console.print(Markdown(content))
            self.message_history.append(self.make_message(content, "assistant"))
        except KeyboardInterrupt:
            self.console.print("Canceled", style="bold red")
            if self.message_history[-1]["role"] == "user":
                self.message_history.pop()
            assistant_response = ""
        except ZhipuAIError as e:
            self.console.print("ZhipuAIError:", e, style="bold red")
            if self.message_history[-1]["role"] == "user":
                self.message_history.pop()
            assistant_response = ""

    @staticmethod
    def make_message(question: str, role: str = "user", enhance=False):
        message = {
            "role": role,
            "content": question if not enhance else get_user_prompt(question),
        }  # get_user_prompt(question),
        return message

    def chat_loop(self):
        self.console.print(
            f"系统配置：\nmodel = {self.model}\nstream = {self.stream}\nprompt = {self.prompt}\nlog = {self.log}\n欢迎使用本智能助手，输入内容即可进行对话，/clear 清空对话历史，/exit 终止程序",
            style="bold green",
        )

        question_start = None
        if self.prompt:
            question_start = True
        while True:
            self.console.print("\n(User)", end=" ", style="bold blue")
            try:
                question = input().strip()
                if question.strip() == "/exit":
                    if self.log:
                        self.logger.info(
                            datetime.datetime.now().strftime("%m-%d %H:%M:%S")
                            + " 程序退出"
                        )
                    break
                elif question.strip() == "/clear":
                    self.message_history = [
                        {"role": "system", "content": system_prompt}
                    ]
                    self.console.print("对话历史已清空", style="bold yellow")
                    if self.log:
                        self.logger.info(
                            datetime.datetime.now().strftime("%m-%d %H:%M:%S")
                            + " 清空对话历史"
                        )
                else:
                    # 是否流式输出
                    if self.stream:
                        self.chat_stream(question, question_start)
                    else:
                        self.chat_non_stream(question, question_start)
                    question_start = False
            except KeyboardInterrupt:
                self.console.print("Canceled", style="bold red")
                if self.log:
                    self.logger.warning(
                        datetime.datetime.now().strftime("%m-%d %H:%M:%S") + " 程序退出"
                    )
                break
            except EOFError:
                self.console.print("Canceled", style="bold red")
                if self.log:
                    self.logger.warning(
                        datetime.datetime.now().strftime("%m-%d %H:%M:%S") + " 程序退出"
                    )
                break


# def chat_stream_test(question: str):
#     message_history.append(make_message(question, "user"))
#     # 流式响应
#     stream = client.chat.completions.create(
#         model=model,
#         messages=message_history,
#         tools=[{"type": "web_search", "web_search": {"search_result": True}}],
#         stream=True,
#     )
#     # 打印系统响应
#     assistant_response = ""
#     print("系统：", end="", flush=True)
#     for chunk in stream:
#         if chunk.choices[0].delta.content is not None:
#             temp_response = chunk.choices[0].delta.content
#             assistant_response += temp_response
#             print(temp_response, end="")
#             # rprint(Markdown(temp_response),end="")
#     message_history.append(make_message(assistant_response, "assistant"))


# def chat_stream(question: str):
#     # 日志记录
#     logger.info(
#         datetime.datetime.now().strftime("%m-%d %H:%M:%S") + " (User)" + question
#     )
#     try:
#         message_history.append(make_message(question, "user"))
#         # 流式响应
#         stream = client.chat.completions.create(
#             model=model,
#             messages=message_history,
#             tools=[{"type": "web_search", "web_search": {"search_result": True}}],
#             stream=True,
#         )
#         # 打印系统响应
#         assistant_response, md = "", Markdown("")
#         parser = MarkdownIt().enable("strikethrough")
#         with Live(md, refresh_per_second=10, console=console) as lv:
#             for chunk in stream:
#                 # print(chunk.choices[0])
#                 logger.info(
#                     datetime.datetime.now().strftime("%m-%d %H:%M:%S")
#                     + " "
#                     + str(chunk.choices[0].delta)
#                 )
#                 if (content := chunk.choices[0].delta.content) is not None:
#                     assistant_response += content
#                     md.markup += content
#                     md.parsed = parser.parse(md.markup)
#                     # console.print(content, end="")
#                 time.sleep(0.05)
#         message_history.append(make_message(assistant_response, "assistant"))
#     except KeyboardInterrupt:
#         console.print("Canceled", style="bold red")
#         if message_history[-1]["role"] == "user":
#             message_history.pop()
#     except ZhipuAIError as e:
#         console.print("ZhipuAIError:", e, style="bold red")
#         assistant_response = ""


# def chat_non_stream_test(question: str):
#     message_history.append(make_message(question, "user"))
#     # 非流式响应
#     response = client.chat.completions.create(
#         model=model,
#         messages=message_history,
#         tools=[{"type": "web_search", "web_search": {"search_result": True}}],
#     )
#     assistant_response = response.choices[0].message.content
#     message_history.append(make_message(assistant_response, "assistant"))
#     # print("系统：", assistant_response)
#     rprint(Markdown("系统：" + assistant_response))


# def chat_non_stream(question: str):
#     try:
#         # 日志记录
#         logger.info(
#             datetime.datetime.now().strftime("%m-%d %H:%M:%S") + " (User)" + question
#         )

#         console.print("(System)", style="bold green")
#         message_history.append(make_message(question, "user"))  # 加入对话历史

#         # 非流式响应
#         with console.status("[bold green]等待API返回中...") as status:
#             response = client.chat.completions.create(
#                 model=model,
#                 messages=message_history,
#                 tools=[{"type": "web_search", "web_search": {"search_result": True}}],
#             )

#         # 打印系统响应
#         content = response.choices[0].message.content
#         logger.info(
#             datetime.datetime.now().strftime("%m-%d %H:%M:%S")
#             + " "
#             + str(response.choices[0].message)
#         )
#         console.print(Markdown(content))
#         message_history.append(make_message(content, "assistant"))
#     except KeyboardInterrupt:
#         console.print("Canceled", style="bold red")
#         if message_history[-1]["role"] == "user":
#             message_history.pop()
#     except ZhipuAIError as e:
#         console.print("ZhipuAIError:", e, style="bold red")
#         assistant_response = ""


# if __name__ == "__main__":
#     logger = logging.getLogger(__name__)
#     logging.basicConfig(
#         filename=f"logs/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log",
#         encoding="utf-8",
#         level=logging.INFO,
#     )
#     logger.info(f"Model: {model}")

#     console.print(
#         "欢迎使用本智能助手，输入内容即可进行对话，clear 清空对话历史，exit 终止程序",
#         style="bold green",
#     )
#     while True:
#         console.print("\n(User)", end=" ", style="bold blue")
#         try:
#             question = input().strip()
#             if question.strip() == "exit":
#                 logger.info(
#                     datetime.datetime.now().strftime("%m-%d %H:%M:%S") + " 程序退出"
#                 )
#                 break
#             elif question.strip() == "clear":
#                 message_history = [{"role": "system", "content": system_prompt}]
#                 console.print("对话历史已清空", style="bold yellow")
#                 logger.info(
#                     datetime.datetime.now().strftime("%m-%d %H:%M:%S") + " 清空对话历史"
#                 )
#             else:
#                 chat_non_stream(question)
#         except KeyboardInterrupt:
#             console.print("Canceled", style="bold red")
#             logger.warning(
#                 datetime.datetime.now().strftime("%m-%d %H:%M:%S") + " 程序退出"
#             )
#             break
#         except EOFError:
#             console.print("Canceled", style="bold red")
#             logger.warning(
#                 datetime.datetime.now().strftime("%m-%d %H:%M:%S") + " 程序退出"
#             )
#             break
