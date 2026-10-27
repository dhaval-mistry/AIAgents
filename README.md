# AI Agents Learning and Project Portfolio

This repository is a hands-on workspace for learning how large language models become useful applications: prompt design, conversation state, structured evaluation, tool calling, agent loops, external integrations, and user-facing interfaces.

It also serves as a structured record of my professional context and technical growth. The notebooks capture focused experiments, while `projects/` contains complete applications that bring those ideas together.

## Professional context

I am Dhaval Mistry, a senior engineering leader with more than 20 years of experience across software engineering, enterprise architecture, banking and payments, cloud modernization, production reliability, and globally distributed team leadership.

My current learning and project work focuses on:

- Applied AI and production-oriented AI applications
- Agentic workflows, tool calling, and Model Context Protocol (MCP)
- Secure integration of LLMs with enterprise applications
- Microsoft Azure, cloud-native architecture, microservices, APIs, and Kubernetes
- Observability, operational intelligence, and engineering reliability
- Practical engineering leadership that connects technology decisions to business outcomes

The goal is not only to explore frameworks, but to understand the underlying patterns, trade-offs, failure modes, and steps required to move an AI experiment toward a reliable application.

## Repository map

```text
AIAgents/
|-- 1_foundations/                 # Learning notebooks and source material
|   |-- exercise1.ipynb
|   |-- lab1.ipynb
|   |-- lab2.ipynb
|   |-- lab4.ipynb
|   `-- resources/
|-- projects/
|   `-- 01_TheDigitalTwin/         # First complete AI application
|       `-- README.md
|-- pyproject.toml                 # Repository-wide Python environment
|-- uv.lock                        # Reproducible dependency lock file
`-- README.md
```

## Live projects

| Project | Status | What it demonstrates | Documentation |
| --- | --- | --- | --- |
| The Digital Twin | Working local prototype | PDF-grounded professional assistant, prompt guardrails, multi-turn chat, function calling, Pushover notifications, and a customized Gradio interface | [Open project README](projects/01_TheDigitalTwin/README.md) |

Future applications will be added under `projects/` using numbered folders and a dedicated `README.md` in each project.

## Foundation notebooks

The notebooks form a practical learning sequence. They are experiments rather than production applications, and some cells intentionally show the mechanics that an agent framework would normally abstract.

| Notebook | Topics covered | Tools and integrations |
| --- | --- | --- |
| [Lab 1 - Foundations of AI Agents](1_foundations/lab1.ipynb) | Environment configuration, provider-key discovery, chat-completion request construction, and a first model call | Python, `python-dotenv`, OpenAI Python SDK, IPython Markdown; optional key checks for OpenAI, Anthropic, Google, DeepSeek, Groq, Grok, and OpenRouter |
| [Lab 2 - Digital Twin Foundations](1_foundations/lab2.ipynb) | System prompts, assistant personas, stateless model behavior, conversation history, PDF-grounded context, manual function calling, and a basic agent loop | OpenAI Chat Completions, `pypdf`, JSON tool schemas, local file output, Gradio |
| [Lab 4 - Digital Twin Project Build](1_foundations/lab4.ipynb) | Multiple tool definitions, tool dispatch, repeated tool-call handling, profile grounding, lead capture, unanswered-question capture, and conversion of the notebook experiment into an application | OpenAI-compatible endpoint, Pushover REST API, `requests`, `pypdf`, Gradio, environment variables |
| [Exercise 1 - Work-Only Gatekeeper](1_foundations/exercise1.ipynb) | A two-stage LLM pipeline in which one model drafts a response and a second model evaluates both the request and draft; structured JSON output; prompt-injection resistance; and fail-closed approval logic | OpenAI-compatible model endpoint, JSON mode, reusable LLM wrapper, IPython Markdown, optional Gradio UI |

### Learning progression

