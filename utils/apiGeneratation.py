import requests
import sys

from codeGeneration import generate_dataclass
sys.path.append('../SocieAppManagement')

from socieconnect import SocieConnect

if __name__ == '__main__':
    api = SocieConnect()
    api.login()

    print (generate_dataclass("Module", requests.get(api.buildUrl("modules"), headers=api.headers).json()))
    print (generate_dataclass("Membership", requests.get(api.buildUrl("memberships"), headers=api.headers).json()))