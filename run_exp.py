import argparse
import json
import subprocess
import time

PROGRAMS = ('gmp', 'gzip', 'libtiff', 'php', 'wireshark')

def run_exp(config):
    run_defect_exp = './run_defect_exp'
    run_defect_exp_opt = []
    if config['force']:
        run_defect_exp_opt.append('-f')
    if config['delay']:
        run_defect_exp_opt.append('-d {}'.format(config['delay']))
    if config['iterations']:
        run_defect_exp_opt.append('-i {}'.format(config['iterations']))

    with open('options.json') as f:
        options = json.load(f)

    for program in sorted(config['programs']):
        versions = sorted(options[program])
        num_defects = len(versions)
        i = 0
        for version in versions:
            i += 1
            print(('running defect experiment [{}/{}]'
                   '\nprogram: {}'
                   '\nversion: {}'
                  ).format(i, num_defects, program, version))
            start = time.time()
            retcode = subprocess.call(([run_defect_exp]
                                       + run_defect_exp_opt
                                       + [config['tool'],
                                          program,
                                          version]),
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
            end = time.time()
            if retcode == 0:
                print(('defect experiment finished in {}s'
                      ).format(int(end - start)))
            else:
                print(('defect experiment failed with retcode: {}'
                      ).format(retcode))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run repair experiment')
    parser.add_argument('tool', choices=('angelix', 'evangelix'),
                        help='tool to use for repair')
    parser.add_argument('-p', '--programs', nargs='+',
                        choices=PROGRAMS,
                        default=PROGRAMS,
                        help='programs to repair')
    parser.add_argument('-i', '--iterations', type=int, default=1,
                        help='number of repair iterations for each defect')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force experiment on a defect')
    parser.add_argument('-d', '--delay', type=int, default=0,
                        help='add n seconds delay before each iteration')
    args = parser.parse_args()

    config = {}
    config['tool'] = args.tool
    config['programs'] = args.programs
    config['iterations'] = args.iterations
    config['force'] = args.force
    config['delay'] = args.delay

    run_exp(config)
