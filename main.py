import os
import argparse
from dotenv import load_dotenv

from llm import CLILLM

load_dotenv(override=True)
os.makedirs("logs", exist_ok=True)

zhipu_api_key = os.getenv("ZHIPU_API_KEY")
model = os.getenv("MODEL")


def main():
    parser = argparse.ArgumentParser(description="This is a LLM-based chatbot.")
    parser.add_argument(
        "--stream", "-s", action="store_true", help="stream mode output"
    )
    parser.add_argument(
        "--prompt", "-pe", action="store_true", help="prompt enhancing mode"
    )
    parser.add_argument("--log", "-l", action="store_true", help="enable logging")

    args = parser.parse_args()

    llm = CLILLM(
        api_key=zhipu_api_key,
        model=model,
        stream=args.stream,
        log=args.log,
        prompt=args.prompt,
    )

    llm.chat_loop()
    exit()

if __name__ == "__main__":
    main()