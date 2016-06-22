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

import mock
import pytz

from testmaster import result_statistics
from testmaster.ndt_e2e_clientworker.client_wrapper import results

# Mock NDT results from which to calculate aggregate statistics.
RESULTS_A = results.NdtResult(
    start_time=datetime.datetime(2016, 1, 1, 0, 0, 0, 0, pytz.utc),
    end_time=datetime.datetime(2016, 1, 1, 0, 0, 23, 0, pytz.utc),
    c2s_result=results.NdtSingleTestResult(
        start_time=datetime.datetime(2016, 1, 1, 0, 0, 1, 0, pytz.utc),
        end_time=datetime.datetime(2016, 1, 1, 0, 0, 11, 0, pytz.utc),
        throughput=1.0),
    s2c_result=results.NdtSingleTestResult(
        start_time=datetime.datetime(2016, 1, 1, 0, 0, 12, 0, pytz.utc),
        end_time=datetime.datetime(2016, 1, 1, 0, 0, 22, 500000, pytz.utc),
        throughput=5.0),
    latency=10.0)
RESULTS_B = results.NdtResult(
    start_time=datetime.datetime(2016, 1, 1, 0, 0, 0, 0, pytz.utc),
    end_time=datetime.datetime(2016, 1, 1, 0, 0, 25, 0, pytz.utc),
    c2s_result=results.NdtSingleTestResult(
        start_time=datetime.datetime(2016, 1, 1, 0, 0, 1, 0, pytz.utc),
        end_time=datetime.datetime(2016, 1, 1, 0, 0, 13, 0, pytz.utc),
        throughput=97.6),
    s2c_result=results.NdtSingleTestResult(
        start_time=datetime.datetime(2016, 1, 1, 0, 0, 13, 0, pytz.utc),
        end_time=datetime.datetime(2016, 1, 1, 0, 0, 23, 0, pytz.utc),
        throughput=108.2),
    latency=3.0)
RESULTS_C = results.NdtResult(
    start_time=datetime.datetime(2016, 1, 1, 0, 0, 0, 0, pytz.utc),
    end_time=datetime.datetime(2016, 1, 1, 0, 0, 26, 0, pytz.utc),
    c2s_result=results.NdtSingleTestResult(
        start_time=datetime.datetime(2016, 1, 1, 0, 0, 1, 0, pytz.utc),
        end_time=datetime.datetime(2016, 1, 1, 0, 0, 12, 0, pytz.utc),
        throughput=55.3),
    s2c_result=results.NdtSingleTestResult(
        start_time=datetime.datetime(2016, 1, 1, 0, 0, 13, 0, pytz.utc),
        end_time=datetime.datetime(2016, 1, 1, 0, 0, 24, 500000, pytz.utc),
        throughput=47.6),
    latency=103.5)


class CalculateStatisticsTest(unittest.TestCase):

    def setUp(self):
        aggregate_patcher = mock.patch.object(result_statistics.aggregate,
                                              'aggregate')
        self.addCleanup(aggregate_patcher.stop)
        aggregate_patcher.start()
        self.mock_aggregate = result_statistics.aggregate.aggregate
        # Mock out the return values of the calls to aggregate.aggregate.
        # Caveat: Defining the side effect in this way is FLAKY in that we
        # assume a particular ordering of calls to aggregate.aggregate, even
        # though this is an implementation detail of calculate_statistics. We
        # are accepting this flakiness to avoid the added complexity of
        # creating a mock aggregate function that is order-agnostic.
        self.mock_aggregate.side_effect = [
            'mock total duration', 'mock c2s duration', 'mock s2c duration',
            'mock c2s throughput', 'mock s2c throughput', 'mock latency'
        ]

    def assertMockAggregateHasCalls(self, total_duration, c2s_duration,
                                    s2c_duration, c2s_throughput,
                                    s2c_throughput, latency):
        """Verify that the mocked out aggregate function was called correctly.

        Verify that the calculate_statistics calls the aggregate.aggregate
        function received the expected values to aggregate for each NDT metric.
        """
        self.mock_aggregate.assert_has_calls(
            [
                mock.call(total_duration),
                mock.call(c2s_duration),
                mock.call(s2c_duration),
                mock.call(c2s_throughput),
                mock.call(s2c_throughput),
                mock.call(latency),
            ],
            any_order=True)

    def test_calculate_aggregates_for_single_result(self):
        statistics = result_statistics.calculate_statistics([RESULTS_A])
        self.assertMockAggregateHasCalls(total_duration=[23.0],
                                         c2s_duration=[10.0],
                                         s2c_duration=[10.5],
                                         c2s_throughput=[1.0],
                                         s2c_throughput=[5.0],
                                         latency=[10.0])
        self.assertEqual('mock total duration', statistics.total_duration)
        self.assertEqual('mock c2s duration', statistics.c2s_duration)
        self.assertEqual('mock s2c duration', statistics.s2c_duration)
        self.assertEqual('mock c2s throughput', statistics.c2s_throughput)
        self.assertEqual('mock s2c throughput', statistics.s2c_throughput)
        self.assertEqual('mock latency', statistics.latency)

    def test_calculate_aggregates_for_three_results(self):
        statistics = result_statistics.calculate_statistics(
            [RESULTS_A, RESULTS_B, RESULTS_C])
        self.assertMockAggregateHasCalls(total_duration=[23.0, 25.0, 26.0],
                                         c2s_duration=[10.0, 12.0, 11.0],
                                         s2c_duration=[10.5, 10.0, 11.5],
                                         c2s_throughput=[1.0, 97.6, 55.3],
                                         s2c_throughput=[5.0, 108.2, 47.6],
                                         latency=[10.0, 3.0, 103.5])
        self.assertEqual('mock total duration', statistics.total_duration)
        self.assertEqual('mock c2s duration', statistics.c2s_duration)
        self.assertEqual('mock s2c duration', statistics.s2c_duration)
        self.assertEqual('mock c2s throughput', statistics.c2s_throughput)
        self.assertEqual('mock s2c throughput', statistics.s2c_throughput)
        self.assertEqual('mock latency', statistics.latency)
