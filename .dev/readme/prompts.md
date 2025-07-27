# Research Prompts (for use in generating other project files)

The following prompts are designed to be employed by a high end reasoning model. Since this process is very human interaction driven this research process does not require the API and can be conducted over web based chat sessions.

This research feeds the Aider build process, as we share the project directory with the AI model to help define the goals, rules, and ultimate outcome.

The following prompts are based on a workflow by Harper Reed (https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/)

## Initial exploratory project planning

Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. Remember, only one question at a time.

Here’s is the goal:

I need to generate an accurate and comprehensive top level README.md file for the Zimagi project. I have a collection of README files from all of the subdirectories that can feed information to this README file generation. I need to design a really effective README file that highlights the important points of the Zimagi project, architecture, and design philosophy. This README file should revolve around the concept of an integrated system for multi-agent systems, or a multi cellular brain, since our core AI agents are called and modelled after biological cells. We are creating a growing, adaptive system that can federate across the web, and operate on physical hardware, like laptops, servers, and clusters, and cloud services in a hybrid cloud model. I need to understand what needs to go into this README to make it shine so we can create a specification for it to develop it out. I need a specification that is simple enough that a new human programmer and a machine can understand in a standardized format across files.

## Specification generation (after AI QA session)

Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification in Markdown format in the .dev/readme/spec.md file? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation. Be as detailed as possible with the information you have been given.

## Project planning

Draft a detailed, step-by-step blueprint for building this project in Markdown format in the .dev/readme/plan.md file. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use Markdown format. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

## TODO file

Generate a TODO list in Markdown format in the .dev/readme/todo.md file that we can use as a checklist to guide AI in completing the project outlined in the specifications and project plan? Be thorough.

## Project kickoff

Implement the README project in the order specified in .dev/readme/todo.md file. Use the related plan sections in the .dev/readme/plan.md file to provide more clarification about the deliverables. Use the README files from the subdirectories to understand the project as you are making changes to the README file so we can ensure accuracy. Make sure we have a accurate way to test the work in each phase of execution.

As you complete each task, please update the TODO list in .dev/readme/todo.md by checking off the corresponding item under the current phase and section you have completed. Do not modify the TODO list items.

The content should follow the specification defined in .dev/readme/spec.md.
