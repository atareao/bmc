#!/usr/bin/env python3

import unittest
import sys
import os
sys.path.append(os.path.join("../src"))
from bmc import BMC
from user import User

BMC_TOKEN = os.getenv("BMC_ACCESS_TOKEN")

class TestBMC(unittest.TestCase):
    def test_get_active_members(self):
        print(BMC_TOKEN)
        bmc_client = BMC(BMC_TOKEN)
        users = bmc_client.get_active_members()
        for user in users:
            print(user)
        self.assertGreater(len(users), 0, "Should be greater than 0")

    def test_user(self):
        an_user = User(None, None)
        print("---")
        print(an_user)


if __name__ == '__main__':
    unittest.main()
