"""Existing Gradio presentation, now backed by semantic retrieval."""
from functools import lru_cache
import os
from rag.settings import MAX_TOOL_ROUNDS, PROJECT_ROOT
# settings loads .env before these imports, including existing tool globals.
from openai import OpenAI, OpenAIError
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from rag.chat import prompt_messages, direct_profile_link, log_usage
from rag.embeddings import EmbeddingError
from rag.vectors import IndexError as SemanticIndexError
import gradio as gr

# Keep the deployed chat model configurable without requiring a source-code edit.
MODEL_NAME = os.getenv('BEDROCK_CHAT_MODEL_ID', 'openai.gpt-oss-20b')

@lru_cache(maxsize=1)
# Build the OpenAI-compatible client once and reuse its connection pool.
def chat_client():
    key = os.getenv('OPENAI_API_KEY')
    base = os.getenv('OPENAI_BASE_URL')
    if not key or not base:
        raise ValueError('Configure OPENAI_API_KEY and OPENAI_BASE_URL for your existing chat endpoint.')
    return OpenAI(api_key=key, base_url=base, timeout=60, max_retries=2)


# Orchestrate one user turn: retrieve evidence, call the model, execute any
# approved tools, and translate provider failures into safe visitor messages.
def chat(message, history):
    if not isinstance(message, str) or not message.strip():
        return 'Please enter a question about my professional experience.'
    try:
        quick_answer = direct_profile_link(message)
        if quick_answer:
            return quick_answer
        # Retrieval constructs a bounded, source-grounded prompt before the
        # generative model is called.
        messages, _matches = prompt_messages(TWIN_SYSTEM_PROMPT, history, message)
        client = chat_client()
        # Bound the loop so a model cannot request tools indefinitely.
        for round_number in range(MAX_TOOL_ROUNDS + 1):
            request = {'model': MODEL_NAME, 'messages': messages}
            if tools:
                request['tools'] = tools
            response = client.chat.completions.create(**request)
            log_usage(response)
            if not response.choices:
                return 'The answer service returned no response. Please try again.'
            answer = response.choices[0].message
            if not answer.tool_calls:
                return answer.content or 'I do not have enough verified information to answer that.'
            if round_number == MAX_TOOL_ROUNDS:
                return 'I could not complete the follow-up action. Please try again or contact me through LinkedIn.'
            # Preserve existing contact/unanswered-question/Pushover behavior.
            results = handle_tool_calls(answer.tool_calls)
            messages.append(answer.model_dump(exclude_none=True))
            messages.extend(results)
    except SemanticIndexError:
        print('[chat] Semantic index unavailable; rebuild and redeploy the index.')
        return 'My knowledge index is temporarily unavailable. Please try again later.'
    except EmbeddingError as error:
        print(str(error))  # Sanitized provider error code only.
        return 'My knowledge search is temporarily unavailable. Please try again shortly.'
    except OpenAIError as error:
        print(f'[chat] Chat provider failure: {type(error).__name__}')
        return 'The answer service is temporarily unavailable. Please try again shortly.'
    except ValueError as error:
        # Configuration validation messages contain no credential values.
        return str(error) if str(error).startswith(('Please ', 'Configure ')) else 'I could not process that request.'
    except Exception as error:
        print(f'[chat] Request failed: {type(error).__name__}')
        return 'I could not complete that request. Please try again.'


if __name__ == '__main__':
    # Keep the existing UI structure, CSS, JS, examples, title, and theme.
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title='Digital Twin',
        description='Talk to my AI twin about my career',
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())
