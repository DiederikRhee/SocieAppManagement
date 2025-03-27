import requests
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import os
from functools import cache
from enum import Enum

class ModuleTypes(Enum):
    BIRTHDAYS = "BIRTHDAYS"
    DOCUMENTS = "DOCUMENTS"
    DONATIONS = "DONATIONS"
    EVENTS = "EVENTS"
    GROUPS = "GROUPS"
    INFORMATION = "INFORMATION"
    MEMBERS = "MEMBERS"
    NEWS = "NEWS"
    NOTIFICATIONS = "NOTIFICATIONS"
    OVERVIEW = "OVERVIEW"
    STATISTICS = "STATISTICS"
    WEBSITES = "WEBSITES"

@dataclass
class Module:
    icon: str
    community_id: str
    _id: str
    iconFa: str
    orderNumber: int
    modified: datetime
    name: str
    created: datetime
    isEnabled: bool
    type: ModuleTypes
    groups: Optional[List[dict]] = None
    external: Optional[str] = None
    primaryItems: Optional[str] = None
    isGuestAllowed: Optional[bool] = None
    widgets: Optional[str] = None
    preset: Optional[str] = None
    primaryGroupsWidgetEnabled: Optional[bool] = None
    payment: Optional[str] = None
    media: Optional[str] = None
    preferences: Optional[str] = None
    pages: Optional[List[dict]] = None

@dataclass
class Membership:
    roles: str
    community_id: str
    _id: str
    feed_id: str
    extraFields: str
    person: str
    created: datetime
    status: str
    preferences: str
    address: str
    modified: Optional[datetime] = None
    privacy: Optional[str] = None
    user_id: Optional[str] = None


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
    def getMemberships(self) -> List[Membership]:
        response = requests.get(self.buildUrl("memberships"), headers=self.headers)
        return [Membership(**membership_dict) for membership_dict in response.json()]

    @cache
    def getModules(self) -> List[Module]:
        response = requests.get(self.buildUrl("modules"), headers=self.headers)
        return [Module(**module_dict) for module_dict in response.json()]
    
    def getModuleByName(self, name: str) -> Module:
        return next((module for module in self.getModules() if module.name == name), None)
    
    def getModuleById(self, id: str) -> Module:
        return next((module for module in self.getModules() if module._id == id), None)
    
    
    def getDocuments(self, module: Module):
        if (module.type != ModuleTypes.DOCUMENTS.value): return []
        if (len(module.pages) == 0): return []
        if ("_id" not in module.pages[0]): return []

        url = self.buildUrl(f"modules/{module._id}/pages/{module.pages[0]['_id']}/documents")
        return  requests.get(url, headers=self.headers).json()




if __name__ == '__main__':
    api = SocieConnect()
    api.login()

    weekbriefModule = api.getModuleByName("Weekbrief Broederkerk")
    docs = api.getDocuments(weekbriefModule)
    q = 0


