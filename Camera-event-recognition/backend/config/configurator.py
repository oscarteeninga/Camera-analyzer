from config.configuration import Configuration


class Configurator:
    def __init__(self, config_file='config/configurations.csv'):
        self.config_file = config_file

    def get_configurations(self):
        configs = {}
        with open(self.config_file, 'r') as f:
            line = f.readline()
            while line:
                line = line.replace("\n", "")
                args = line.split(",")
                config = Configuration.from_arguments(args[0], args[1], args[2])
                print(str(config))
                line = f.readline()
                configs[args[0]] = config
            f.close()
        return configs

    def find_configuration(self, camera_id):
        return self.get_configurations().get(camera_id)

    def add_configuration(self, configuration):
        with open(self.config_file, 'w') as f:
            f.write(str(configuration))
            f.close()

    def delete_configuration(self, camera_ip):
        with open(self.config_file, 'wr') as f:

            f.close()
