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
    "app/spec/mixins",
    "app/spec/base",
    "app/spec/data",
    "app/spec/plugins",
    "app/spec/commands",
    "app/spec",
    "app/utility",
    "app/systems/manage",
    "app/systems/index",
    "app/systems/db",
    "app/systems/kubernetes",
    "app/systems/encryption",
    "app/systems/models/mixins",
    "app/systems/models/parsers",
    "app/systems/models",
    "app/systems/plugins",
    "app/systems/commands/mixins",
    "app/systems/commands/factory",
    "app/systems/commands",
    "app/systems/cell",
    "app/systems/celery",
    "app/systems/cache",
    "app/systems/api/data",
    "app/systems/api/command",
    "app/systems/api/mcp",
    "app/systems/api",
    "app/systems/client",
    "app/systems",
    "app/data/mixins",
    "app/data/base",
    "app/data/cache",
    "app/data/memory",
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
    "app/plugins/mixins",
    "app/plugins/calculation",
    "app/plugins/channel_token",
    "app/plugins/data_processor",
    "app/plugins/dataset",
    "app/plugins/document_source",
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
    "app/plugins/search_engine",
    "app/plugins/source",
    "app/plugins/task",
    "app/plugins/text_splitter",
    "app/plugins/validator",
    "app/plugins/worker",
    "app/plugins",
    "app/commands/mixins",
    "app/commands/base",
    "app/commands/agent",
    "app/commands/cache",
    "app/commands/chat",
    "app/commands/db",
    "app/commands/file",
    "app/commands/group",
    "app/commands/log",
    "app/commands/module",
    "app/commands/notification",
    "app/commands/qdrant",
    "app/commands/service",
    "app/commands/template",
    "app/commands/user",
    "app/commands/web",
    "app/commands",
    "app/components",
    "app/templates/functions",
    "app/templates/module",
    "app/templates/field",
    "app/templates/data",
    "app/templates/user",
    "app/templates/cell",
    "app/templates",
    "app/tasks",
    "app/profiles/test",
    "app/profiles",
    "app/tests/mixins",
    "app/tests/data",
    "app/tests/command",
    "app/tests/sdk_python",
    "app/tests",
    "app/help",
    "app",
    "sdk/python/bin",
    "sdk/python/zimagi/data",
    "sdk/python/zimagi/command",
    "sdk/python/zimagi",
    "sdk/python",
    "sdk/javascript/src/schema",
    "sdk/javascript/src/transports",
    "sdk/javascript/src/client",
    "sdk/javascript/src/command",
    "sdk/javascript/src/messages",
    "sdk/javascript/src",
    "sdk/javascript/tests",
    "sdk/javascript",
    "sdk",
    "reactor/utilities",
    "reactor/build",
    "reactor/commands",
    "reactor",
    ".circleci",
]


