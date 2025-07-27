#!/usr/bin/env python3
# flake8: noqa

import json
import os
import re
import sys
from contextlib import contextmanager
from io import StringIO
from pathlib import Path

from aider.coders import Coder
from aider.commands import Commands, SwitchCoder
from aider.io import InputOutput
from aider.models import Model
from aider.utils import is_image_file

doc_sequence = [
    "docker",
    "env",
    "app/scripts",
    "app/services",
    "app/settings",
    "app/spec",
    "app/spec/mixins",
    "app/spec/base",
    "app/spec/data",
    "app/spec/plugins",
    "app/spec/commands",
    "app/spec",
    "app/utility",
    "app/systems",
    "app/systems/manage",
    "app/systems/index",
    "app/systems/db",
    "app/systems/kubernetes",
    "app/systems/encryption",
    "app/systems",
    "app/systems/models",
    "app/systems/models/mixins",
    "app/systems/models/parsers",
    "app/systems/models",
    "app/systems/plugins",
    "app/systems/commands",
    "app/systems/commands/mixins",
    "app/systems/commands/factory",
    "app/systems/commands",
    "app/systems/cell",
    "app/systems/celery",
    "app/systems/cache",
    "app/systems/api",
    "app/systems/api/data",
    "app/systems/api/command",
    "app/systems/api/mcp",
    "app/systems/api",
    "app/systems/client",
    "app/systems",
    "app/data",
    "app/data/mixins",
    "app/data/base",
    "app/data/cache",
    "app/data/chat",
    "app/data/config",
    "app/data/dataset",
    "app/data/group",
    "app/data/host",
    "app/data/log",
    "app/data/module",
    "app/data/notification",
    "app/data/scaling_event",
    "app/data/schedule",
    "app/data/state",
    "app/data/user",
    "app/data",
    "app/plugins",
    "app/plugins/mixins",
    "app/plugins/calculation",
    "app/plugins/channel_token",
    "app/plugins/data_processor",
    "app/plugins/dataset",
    "app/plugins/encoder",
    "app/plugins/encryption",
    "app/plugins/field_processor",
    "app/plugins/file_parser",
    "app/plugins/formatter",
    "app/plugins/function",
    "app/plugins/language_model",
    "app/plugins/message_filter",
    "app/plugins/module",
    "app/plugins/parser",
    "app/plugins/qdrant_collection",
    "app/plugins/source",
    "app/plugins/task",
    "app/plugins/text_splitter",
    "app/plugins/validator",
    "app/plugins/worker",
    "app/plugins",
    "app/commands",
    "app/commands/mixins",
    "app/commands/base",
    "app/commands/agent",
    "app/commands/cache",
    "app/commands/chat",
    "app/commands/db",
    "app/commands/group",
    "app/commands/log",
    "app/commands/module",
    "app/commands/notification",
    "app/commands/qdrant",
    "app/commands/service",
    "app/commands/template",
    "app/commands/user",
    "app/commands",
    "app/components",
    "app/templates",
    "app/templates/functions",
    "app/templates/module",
    "app/templates/field",
    "app/templates/data",
    "app/templates/user",
    "app/templates/cell",
    "app/templates",
    "app/tasks",
    "app/profiles",
    "app/profiles/test",
    "app/profiles",
    "app",
    "app/tests",
    "app/tests/mixins",
    "app/tests/data",
    "app/tests/command",
    "app/tests/sdk_python",
    "app/tests",
    "app",
    "app/help",
    "app",
    "package",
    "package/bin",
    "package/zimagi",
    "package/zimagi/data",
    "package/zimagi/command",
    "package/zimagi",
    "package",
    "reactor",
    "reactor/utilities",
    "reactor/build",
    "reactor/commands",
    "reactor",
    ".circleci",
]