```text
Model call
   -> system prompts and conversation history
   -> external context from PDF/text
   -> function schemas and tool calls
   -> repeated agent/tool loop
   -> external notifications
   -> multi-model evaluation and guardrails
   -> complete Digital Twin application
```

## Technology coverage

### Demonstrated in the current notebooks and project

- Python 3.12 and Jupyter notebooks
- OpenAI Python SDK and OpenAI-compatible API endpoints
- Chat Completions and structured JSON responses
- Prompt engineering and context construction
- Multi-turn conversation history
- Function/tool calling and manual agent loops
- PDF text extraction with `pypdf`
- Gradio chat interfaces with custom CSS and JavaScript
- REST integration with Pushover
- Environment management with `python-dotenv`
- A second-LLM evaluation pattern with fail-closed behavior

### Included in the repository environment for continued exploration

The root `pyproject.toml` also includes Microsoft Agent Framework, Agno, Deep Agents, Google ADK, LangChain, LangGraph, MCP adapters, OpenAI Agents SDK, Pydantic AI, Strands Agents, FastAPI, Plotly, and related libraries. Their presence describes the learning environment; it does not mean every framework is already implemented in the current notebooks.

## Getting started

### Prerequisites

- Python 3.12 or later
- [`uv`](https://docs.astral.sh/uv/) for the repository-wide environment
- A Jupyter-capable editor such as VS Code, or another notebook frontend
- Credentials for only the providers or integrations you plan to run

### Install the repository environment

From the repository root:

```powershell
uv sync
.\.venv\Scripts\Activate.ps1
```

To register the environment as a notebook kernel:

```powershell
python -m ipykernel install --user --name auagents --display-name "auagents"
```

Select the `auagents` kernel when opening a notebook.

### Environment variables

Create a root `.env` file for local development. Not every notebook needs every value.

```dotenv
# OpenAI or an OpenAI-compatible endpoint
OPENAI_API_KEY=replace_with_your_key
OPENAI_BASE_URL=replace_with_your_endpoint

# Used by the Digital Twin notification tools
PUSHOVER_USER=replace_with_your_pushover_user_key
PUSHOVER_TOKEN=replace_with_your_pushover_application_token

# Optional providers explored by the notebooks
ANTHROPIC_API_KEY=replace_if_used
GOOGLE_API_KEY=replace_if_used
DEEPSEEK_API_KEY=replace_if_used
GROQ_API_KEY=replace_if_used
GROK_API_KEY=replace_if_used
OPENROUTER_API_KEY=replace_if_used
```

The `.env` file is ignored by Git. Never place real credentials in notebooks, source files, screenshots, or committed notebook output.

## Repository conventions

- Complete applications belong in `projects/NN_ProjectName/`.
- Each application has its own `README.md` covering purpose, architecture, setup, operation, limitations, and next steps.
- Focused experiments and notes remain in the foundation or future learning folders.
- Project READMEs describe implemented behavior separately from planned work.
- Secrets stay in ignored `.env` files; only variable names and placeholders belong in documentation.
- Generated files, local virtual environments, notebook checkpoints, and caches remain untracked.

## Security and responsible AI notes

- LLM instructions are behavioral controls, not a complete security boundary.
- Tool arguments and model output should be treated as untrusted input.
- Personal profile documents should be reviewed before publishing the repository.
- User contact details should be collected transparently and handled according to an appropriate privacy policy.
- Model responses must remain grounded in documented context; unknown facts should not be invented.
- Provider access, model availability, pricing, and data-handling terms should be verified before deployment.

## Current direction

The repository is moving from foundational model calls toward complete, observable, and secure agentic applications. Near-term areas of study include framework-based agents, MCP integrations, retrieval-augmented generation, evaluation, workflow orchestration, API services, persistence, deployment, and production observability.

## Professional links

- [LinkedIn](https://www.linkedin.com/in/dhavalmmistry/)
- [GitHub](https://github.com/dhaval-mistry/)
- [Medium](https://medium.com/@mahantai)

