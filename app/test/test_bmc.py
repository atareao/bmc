#!/usr/bin/env python3

import unittest
import sys
import os
sys.path.append(os.path.join("../src"))
from bmc import BMC
from member import Member
from utils import load_env


class TestBMC(unittest.TestCase):
    def test_get_active_members(self):
        bmc_client = BMC(os.getenv('BMC_BASE_URI'),
                         os.getenv('BMC_ACCESS_TOKEN'))
        members = bmc_client.get_active_members()
        for member in members:
            print(member)
        self.assertGreater(len(members), 0, "Should be greater than 0")

    def test_user(self):
        amember = Member(None, None)
        print("---")
        print(amember)


if __name__ == '__main__':
    load_env(os.path.abspath("../../bmc.env"))
    print("=== Start ===")
    unittest.main()
