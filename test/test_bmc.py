#!/usr/bin/env python3

import unittest
import sys
import os
sys.path.append(os.path.join("../src"))
from bmc import BMC
from member import Member
from utils import Log, load_env


class TestBMC(unittest.TestCase):
    def test_get_active_members(self):
        bmc_client = BMC(os.environ['BMC_BASE_URI'],
                         os.environ['BMC_ACCESS_TOKEN'])
        members = bmc_client.get_active_members()
        for member in members:
            Log.info(member.NAME)
            Log.info(member.EMAIL)
        self.assertGreater(len(members), 0, "Should be greater than 0")

    def test_member(self):
        amember = Member("nombre", "email")
        Log.info("---")
        Log.info(amember)


if __name__ == '__main__':
    load_env("../../bmc_prod.env")
    unittest.main()
