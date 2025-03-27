import requests
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import os
from functools import cache

@dataclass
class Module:
    name: str
    community_id: str
    icon: str
    _id: str
    groups: str
    type: str
    isEnabled: bool
    modified: datetime
    created: datetime
    iconFa: str
    orderNumber: int
    primaryGroupsWidgetEnabled: Optional[bool] = None
    pages: Optional[str] = None
    isGuestAllowed: Optional[bool] = None
    preset: Optional[str] = None
    payment: Optional[str] = None
    widgets: Optional[str] = None
    external: Optional[str] = None
    media: Optional[str] = None
    primaryItems: Optional[str] = None
    preferences: Optional[str] = None

@dataclass
class Membership:
    preferences: str
    extraFields: str
    created: datetime
    feed_id: str
    person: str
    community_id: str
    _id: str
    roles: str
    address: str
    status: str
    modified: Optional[datetime] = None
    user_id: Optional[str] = None
    privacy: Optional[str] = None

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

    @cache
    def getModules(self) -> List[Module]:
        response = requests.get(self.buildUrl("modules"), headers=self.headers)
        return [Module(**module_dict) for module_dict in response.json()]
    
    def getModuleByName(self, name: str) -> Module:
        return next((module for module in self.getModules() if module.name == name), None)
    
    def getModuleById(self, id: str) -> Module:
        return next((module for module in self.getModules() if module._id == id), None)
    
    @cache
    def getMemberships(self) -> List[Membership]:
        response = requests.get(self.buildUrl("memberships"), headers=self.headers)
        return [Membership(**membership_dict) for membership_dict in response.json()]
    
    


if __name__ == '__main__':
    api = SocieConnect()
    api.login()

    print (api.getModuleByName("weekbrieftestje"))

