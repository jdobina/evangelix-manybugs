import argparse
import csv
import json
import os
import re
import sys

PROGRAMS = ('gmp', 'gzip', 'libtiff', 'php', 'wireshark')
TOOLS = ('angelix', 'evangelix')
FIELDNAMES = (
    'program',
    'version',
    'angelix_experiment',
    'angelix_repair',
    'angelix_repair_partial',
    'angelix_repair_timeout',
    'angelix_repair_transforms',
    'angelix_repair_time',
    'evangelix_experiment',
    'evangelix_repair',
    'evangelix_repair_partial',
    'evangelix_repair_timeout',
    'evangelix_repair_transforms',
    'evangelix_repair_time',
)

def parse_angelix_log(angelix_log):
    info = dict.fromkeys(
            ['repaired',
             'repair_partial',
             'repair_time',
             'repair_transforms',
             'repair_timeout'])

    patch_gen_regex = re.compile(r'''^INFO\s+repair\s+
                                     (?P<patch>partial\s+patch|patch)\s+
                                     successfully\s+generated\s+in\s+
                                     (?P<repair_time>\d+)s
                                     .*$
                                  ''', re.X)
    no_patch_regex = re.compile(r'^.*no patch generated in (?P<repair_time>\d+)s$')
    no_patch_timeout_regex = re.compile(r'^.*failed to generate patch \(timeout\)$')
    apply_transform_regex = re.compile(r'^.*applied (?P<transform>.+) transform$')
    revert_transform_regex = re.compile(r'^.*reverting (?P<transform>.+) transform$')
    patch_sources_regex = re.compile(r'^.*patching sources$')
    partial_fix_regex = re.compile(r'^.*Saving partial fix$')

    info['repair_transforms'] = []
    for line in angelix_log:
        m = patch_gen_regex.match(line)
        if m:
            if m.group('patch') == 'patch':
                info['repaired'] = True
                info['repair_partial'] = False
            elif m.group('patch') == 'partial patch':
                info['repaired'] = False
                info['repair_partial'] = True
            info['repair_time'] = int(m.group('repair_time'))
            info['repair_timeout'] = False
            break

        m = no_patch_regex.match(line)
        if m:
            info['repaired'] = False
            info['repair_partial'] = False
            info['repair_time'] = int(m.group('repair_time'))
            info['repair_timeout'] = False
            break

        m = no_patch_timeout_regex.match(line)
        if m:
            info['repaired'] = False
            info['repair_partial'] = False
            info['repair_timeout'] = True
            break

        m = partial_fix_regex.match(line)
        if m:
            info['repair_transforms'].append('partial fix')
            continue

        m = patch_sources_regex.match(line)
        if m:
            info['repair_transforms'].append('patch sources')
            continue

        m = apply_transform_regex.match(line)
        if m:
            info['repair_transforms'].append('+' + m.group('transform'))
            continue

        m = revert_transform_regex.match(line)
        if m:
            info['repair_transforms'].append('-' + m.group('transform'))
            continue

    return info

def get_defect_results(config):
    results = []

    with open('options.json') as f:
        options = json.load(f)

    for program in sorted(config['programs']):
        versions = sorted(options[program])
        for version in versions:
            result = dict.fromkeys(FIELDNAMES)

            result['program'] = program
            result['version'] = version

            for tool in TOOLS:
                defect_dir = os.path.join('results',
                                          tool,
                                          program + '-' + version)

                exp_ok_path = os.path.join(defect_dir, tool + '_exp_ok')
                exp_fail_path = os.path.join(defect_dir, tool + '_exp_fail')
                if os.path.exists(exp_ok_path):
                    result[tool + '_experiment'] = 'ok'
                elif os.path.exists(exp_fail_path):
                    result[tool + '_experiment'] = 'fail'
                    continue
                else:
                    result[tool + '_experiment'] = 'none'
                    continue

                iter_dir = os.path.join(defect_dir, '1')

                angelix_log = os.path.join(iter_dir, '.angelix', 'angelix.log')
                with open(angelix_log) as f:
                    info = parse_angelix_log(f)

                result[tool + '_repair'] = info['repaired']
                result[tool + '_repair_partial'] = info['repair_partial']
                result[tool + '_repair_transforms'] = "->".join(info['repair_transforms'])
                result[tool + '_repair_time'] = info['repair_time']
                result[tool + '_repair_timeout'] = info['repair_timeout']

            results.append(result)

    return results

def dump_csv(defect_results):
    csv_writer = csv.DictWriter(sys.stdout, fieldnames=FIELDNAMES)
    csv_writer.writeheader()
    csv_writer.writerows(defect_results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generate experiment report')
    parser.add_argument('-p', '--programs', nargs='+',
                        choices=PROGRAMS,
                        default=PROGRAMS,
                        help='programs to generate report')
    args = parser.parse_args()

    config = {}
    config['programs'] = args.programs

    defect_results = get_defect_results(config)
    dump_csv(defect_results)
