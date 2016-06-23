#!/usr/bin/python
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
"""Calculates aggregate statistics from a set of NDT result files.

Given a pattern of files, finds the NDT result files (JSON) or result packages
(zips of JSON) and parses their contents to dump out aggregate statistics on
each each metric.
"""

import argparse
import csv
import glob
import io
import logging

import read_results
import result_statistics


def print_simple(stats):
    print _metric_to_simple_summary('Total Duration (s)', stats.total_duration)
    print _metric_to_simple_summary('Upload Duration (s)', stats.c2s_duration)
    print _metric_to_simple_summary('Download Duration (s)', stats.s2c_duration)
    print _metric_to_simple_summary('Upload Throughput (Mbps)',
                                    stats.c2s_throughput)
    print _metric_to_simple_summary('Download Throughput (Mbps)',
                                    stats.s2c_throughput)
    print _metric_to_simple_summary('Latency (ms)', stats.latency)


def _metric_to_simple_summary(metric_friendly_name, metric_aggregates):
    summary = metric_friendly_name + '\n'
    summary += '    Minimum: %.1f\n' % metric_aggregates.minimum
    summary += '    Maximum: %.1f\n' % metric_aggregates.maximum
    summary += '    Mean:    %.1f\n' % metric_aggregates.mean
    summary += '    Median:  %.1f\n' % metric_aggregates.median
    summary += '    StdDev:  %.3f\n' % metric_aggregates.standard_deviation
    summary += '    Samples: %d\n' % metric_aggregates.sample_count
    return summary


def print_csv(stats):
    output = io.BytesIO()
    # Note: We are duplicating strings from _metric_to_csv_row, but this
    # enforces our desired ordering of fields.
    fields = ['Metric', 'Minimum', 'Maximum', 'Mean', 'Median', 'StdDev',
              'Samples']
    csv_file = csv.DictWriter(output, fieldnames=fields)
    csv_file.writeheader()
    csv_file.writerow(_metric_to_csv_row('Total Duration (s)',
                                         stats.total_duration))
    csv_file.writerow(_metric_to_csv_row('Upload Duration (s)',
                                         stats.c2s_duration))
    csv_file.writerow(_metric_to_csv_row('Download Duration (s)',
                                         stats.s2c_duration))
    csv_file.writerow(_metric_to_csv_row('Upload Throughput (Mbps)',
                                         stats.c2s_throughput))
    csv_file.writerow(_metric_to_csv_row('Download Throughput (Mbps)',
                                         stats.s2c_throughput))
    csv_file.writerow(_metric_to_csv_row('Latency (ms)', stats.latency))
    print output.getvalue()


def _metric_to_csv_row(metric_friendly_name, metric_aggregates):
    return {
        'Metric': metric_friendly_name,
        'Minimum': metric_aggregates.minimum,
        'Maximum': metric_aggregates.maximum,
        'Mean': metric_aggregates.mean,
        'Median': metric_aggregates.median,
        'StdDev': metric_aggregates.standard_deviation,
        'Samples': metric_aggregates.sample_count,
    }


def print_statistics(stats, output_format):
    if output_format == 'simple':
        print_simple(stats)
    elif output_format == 'csv':
        print_csv(stats)
    else:
        raise ValueError('Invalid output format: %s' % output_format)


def main(args):
    matching_files = glob.glob(args.pattern)
    if not matching_files:
        logging.error('No files matched pattern %s', args.pattern)
        return
    results = read_results.parse_files(matching_files)
    stats = result_statistics.calculate_statistics(results.values())
    print_statistics(stats, args.format)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='NDT Result Aggregate Statistic Calculator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pattern',
                        required=True,
                        help='Glob pattern of input files')
    parser.add_argument('--format',
                        choices=('simple', 'csv'),
                        default='simple',
                        help='Output format')
    main(parser.parse_args())
