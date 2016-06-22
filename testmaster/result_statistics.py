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

import collections

import aggregate
import result_metrics

# Create a named tuple to store the Aggregate values for each NDT metric we're
# tracking.
ResultStatistics = collections.namedtuple(
    'ResultStatistics', ['total_duration', 'c2s_duration', 's2c_duration',
                         'c2s_throughput', 's2c_throughput', 'latency'])


def calculate_statistics(results):
    """Calculates aggregate statistics for a set of NDT results.

    Calculates aggregate statistics (e.g. mean, median, std dev) for each
    relevant NDT metric (e.g. total test duration, s2c throughput).

    Args:
        results: A list of NdtResult instances for which to calculate aggregate
            statistics.

    Returns:
        A ResultStatistics instance that contains aggregate statistics for each
        NDT metric.
    """
    total_duration = aggregate.aggregate(map(result_metrics.total_duration,
                                             results))
    c2s_duration = aggregate.aggregate(map(result_metrics.c2s_duration,
                                           results))
    s2c_duration = aggregate.aggregate(map(result_metrics.s2c_duration,
                                           results))
    c2s_throughput = aggregate.aggregate(map(
        lambda result: result.c2s_result.throughput, results))
    s2c_throughput = aggregate.aggregate(map(
        lambda result: result.s2c_result.throughput, results))
    latency = aggregate.aggregate(map(lambda result: result.latency, results))
    return ResultStatistics(total_duration, c2s_duration, s2c_duration,
                            c2s_throughput, s2c_throughput, latency)