def directory_docs_prompt(dir_path, allowed_files):
    file_list = []

    for file_path in allowed_files:
        file_list.append(
            f"**{os.path.join(dir_path, file_path)}**\n     [**Role:** Short description of the purpose of the file.]\n     [**Detailed Description:** Longer description providing context and detailed information about the file.]"
        )

    """Generate the documentation prompt for a directory."""
    return f"""
Generate a comprehensive **README.rst** file in the **reStructuredText** format for the directory located at: `{dir_path}`.  Include information on only the following files and dirctories: {", ".join([f"**{os.path.join(dir_path, file_path)}**" for file_path in allowed_files])}.

CRITICAL: **NEVER** ask questions or ask for more information!

IMPORTANT: **ONLY** render the readme file with the information you currently have without comments and put the entire README file contents between a ``` fence directly under the README file path.

---

## **Requirements and Context**

1.  **Format:** The entire output *must* be valid **reStructuredText (.rst)** format.
2.  **Target Audience and Purpose:** The generated README is specifically designed to maximize understanding for both **human developers and other AI models** reviewing this codebase. Its primary goal is to clearly and quickly explain the directory's purpose, its contents, and how the source files within it fit into the broader project architecture.
3.  **Detail Level:** Be as **detailed and verbose as possible** to provide rich context. The only exception to this is the exclusion of actual source code.
4.  **Exclusions:** **DO NOT** include any actual lines or blocks of source code from the files. References to files or functions are fine, but the code itself is prohibited.
5.  **Output Use:** This README will be used as a source for developing a documentation site and for generating a high-level, project-wide README.

---

## **Content Sections to Include**

The README.rst must contain the following major sections, using appropriate reStructuredText section headers (e.g., `=====`, `-----`):

### **1. Directory Overview**
* **Purpose:** A concise, high-level explanation of this directory's role within the entire software project.
* **Key Functionality:** What core software features or services are implemented within the files of this directory?

### **2. Platform and Dependencies**
* **Target Platform/Environment:** Specify the operating systems, frameworks, or execution environments this code is designed for (e.g., Python 3.10+, Node.js v18, Kubernetes, specific cloud provider features like AWS Lambda).
* **Local Dependencies:** List and briefly describe any major libraries, packages, or services that the code in this directory heavily relies on. (e.g., 'Requires the `requests` library for HTTP communication.')

### **3. File Structure and Descriptions**
* **File List:** Provide a table or a clear, hierarchical list of all files and sub-directories within `{dir_path}`.
* **Detailed File Descriptions:** For *every* significant source file (e.g., `.py`, `.js`, `.java`, configuration files, etc.), include:
    * The **filename** itself.
    * A **one-sentence summary** of its role.
    * A **detailed paragraph** describing the major functions, classes, or modules it contains and *what* they achieve (not *how* they are coded).
    * Mention its **relationship** to other files in this or other directories.

### **4. Execution Flow and Interconnection**
* **Control Flow:** Describe the typical execution flow or request lifecycle as it relates to the files in this directory. Which file is the entry point? Which files act as helpers, and which handle primary logic?
* **External Interfaces:** Describe how the code in this directory interacts with components **outside** of this directory (e.g., databases, external APIs, message queues, other project services).

---

**Start the Output now, ensuring it begins with a reStructuredText-formatted title for the directory.**

Update the document prompt ro ensure that the AI model generating the documentation does not duplicate files it has already referenced and only contains files it has in its previous context window. It should only generate descriptions for the top level files and directories from the {dir_path} template variable. Also add an exact example README at the bottom so that the AI models knows exactly how to structure each README file with help information for each information instead of the actual information. Also add help information that ensures that the AI model does not hallucinate extra files that do not exist, which it does with the current prompt. The AI model gnerating the documentation id Gemini 2.5 Flash (the same as this one) so write the prompt for yourself to accomplish the task in the most accurate way possible.

Here is the updated and refined prompt, specifically tailored for Gemini 2.5 Flash, incorporating all your requirements, including file non-duplication, focusing only on top-level files, and providing a structural template to prevent hallucination.

**Prompt for Gemini 2.5 Flash: Generate Detailed, Top-Level reStructuredText README for Codebase Directory**

Generate a comprehensive **README.rst** file in the **reStructuredText** format for the directory located at: `{dir_path}`.

---

## **AI Model Directives and Constraints**

1.  **Format:** The entire output *must* be strictly valid **reStructuredText (.rst)** format.
2.  **Scope Limitation:** **CRITICAL:** Only describe the **top-level files and directories** immediately within `{dir_path}`. **DO NOT** recursively describe files in subdirectories.
3.  **Non-Hallucination Mandate:** **CRITICAL:** **DO NOT** invent, assume, or hallucinate the existence of files or directories that are not explicitly present in the provided context window for `{dir_path}`. Use only the actual files and directories you have been supplied.
4.  **Non-Duplication Mandate:** **CRITICAL:** Ensure that every file or directory is mentioned and described **only once** within the document, primarily in the "File Structure and Descriptions" section.
5.  **Exclusions:** **DO NOT** include any actual lines or blocks of source code. References to files, functions, or concepts are fine, but the code itself is prohibited.
6.  **Target Audience:** Maximize understanding for both **human developers and other AI models** reviewing this codebase. The goal is context-rich, architecture-focused documentation.
7.  **Detail Level:** Be as **detailed and verbose as possible** for the files that *are* included in the scope.

---

## **Content Sections to Include**

The README.rst must strictly adhere to the following structure and section headers, using appropriate reStructuredText formatting (e.g., `=====`, `-----`).

### **1. Directory Overview**
* **Purpose:** A concise, high-level explanation of this directory's role within the entire software project.
* **Key Functionality:** What core software features or services are implemented within the top-level contents of this directory?

### **2. Platform and Dependencies**
* **Target Platform/Environment:** Specify the operating systems, frameworks, or execution environments this code is designed for.
* **Local Dependencies:** List and briefly describe any major libraries, packages, or services that the code in this directory heavily relies on.

### **3. File Structure and Descriptions**
* **File List and Descriptions:** Use a definition list or a descriptive list structure (as shown in the template below) to list **every** top-level file and subdirectory, followed by a detailed description.

### **4. Execution Flow and Interconnection**
* **Control Flow:** Describe the typical execution flow or request lifecycle as it relates to the files in this directory. Which file is the entry point? Which files act as primary logic?
* **External Interfaces:** Describe how the code in this directory interacts with components **outside** of this directory (e.g., databases, external APIs, message queues).

---

## **REQUIRED Output Structure Template**

The final output **must** follow this exact format, replacing the bracketed help text with the actual generated content for `{dir_path}`.

```rst
=====================================================
README for Directory: {dir_path}
=====================================================

.. The title uses a double underline for the top-level heading.

Directory Overview
------------------
.. This section uses a single underline for the secondary heading.

**Purpose**
   [Provide a high-level, one-paragraph explanation of the directory's primary role and context within the larger project architecture. For example: "This directory contains the core business logic implementation for the user authentication and authorization services."]

**Key Functionality**
   [List 3-5 major software features or services implemented here. For example: User registration, token generation/validation, password reset logic.]


Dependencies
-------------------------

[List and briefly describe major third-party libraries or internal components required. E.g., `sqlalchemy` for ORM, `pydantic` for data validation.]


File Structure and Descriptions
-------------------------------
.. DO NOT recurse into subdirectories. DO NOT hallucinate files.  CRITICAL: Only include the following directories and files.

{"\n\n".join(file_list)}


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   [Provide a clear, step-by-step description of the primary execution flow (e.g., "1. An HTTP request hits a route defined in `app.py`. 2. The handler calls a method in `service.py`. 3. `service.py` interacts with `models.py` to fetch data."). **CRITICAL: Ensure all files mentioned are top-level files within this directory.**]

**External Interfaces**
   [Describe all connections to systems outside of this directory's immediate scope. For example: "Communicates with the external `NotificationService` via a REST API," or "Reads/Writes data to the primary PostgreSQL database."]
"""