def directory_docs_prompt(dir_path: Path) -> str:
    """Generate the documentation prompt for a directory."""
    return f"""
# AI Instruction Prompt: Create or update the README for `{dir_path}`

## Task
Generate a comprehensive and accurate `README.md` file for the `{dir_path}` directory. This file should provide both **humans** and **AI models** with a clear and structured understanding of the contents of this directory **without requiring them to inspect each individual file**.

## Goals
- Summarize the **purpose and structure** of `{dir_path}`
- List and describe all **files** and **subdirectories**
- Use context from **parent and child README files** when available
- Support **human onboarding** and **AI-driven development**
- Ensure **accuracy**, **clarity**, and **completeness**

## Background

For a general reference, this project contains the following top level directories:

- .circleci: The .circleci directory contains all CI/CD related build, test, and deploy jobs for the CircleCI service
- app: The app directory contains all of the server application files as well as gateway entrypoint scripts
    - app/scripts: The scripts directory contains Docker entrypoint scripts and command / server configurations as well as a few helpers
    - app/services: The services directory contains various Django service gateways and url definitions, and a Celery service gateway
    - app/settings: The settings directory contains Django settings files, various utilities for working with configurations, and Celery task collection
    - app/utility: The utility directory contains a collection of specialized utilities used across the application and modules
    - app/systems: The systems directory contains integrated systems that implement components of the overarching application
    - app/spec: The spec directory contains YAML specifications that power meta-programming code genration for various component systems of the application
    - app/data: The data directory contains Django data model apps that are available through CLI or APIs, each with model and model facade classes and model migrations
    - app/commands: The commands directory contains executable commands and agents that are available through CLI or APIs
    - app/components: The components directory contains various YAML command profile component processors
    - app/help: The help directory contains language based help information for Zimagi commands
    - app/plugins: The plugins directory contains various plugin types and provider implementations
    - app/profiles: The profiles directory contains various YAML command profiles
    - app/tasks: The tasks directory contains various YAML command execution task definitions
    - app/templates: The templates directory contains various Jinja2 templates for various component systems
    - app/tests: The tests directory contains the test frameworks and various test libraries
- docker: The docker directory contains the server and client Dockerfiles, as well as build and deploy scripts
- env: The env directory contains the environment variables loaded into Docker Compose manifests in the top level directory.
- package: The package directory contains a Python SDK client library for interacting with the Zimagi server API endpoints and a CLI executable
- reactor: The reactor directory contains file that integrate with the Reactor Kubernetes development and management platform, which includes Docker build argument files, utility libraries, and a zimagi executable that integrates with the reactor CLI.

---

## Instructions

### 1. Overview
Begin with a high-level explanation of `{dir_path}`:
- What is this directory for?
- How does it relate to the overall project (use parent READMEs for context)?
- Who uses it (humans, build systems, AI models)?
- What architectural or functional role does it play?

---

### 2. Directory Contents Table
List all **files and subdirectories** except README files within `{dir_path}`.
For each:

#### Files:
- **Name**
- **Purpose** and what it does
- Language or format (e.g., `.ts`, `.json`, `.md`)

#### Subdirectories:
- **Name**
- **Purpose** and what kinds of files it contains
- Link to its own README if present (e.g., `See subdir/README.md`)

---

### 3. Cross-Referencing
- Use **README files in parent directories** to establish context
- Use **README files in child directories** to summarize their content
- Clearly show how `{dir_path}` fits into the broader structure

---

### 4. Key Concepts, Conventions, and Patterns
Document:
- **Naming conventions** (e.g., `*.test.ts`)
- **File organization** (e.g., by domain, by feature)
- **Standards** used (e.g., TypeScript strict mode, JSON schema)
- Any **domain-specific logic** or rules relevant to this directory

---

### 5. Developer Notes and Usage Tips
Include any important developer information:
- Build requirements
- External dependencies or environment variables
- Tips for editing or generating files in this directory
- AI-specific guidance if models are expected to generate content here

---

## Final Checklist

- [ ] All files and subdirectories are listed and described
- [ ] Purpose and usage of each file are clearly explained
- [ ] Cross-references to related README files are accurate
- [ ] Descriptions are verbose, meaningful, and non-generic
- [ ] No assumptions made without filename or content support
- [ ] English is clear, professional, and helpful for AI + humans
- [ ] The README gives a **standalone** understanding of `{dir_path}`

---

## Output Format

Produce a `README.md` file using **standard Markdown**, including:
- `#`-style headers
- Bullet lists or tables
- Do not include code snippets or code blocks in the output file
"""


@contextmanager
def run_quiet(output: StringIO = None):
    try:
        if not output:
            output = StringIO()

        sys.stdout = output
        yield

    except Exception as error:
        sys.stdout = sys.__stdout__
        print(output.getvalue())
        raise error
    finally:
        sys.stdout = sys.__stdout__


class AiderFileInfo:

    def __init__(self, name, tokens, token_unit_cost, readonly=False):
        self.name = name
        self.readonly = readonly
        self.tokens = tokens
        self.cost = tokens * token_unit_cost

    def __str__(self):
        return json.dumps(self.export(), indent=2)

    def export(self):
        return {
            "name": self.name,
            "readonly": self.readonly,
            "tokens": self.tokens,
            "cost": self.cost,
        }


