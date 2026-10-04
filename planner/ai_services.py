"""Single provider boundary for personalised AI; deterministic features remain usable offline."""
from django.conf import settings


def complete(prompt, fallback=""):
    if not settings.OPENAI_API_KEY:
        return fallback
    try:
        from openai import OpenAI
        response = OpenAI(api_key=settings.OPENAI_API_KEY).responses.create(model=settings.CHRONOVA_LLM_MODEL, input=prompt)
        return response.output_text.strip() or fallback
    except Exception:
        return fallback
