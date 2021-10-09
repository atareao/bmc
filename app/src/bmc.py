#!/usr/bin/env python3

import requests
from member import Member
from utils import Log


class BMC:
    def __init__(self, base_uri, token):
        self._base_uri = base_uri
        self._token = token

    def get_active_members(self):
        members = []
        url = f"{self._base_uri}/api/v1/subscriptions?status=active&page=1"
        Log.info(url)
        while url is not None:
            url, new_members = self._get_active_members(url)
            members.extend(new_members)
        return members

    def _get_active_members(self, url):
        members = []
        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                url = data['next_page_url']
                for item in data['data']:
                    amember = Member(item['payer_name'], item['payer_email'])
                    members.append(amember)
                return url, members
        except Exception as exception:
            Log.error(exception)
        return None, members