class AiderSessionInfo:
    """Stores information about the current Aider session"""

    def __init__(self, session):
        self._session = session
        self._coder = session.coder
        self._io = session.io

        self._fence = "`" * 3
        self.load()

    def __str__(self):
        return json.dumps(self.export(), indent=2)

    def export(self):
        return {
            "model": self.model_name,
            "token_unit_cost": self.token_unit_cost,
            "system_tokens": self.system_tokens,
            "system_token_cost": self.system_token_cost,
            "chat_tokens": self.chat_tokens,
            "repo_map_tokens": self.repo_map_tokens,
            "repo_map_token_cost": self.repo_map_token_cost,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "max_tokens": self.max_tokens,
            "remaining_tokens": self.remaining_tokens,
            "files": {file_path: info.export() for file_path, info in self.files.items()},
        }

    @property
    def model_name(self):
        return self._session.model_name

    @property
    def token_unit_cost(self):
        return self._coder.main_model.info.get("input_cost_per_token") or 0

    @property
    def max_tokens(self):
        return self._coder.main_model.info.get("max_input_tokens") or 0

    def reset(self):
        """Resets token counts and pricing information."""
        self.system_tokens = 0
        self.system_token_cost = 0
        self.chat_tokens = 0
        self.chat_token_cost = 0
        self.repo_map_tokens = 0
        self.repo_map_token_cost = 0
        self.total_tokens = 0
        self.total_cost = 0
        self.remaining_tokens = 0
        self.files = {}

    def load(self):
        """Extracts token counts and pricing information from chat session."""
        self.reset()
        self._coder.choose_fence()

        messages = self._get_system_messages()
        self.system_tokens = self._coder.main_model.token_count(messages)
        self.system_token_cost = self.system_tokens * self.token_unit_cost

        messages = self._coder.done_messages + self._coder.cur_messages
        if messages:
            self.chat_tokens = self._coder.main_model.token_count(messages)
            self.chat_token_cost = self.chat_tokens * self.token_unit_cost

        files = set(self._coder.get_all_abs_files()) - set(self._coder.abs_fnames)
        if self._coder.repo_map:
            repo_content = self._coder.repo_map.get_repo_map(self._coder.abs_fnames, files)
            if repo_content:
                self.repo_map_tokens = self._coder.main_model.token_count(repo_content)
                self.repo_map_token_cost = self.repo_map_tokens * self.token_unit_cost

        for file_path in self._coder.abs_fnames:
            relative_file_path = self._coder.get_rel_fname(file_path)
            content = self._io.read_text(file_path)

            if is_image_file(relative_file_path):
                tokens = self._coder.main_model.token_count_for_image(file_path)
            else:
                content = f"{relative_file_path}\n{self._fence}\n" + content + f"{self._fence}\n"
                tokens = self._coder.main_model.token_count(content)

            self.files[relative_file_path] = AiderFileInfo(relative_file_path, tokens, self.token_unit_cost, False)

        for file_path in self._coder.abs_read_only_fnames:
            relative_file_path = self._coder.get_rel_fname(file_path)
            content = self._io.read_text(file_path)

            if content is not None and not is_image_file(relative_file_path):
                content = f"{relative_file_path}\n{self._fence}\n" + content + f"{self._fence}\n"
                tokens = self._coder.main_model.token_count(content)

                self.files[relative_file_path] = AiderFileInfo(relative_file_path, tokens, self.token_unit_cost, True)

        self.total_tokens = self.system_tokens + self.chat_tokens + self.repo_map_tokens
        self.total_cost = self.system_token_cost + self.chat_token_cost + self.repo_map_token_cost
        for file_path, info in self.files.items():
            self.total_tokens += info.tokens
            self.total_cost += info.cost

        self.remaining_tokens = self.max_tokens - self.total_tokens
        return self

    def _get_system_messages(self):
        system_message = self._coder.fmt_system_prompt(self._coder.gpt_prompts.main_system)
        system_message += "\n" + self._coder.fmt_system_prompt(self._coder.gpt_prompts.system_reminder)
        return [
            {"role": "system", "content": system_message},
            {"role": "system", "content": self._coder.fmt_system_prompt(self._coder.gpt_prompts.system_reminder)},
        ]


