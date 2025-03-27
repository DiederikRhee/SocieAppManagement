import requests
from dataclasses import dataclass
from typing import Optional, List
import os

@dataclass
class Module:
    modified: str
    iconFa: str
    groups: list
    orderNumber: int
    created: str
    community_id: str
    _id: str
    icon: str
    type: str
    name: str
    isEnabled: bool
    media: Optional[list] = None
    pages: Optional[list] = None
    preferences: Optional[dict] = None
    widgets: Optional[list] = None
    preset: Optional[str] = None
    primaryGroupsWidgetEnabled: Optional[bool] = None
    payment: Optional[dict] = None
    external: Optional[dict] = None
    isGuestAllowed: Optional[bool] = None
    primaryItems: Optional[list] = None

@dataclass
class Membership:
    preferences: dict
    created: str
    roles: dict
    feed_id: str
    community_id: str
    _id: str
    person: dict
    address: dict
    extraFields: dict
    status: dict
    modified: Optional[str] = None
    user_id: Optional[str] = None
    privacy: Optional[dict] = None

class SocieConnect():
    def __init__(self, appId: str = os.getenv("appId")):
        self.baseUrl = "https://api.socie.nl"
        self.headers = {
            "platform": "website",
            "Content-Type": "application/json",
        }
        self.appId = appId

    def buildUrl(self, postfix: str):
        return f"{self.baseUrl}/communities/{self.appId}/{postfix}"
    
    def login(self, email: str = os.getenv("email"), password: str = os.getenv("password"), appType: str = "CHURCH"):
        payload = {
            "email": email,
            "password": password,
            "appType": appType
        }   

        response = requests.post(f"{self.baseUrl}/login/socie", json=payload, headers=self.headers)
        response.raise_for_status()
        self.headers["authorization"]= f"{response.json()['token_type']} {response.json()['access_token']}"

    def getModules(self) -> List[Module]:
        response = requests.get(self.buildUrl("modules"), headers=self.headers)
        return [Module(**module_dict) for module_dict in response.json()]
    
    def getMemberships(self) -> List[Membership]:
        response = requests.get(self.buildUrl("memberships"), headers=self.headers)
        return [Membership(**membership_dict) for membership_dict in response.json()]


if __name__ == '__main__':
    api = SocieConnect()
    api.login()

    print (api.getMemberships()[0])

