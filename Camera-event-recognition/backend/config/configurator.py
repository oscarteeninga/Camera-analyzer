class Configurator:
    def __init__(self, config_file='configurations.csv'):
        self.config_file = config_file

    def get_configurations(self):
        with open(self.config_file, 'r') as f:
            configs = {}
            f.close()
            return configs

    def find_configuration(self, camera_ip):
        self.get_configurations().get(camera_ip)

    def add_configuration(self, configuration):
        with open(self.config_file, 'w') as f:
            f.write(configuration.__str__)
            f.close()

    def delete_configuration(self, camera_ip):
        with open(self.config_file, 'r') as f:
            f.close()
