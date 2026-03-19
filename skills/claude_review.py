import anthropic

_client = anthropic.Anthropic()


def review_code_with_claude(diff: str, context: str = "") -> str:
    """Revisión semántica de un diff de PR usando Claude."""
    message = _client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Revisa el siguiente diff como un senior engineer.

Contexto del proyecto: {context}

Diff:
```diff
{diff}
```

Proporciona:
1. Resumen de cambios
2. Problemas potenciales (bugs, seguridad, rendimiento)
3. Sugerencias de mejora
4. Puntuación general (1-10)

Sé conciso y directo.""",
            }
        ],
    )
    return message.content[0].text
