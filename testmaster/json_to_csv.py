import argparse
import csv
import io
import glob
import os
import sys

from ndt_e2e_client.client_wrapper import result_decoder

def _parse_results(result_filenames):
    results = {}
    decoder = result_decoder.NdtResultDecoder()
    for filename in result_filenames:
        with open(filename) as result_json:
            results[filename] = decoder.decode(result_json.read())
    return results

def _results_to_csv(results):
    output = io.BytesIO()
    csv_writer = csv.DictWriter(output, fieldnames=['filename', 'total_duration', 'c2s_throughput', 'c2s_duration', 's2c_throughput', 's2c_duration', 'latency', 'error', 'err_list'])
    csv_writer.writeheader()
    for filename, result in results.iteritems():
        err_list = ','.join([x.message for x in result.errors]) if result.errors else ''
        row = {
            'filename': os.path.basename(filename),
            'total_duration': (result.end_time - result.start_time).total_seconds(),
            'c2s_throughput': result.c2s_result.throughput,
            's2c_throughput': result.s2c_result.throughput,
            'latency': result.latency,
            'error': 1 if len(result.errors) > 0 else 0,
            'err_list': err_list,
        }
        if result.c2s_result.end_time and result.c2s_result.start_time:
            row['c2s_duration'] = (result.c2s_result.end_time - result.c2s_result.start_time).total_seconds()
        if result.s2c_result.end_time and result.s2c_result.start_time:
            row['s2c_duration'] = (result.s2c_result.end_time - result.s2c_result.start_time).total_seconds()
        csv_writer.writerow(row)
    return output.getvalue()

def main(args):
    input_files = glob.glob(args.pattern)
    results = _parse_results(input_files)
    print _results_to_csv(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='JSON to CSV converter',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pattern', required=True)
    main(parser.parse_args())
