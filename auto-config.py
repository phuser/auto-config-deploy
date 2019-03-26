from jinja2 import Environment, FileSystemLoader
import yaml
import napalm
from time import sleep

# Definition variables
my_device = {'hostname': '10.3.255.103',
             'username': 'python',
             'password': 'cisco'
             }


def creat_config():
    # Load data from YAML into Python dict
    yaml_file = open('config-device1.yml')
    config_data = yaml.load(yaml_file)

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    # template = env.get_template('template.j2')
    template = env.get_template('original.j2')

    # Render the template with data and print the output
    for config_device in config_data:
        config = template.render(config_device)

    # print('The config is:')
    # print(config)
    # print('-'*150)
    return config


def connect_device(config):
    print('Connect to device and diff config:')
    driver = napalm.get_network_driver('ios')
    with driver(**my_device) as device:
        device.load_merge_candidate(config=config)
        config_diff = device.compare_config()

    if len(config_diff) != 0:
        print('Config has changed:')
        print(config_diff)
    else:
        print('Nothing changed!')


if __name__ == '__main__':
    while True:
        device_config = creat_config()
        connect_device(device_config)
        i = 0
        print('Sleep for 60s!')
        for i in range(0, 60):
            print('+', end='', flush=True)
            sleep(1)
        print('\n')
