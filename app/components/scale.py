from systems.commands import profile


class ProfileComponent(profile.BaseProfileComponent):
    def priority(self):
        return 95

    def run(self, name, count):
        if count is None:
            self.command.error(f"Agent {name} scaling requires count to be set (set to 0 for none)")

        self.exec(
            "scale",
            agent_name=name,
            agent_count=count,
            local=True,
        )
