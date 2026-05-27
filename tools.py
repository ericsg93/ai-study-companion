import json
from pathlib import Path

NOTAS_PATH = Path("notas.md")


def save_note(topic: str, content: str) -> str:
    """Append a note under a topic heading to notas.md."""
    with NOTAS_PATH.open("a", encoding="utf-8") as f:
        f.write(f"\n## {topic}\n\n{content}\n")
    return f"Nota guardada bajo '{topic}'."


def read_notes() -> str:
    """Return the full contents of notas.md, or a message if empty."""
    if not NOTAS_PATH.exists() or NOTAS_PATH.stat().st_size == 0:
        return "No hay notas guardadas todavía."
    return NOTAS_PATH.read_text(encoding="utf-8")


# Tool schemas for the Anthropic API
TOOLS = [
    {
        "name": "save_note",
        "description": "Guarda una nota sobre un tema de estudio en notas.md.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "Título o tema de la nota"},
                "content": {"type": "string", "description": "Contenido de la nota"},
            },
            "required": ["topic", "content"],
        },
    },
    {
        "name": "read_notes",
        "description": "Lee todas las notas guardadas en notas.md.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

TOOL_HANDLERS = {
    "save_note": lambda args: save_note(**args),
    "read_notes": lambda args: read_notes(),
}


def dispatch(tool_name: str, tool_input: dict) -> str:
    handler = TOOL_HANDLERS.get(tool_name)
    if not handler:
        return f"Herramienta desconocida: {tool_name}"
    return handler(tool_input)
