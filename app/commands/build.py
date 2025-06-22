from systems.commands.index import Command


class Build(Command("build")):
    def exec(self):
        self.info("Executing build process")
