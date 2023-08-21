class ControllerConfig(object):
    def __init__(self, name, behavior_func):
        self.name = name
        self.behavior_func = behavior_func

    def execute_behavior(self, frame):
        self.behavior_func(frame)

class ConfigurationManager(object):
    def __init__(self):
        self.configs = {}
        self.selected_config = None

    def add_config(self, config):
        if config.name in self.configs:
            raise ValueError("Configuration with name '{}' already exists.".format(config.name))
        self.configs[config.name] = config

    def select_config(self, name):
        if name not in self.configs:
            raise ValueError("Configuration with name '{}' does not exist.".format(name))
        
        self.selected_config = self.configs[name]

    def execute_selected_behavior(self, frame):
        if self.selected_config:
            self.selected_config.execute(frame)

