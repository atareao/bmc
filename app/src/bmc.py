#!/usr/bin/env python3

import requests
from user import User

BASE_URI = 'https://developers.buymeacoffee.com'

class BMC:
    def __init__(self, token):
        self._token = token

    def get_active_members(self):
        users = []
        url = f"{BASE_URI}/api/v1/subscriptions?status=active&page=1"
        while url is not None:
            url, new_users = self._get_active_members(url)
            users.extend(new_users)
        return users

    def _get_active_members(self, url):
        users = []
        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                url = data['next_page_url']
                for item in data['data']:
                    an_user = User.from_json(item)
                    an_user.is_member = True
                    users.append(an_user)
                return url, users
        except Exception as exception:
            print(exception)
        return None, users