class Aider:
    """Interfaces with the Aider AI development tool to manage repositories."""

    def __init__(
        self,
        write_files=None,
        read_files=None,
        model="openrouter/qwen/qwen3-coder",
        io=None,
        commit=False,
        **kwargs,
    ):
        self.model_name = model
        self._model = Model(self.model_name)
        self._start(write_files, read_files, io=io, commit=commit, **kwargs)

    @property
    def coder(self):
        return self._coder

    @property
    def io(self):
        return self._io

    @property
    def info(self):
        """Extracts token counts and pricing information from the model context."""
        return self._info

    def _start(self, write_files=None, read_files=None, io=None, commit=False, **kwargs):
        """Start a new Aider chat session."""
        self._io = InputOutput(pretty=False, fancy_input=False, yes=True) if io is None else io
        self._coder = Coder.create(
            main_model=self._model,
            io=self._io,
            auto_commits=commit,
            **kwargs,
        )
        self._session = Commands(self._io, self._coder)
        self._info = AiderSessionInfo(self)
        if write_files:
            self.add_write_files(write_files)
        if read_files:
            self.add_read_files(read_files)

    def add_write_files(self, files):
        """Add writable files to the Aider chat session."""
        with run_quiet():
            for file in files if isinstance(files, (list, tuple)) else [files]:
                self._session.cmd_add(str(file))
            self._info.load()

    def add_read_files(self, files):
        """Add readonly files to the Aider chat session."""
        with run_quiet():
            for file in files if isinstance(files, (list, tuple)) else [files]:
                self._session.cmd_read_only(str(file))
            self._info.load()

    def run(self, command, message=""):
        """Run an Aider command."""
        output = StringIO()
        with run_quiet(output):
            try:
                getattr(self._session, f"cmd_{command}")(message)
            except SwitchCoder:
                pass
        return output.getvalue()

    def ask(self, message):
        """Run an Aider ask command."""
        return self.run("ask", message)

    def architect(self, message):
        """Run an Aider architect command."""
        return self.run("architect", message)

    def code(self, message):
        """Run an Aider code command."""
        return self.run("code", message)


class DocGenerator:
    """Generates documentation for directories while skipping specified patterns."""

    def __init__(self, doc_sequence, output_token_context=3000, max_tokens=200000):
        self.doc_sequence = doc_sequence
        self.output_token_context = output_token_context
        self.max_tokens = max_tokens

    def generate_docs(self):
        """Main documentation generation workflow."""
        readme_context = {}
        docs_state_file = os.path.join(".", ".docs-index")

        try:
            with open(docs_state_file) as file:
                docs_index = int(file.read())
        except FileNotFoundError:
            docs_index = None

        for dir_index, dir_path in enumerate(self.doc_sequence):
            if os.path.isdir(dir_path):
                readme_file = os.path.join(dir_path, "README.md")
                readme_files = list(readme_context.values())
                readme_generated = False

                if docs_index is None or dir_index >= docs_index:
                    while not readme_generated or os.stat(readme_file).st_size == 0:
                        session = Aider(write_files=readme_file, read_files=[dir_path, *readme_files])
                        if (
                            session.info.total_tokens > self.max_tokens
                            or session.info.remaining_tokens < self.output_token_context
                        ):
                            session = Aider(write_files=readme_file, read_files=readme_files)
                        if (
                            session.info.total_tokens > self.max_tokens
                            or session.info.remaining_tokens < self.output_token_context
                        ):
                            session = Aider(
                                write_files=readme_file, read_files=self._get_readme_files(dir_path, readme_context)
                            )
                        if (
                            session.info.total_tokens <= self.max_tokens
                            and session.info.remaining_tokens >= self.output_token_context
                        ):
                            print(f"Documenting directory: {dir_path}")
                            print("----------------------------------------------------------------------")
                            print(session.code(directory_docs_prompt(dir_path)))
                            with open(docs_state_file, "w") as file:
                                file.write(str(dir_index))

                            readme_generated = True

                readme_context[dir_path] = readme_file
            else:
                print(f"Directory does not exist: {dir_path}")

        os.remove(docs_state_file)

    def _get_readme_files(self, search_path, readme_context):
        parent_path = str(search_path)
        readme_files = set()

        while "/" in parent_path:
            parent_path = "/".join(parent_path.split("/")[:-1])
            if parent_path in readme_context:
                readme_files.add(readme_context[parent_path])

        for dir_path, readme_path in readme_context.items():
            if str(dir_path).startswith(str(search_path)):
                readme_files.add(readme_path)

        return sorted(readme_files)


if __name__ == "__main__":
    generator = DocGenerator(doc_sequence)
    generator.generate_docs()
