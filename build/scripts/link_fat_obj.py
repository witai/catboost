import argparse
import subprocess
import sys

YA_ARG_PREFIX = '-Ya,'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--obj', required=True)
    parser.add_argument('--lib', required=True)
    parser.add_argument('--arch', required=True)

    groups = {}
    args_list = groups.setdefault('default', [])
    for arg in sys.argv[1:]:
        if arg.startswith(YA_ARG_PREFIX):
            group_name = arg[len(YA_ARG_PREFIX):]
            args_list = groups.setdefault(group_name, [])
        else:
            args_list.append(arg)

    return parser.parse_args(groups['default']), groups


def main():
    args, groups = get_args()

    # Inputs
    auto_input = groups['input']

    # Outputs
    lib_output = args.lib
    obj_output = args.obj

    # Dependencies
    global_srcs = groups['global_srcs']
    peers = groups['peers']

    # Settings
    arch = args.arch

    # Tools
    linker = groups['linker']
    archiver = groups['archiver']

    if arch in ['DARWIN', 'IOS']:
        load_all = '-Wl,-all_load'
    else:
        load_all = '-Wl,-whole-archive'

    do_link = linker + ['-o', obj_output, '-Wl,-r', '-nodefaultlibs', '-nostartfiles', load_all] + global_srcs + auto_input
    do_archive = archiver + [lib_output] + peers

    def call(c):
        print >> sys.stderr, ' '.join(c)
        proc = subprocess.Popen(c, shell=False, stderr=sys.stderr, stdout=sys.stdout)
        proc.communicate()
        return proc.returncode

    link_res = call(do_link)
    if link_res:
        sys.exit(link_res)

    sys.exit(call(do_archive))


if __name__ == '__main__':
    main()
