import csv
import io
import os

from ndt_e2e_client.client_wrapper import result_decoder

ANSIBLE_OUTDIR = '/tmp/ansible-out'

decoder = result_decoder.NdtResultDecoder()

output = io.BytesIO()
csv_writer = csv.DictWriter(output, fieldnames=['filename', 'total_duration', 'c2s_throughput', 'c2s_duration', 's2c_throughput', 's2c_duration', 'latency', 'errors'])
csv_writer.writeheader()
errors = []
for filename in os.listdir(ANSIBLE_OUTDIR):
    with open(os.path.join(ANSIBLE_OUTDIR, filename)) as result_json:
        result = decoder.decode(result_json.read())
        row = {
            'filename': filename,
            'total_duration': (result.end_time - result.start_time).total_seconds(),
            'c2s_throughput': result.c2s_result.throughput,
            's2c_throughput': result.s2c_result.throughput,
            'latency': result.latency,
            'errors': len(result.errors),
        }
        errors.extend(result.errors)
        if result.c2s_result.end_time and result.c2s_result.start_time:
            row['c2s_duration'] = (result.c2s_result.end_time - result.c2s_result.start_time).total_seconds()
        if result.s2c_result.end_time and result.s2c_result.start_time:
            row['s2c_duration'] = (result.s2c_result.end_time - result.s2c_result.start_time).total_seconds()
        csv_writer.writerow(row)

print output.getvalue()
