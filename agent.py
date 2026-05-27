import os
from dotenv import load_dotenv
import anthropic
from tools import TOOLS, dispatch

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM = (
    "Eres un asistente de estudio especializado en IA. "
    "Ayudas al usuario a entender conceptos como RAG, Knowledge Graphs, "
    "LangGraph y agentes. Puedes guardar notas y leerlas cuando lo necesites."
)


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )

        # Accumulate assistant turn
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Extract final text response
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = dispatch(block.name, block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )
            messages.append({"role": "user", "content": tool_results})


def main():
    print("AI Study Companion — escribe 'salir' para terminar.\n")
    while True:
        user_input = input("Tú: ").strip()
        if user_input.lower() in {"salir", "exit", "quit"}:
            break
        if not user_input:
            continue
        reply = run_agent(user_input)
        print(f"\nAgente: {reply}\n")


if __name__ == "__main__":
    main()