@contextmanager
def run_quiet(output=None):
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


class DocumentCoder(Coder):

    def check_for_file_mentions(self, content):
        return


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
        model,
        write_files=None,
        read_files=None,
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
        self._coder = DocumentCoder.create(
            main_model=self._model,
            edit_format=self._model.edit_format,
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

    def run(self, message):
        """Run an Aider command."""
        output = StringIO()
        with run_quiet(output):
            self._coder.run(message)
        return output.getvalue()


class DocGenerator:
    """Generates documentation for directories while skipping specified patterns."""

    def __init__(self, doc_sequence):
        self.doc_sequence = doc_sequence

    def generate_docs(self):
        """Main documentation generation workflow."""
        core_files = [
            "start",
            "clean",
            "zimagi",
            "compose.network.yaml",
            "compose.db.yaml",
            "compose.standard.local.yaml",
            "compose.standard.test.yaml",
            "compose.nvidia.local.yaml",
            "compose.nvidia.test.yaml",
        ]
        docs_state_file = os.path.join(".", ".docs-index")
        docs_log_file = os.path.join(".", ".docs-log")

        model = "openrouter/google/gemini-2.5-flash"
        max_input_tokens = 800000
        output_token_context = 10000

        try:
            with open(docs_state_file) as file:
                docs_index = int(file.read())
        except FileNotFoundError:
            docs_index = None

        for dir_index, dir_path in enumerate(self.doc_sequence):
            if os.path.isdir(dir_path):
                readme_file = os.path.join(dir_path, "README.rst")
                dir_files = self._get_top_level_items(dir_path)
                doc_prompt = directory_docs_prompt(dir_path, dir_files)

                if docs_index is None or dir_index >= docs_index:
                    session = Aider(
                        model,
                        write_files=readme_file,
                        read_files=[dir_path, *core_files],
                    )
                    if (
                        session.info.total_tokens <= max_input_tokens
                        and session.info.remaining_tokens >= output_token_context
                    ):
                        write_files = []
                        read_files = []

                        for file_path, file_info in sorted(
                            session.info.export()["files"].items(), key=lambda item: item[1]["tokens"], reverse=True
                        ):
                            file_string = f"{file_path}: {file_info["tokens"]} tokens"
                            if file_info["readonly"]:
                                read_files.append(f"R> {file_string}")
                            else:
                                write_files.append(f"W> {file_string}")

                        dir_info = f"Documenting directory: {dir_path} ( {session.info.total_tokens} tokens )"
                        context_info = (
                            f" '-> Context files:\n{"\n".join([f"    {file}" for file in [*write_files, *read_files]])}"
                        )

                        print(dir_info)
                        response = session.run(doc_prompt)

                        with open(docs_log_file, "a") as file:
                            file.write(f"{dir_info}\n{context_info}\n{response}\n\n")

                        if os.stat(readme_file).st_size == 0:
                            print(f"Failed to generate README file for {dir_path}")
                            exit(1)

                    with open(docs_state_file, "w") as file:
                        file.write(str(dir_index))
            else:
                print(f"Directory does not exist: {dir_path}")
                exit(1)

        os.remove(docs_state_file)
        os.remove(docs_log_file)

    def _get_top_level_items(self, search_path):
        parent_path = str(search_path)
        directories = []
        files = []

        for file_name in os.listdir(parent_path):
            path = os.path.join(search_path, file_name)
            if os.path.isdir(path):
                directories.append(file_name)
            else:
                files.append(file_name)

        return [*directories, *files]


if __name__ == "__main__":
    generator = DocGenerator(doc_sequence)
    generator.generate_docs()
