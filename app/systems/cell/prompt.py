from utility.runtime import debug


class PromptEngine:
    def __init__(self, command, **prompts):
        self.command = command
        self.prompt_base = "cell/prompt"
        self.prompt_templates = self._load_prompt_templates(prompts)

    def _load_prompt_templates(self, prompts):
        return {name: f"{self.prompt_base}/{file_name}.md" for name, file_name in prompts.items()}

    def render(self, variables):
        rendered = {}

        debug(variables, "Prompt variables")

        for name, template_path in self.prompt_templates.items():
            template = self.command.manager.template_engine.get_template(template_path)
            rendered[name] = template.render(**variables)

        debug(rendered, "Rendered prompts")
        return rendered
