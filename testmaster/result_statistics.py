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

import numpy

import result_metrics


class AggregateStats(object):

    def __init__(self, minimum, maximum, mean, median, standard_deviation,
                 sample_count):
        self._minimum = minimum
        self._maximum = maximum
        self._mean = mean
        self._median = median
        self._standard_deviation = standard_deviation
        self._sample_count = sample_count

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @property
    def mean(self):
        return self._mean

    @property
    def median(self):
        return self._median

    @property
    def standard_deviation(self):
        return self._standard_deviation

    @property
    def sample_count(self):
        return self._sample_count


def _aggregate_values(values):
    samples = [x for x in values if x is not None]
    return AggregateStats(minimum=min(samples),
                          maximum=max(samples),
                          mean=numpy.mean(samples),
                          median=numpy.median(samples),
                          standard_deviation=numpy.std(samples),
                          sample_count=len(samples))


def calculate_statistics(results):
    statistics = {}
    values = results.values()
    statistics['Total Duration (s)'] = _aggregate_values(map(
        result_metrics.total_duration, values))
    statistics['Upload Duration (s)'] = _aggregate_values(map(
        result_metrics.c2s_duration, values))
    statistics['Download Duration (s)'] = _aggregate_values(map(
        result_metrics.s2c_duration, values))
    statistics['Upload Throughput (Mbps)'] = _aggregate_values(map(
        lambda result: result.c2s_result.throughput, values))
    statistics['Download Throughput (Mbps)'] = _aggregate_values(map(
        lambda result: result.s2c_result.throughput, values))
    statistics['Latency (ms)'] = _aggregate_values(map(
        lambda result: result.latency, values))
    return statistics
