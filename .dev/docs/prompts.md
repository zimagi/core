# Research Prompts (for use in generating other project files)

The following prompts are designed to be employed by a high end reasoning model. Since this process is very human interaction driven this research process does not require the API and can be conducted over web based chat sessions.

This research feeds the Aider build process, as we share the project directory with the AI model to help define the goals, rules, and ultimate outcome.

The following prompts are based on a workflow by Harper Reed (https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/)

## Initial exploratory project planning

Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s is the goal:

I need to generate an accurate and comprehensive documentation site for this Python Django application and it's corresponding PyPI package, which serves as a Python SDK for the server.  This documentation site should be built with Sphinx Python documentation package and live in the docs directory, which has a deploy script used to build and deploy the documentation site.  I have a scaffolding documentation site but I need a documentation site that is organized for developer and end user efficiency, with pages on philosophy of the project, goals, architectural patterns, different guides, such as a getting started guide or an agent developer guide.  This documentation site should be composed of Markdown (md) or reStructuredText (rst) files.  Each section of the documentation site that is a directory with subpages should have a top level readme.  I have a scaffolding documentation project in the docs directory that builds and deploys a documentation site in Sphinx and I now need to fill in the content with engaging easily understood and followable instructions and help information with tables and mermaid diagrams where it makes sense.  I need a specification that is simple enough that a new human programmer and a machine can understand in a standardized format across files.

## Specification generation (after AI QA session)

Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification in Markdown format in the .dev/docs/spec.md file? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation. Be as detailed as possible with the information you have been given.

## Project planning

Draft a detailed, step-by-step blueprint for building this project in Markdown format in the .dev/docs/plan.md file. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use Markdown format. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

## TODO file

Generate a TODO list in Markdown format in the .dev/docs/todo.md file that we can use as a checklist to guide AI in completing the project outlined in the specifications and project plan? Be thorough.
