# Copyright 2016 Measurement Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import datetime
import unittest

import pytz

from testmaster import result_metrics
from testmaster.ndt_e2e_clientworker.client_wrapper import results


class ResultMetricsTest(unittest.TestCase):

    def test_total_duration_is_correct_for_completed_result(self):
        result = results.NdtResult(
            start_time=datetime.datetime(2016, 6, 8, 12, 0, 0, 0, pytz.utc),
            end_time=datetime.datetime(2016, 6, 8, 12, 0, 35, 700000, pytz.utc))
        self.assertAlmostEqual(35.7,
                               result_metrics.total_duration(result),
                               places=1)

    def test_total_duration_is_None_on_incomplete_result(self):
        result = results.NdtResult(
            start_time=datetime.datetime(2016, 6, 8, 12, 0, 0, 0, pytz.utc))
        self.assertIsNone(result_metrics.total_duration(result))

    def test_c2s_duration_is_correct_for_completed_c2s_test(self):
        result = results.NdtResult(c2s_result=results.NdtSingleTestResult(
            start_time=datetime.datetime(2016, 6, 8, 12, 0, 0, 0, pytz.utc),
            end_time=datetime.datetime(2016, 6, 8, 12, 0, 11, 927345,
                                       pytz.utc)))
        self.assertAlmostEqual(11.9,
                               result_metrics.c2s_duration(result),
                               places=1)

    def test_c2s_duration_is_None_for_incomplete_c2s_test(self):
        result = results.NdtResult(c2s_result=results.NdtSingleTestResult(
            start_time=datetime.datetime(2016, 6, 8, 12, 0, 0, 0, pytz.utc)))
        self.assertIsNone(result_metrics.c2s_duration(result))

    def test_s2c_duration_is_correct_for_completed_s2c_test(self):
        result = results.NdtResult(s2c_result=results.NdtSingleTestResult(
            start_time=datetime.datetime(2016, 6, 8, 12, 0, 0, 0, pytz.utc),
            end_time=datetime.datetime(2016, 6, 8, 12, 0, 11, 927345,
                                       pytz.utc)))
        self.assertAlmostEqual(11.9,
                               result_metrics.s2c_duration(result),
                               places=1)

    def test_s2c_duration_is_None_for_incomplete_s2c_test(self):
        result = results.NdtResult(s2c_result=results.NdtSingleTestResult(
            start_time=datetime.datetime(2016, 6, 8, 12, 0, 0, 0, pytz.utc)))
        self.assertIsNone(result_metrics.s2c_duration(result))
