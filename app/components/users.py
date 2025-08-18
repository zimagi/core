from systems.commands import profile
from utility.data import ensure_list


class ProfileComponent(profile.BaseProfileComponent):
    def priority(self):
        return 10

    def run(self, name, config):
        groups = self.pop_values("groups", config)
        self.exec(
            "user save",
            user_key=name,
            user_fields=config,
            groups_keys=[] if not groups else ensure_list(groups),
            local=self.command.local,
        )

    def destroy(self, name, config):
        self.exec("user remove", user_key=name, force=True, local=self.command.local)
