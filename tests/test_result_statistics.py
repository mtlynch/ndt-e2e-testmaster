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
import collections
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

# Simplified version of the aggregate.Aggregate named tuple that has only a
# total field.
FakeAggregates = collections.namedtuple('FakeAggregates', 'total')


def fake_aggregate(values):
    """Fake implementation of aggregate that just calculates sums.

    Fake implementation of the aggregate.aggregate function that returns a
    simplified.

    Returns:
        An instance of FakeAggregates, populated with the sum total of values.
    """
    return FakeAggregates(total=sum(values))


class CalculateStatisticsTest(unittest.TestCase):

    def setUp(self):
        aggregate_patcher = mock.patch.object(result_statistics.aggregate,
                                              'aggregate')
        self.addCleanup(aggregate_patcher.stop)
        aggregate_patcher.start()
        self.mock_aggregate = result_statistics.aggregate.aggregate
        self.mock_aggregate.side_effect = fake_aggregate

    def test_calculate_statistics_for_single_result(self):
        statistics = result_statistics.calculate_statistics([RESULTS_A])
        self.assertAlmostEqual(23.0, statistics.total_duration.total)
        self.assertAlmostEqual(10.0, statistics.c2s_duration.total)
        self.assertAlmostEqual(10.5, statistics.s2c_duration.total)
        self.assertAlmostEqual(1.0, statistics.c2s_throughput.total)
        self.assertAlmostEqual(5.0, statistics.s2c_throughput.total)
        self.assertAlmostEqual(10.0, statistics.latency.total)

    def test_calculate_statistics_for_three_results(self):
        statistics = result_statistics.calculate_statistics(
            [RESULTS_A, RESULTS_B, RESULTS_C])
        self.assertAlmostEqual(23.0 + 25.0 + 26.0,
                               statistics.total_duration.total)
        self.assertAlmostEqual(10.0 + 12.0 + 11.0,
                               statistics.c2s_duration.total)
        self.assertAlmostEqual(10.5 + 10.0 + 11.5,
                               statistics.s2c_duration.total)
        self.assertAlmostEqual(1.0 + 97.6 + 55.3,
                               statistics.c2s_throughput.total)
        self.assertAlmostEqual(5.0 + 108.2 + 47.6,
                               statistics.s2c_throughput.total)
        self.assertAlmostEqual(10.0 + 3.0 + 103.5, statistics.latency.total)
