#!/usr/bin/env python3


def cli():
    import argparse
    parser = argparse.ArgumentParser(description="Read file line by line")
    parser.add_argument('file', help="File name")
    parser.add_argument('--fs', help="Field separator", default=",")
    parser.add_argument('--cols', help="Columns")
    parser.add_argument('--cmd', action='append', help="Command")
    parser.add_argument('-f', '--file-script', help="File script")
    parser.add_argument('-q','--no-print-out', help="No Print out, silent.", action="store_true")

    args = parser.parse_args()
    return args


def read_line(file, fs, cols):
    if cols is None:
        with open(file, 'r') as f:
            for line in f:
                yield line.strip().split(fs)
    else:
        with open(file, 'r') as f:
            for line in f:
                line = line.strip().split(fs)
                yield [line[i] for i in cols]


def new_user_fn(cmd, g):
    def func(*args, g=g):
        g = g
        (i, line) = args[0]
        exec(cmd)
        return i, line
    return func


def main():
    args = cli()
    print(f"{args = }")
    file = args.file
    print(f"{file = }")

    fs = args.fs
    cmd_list = args.cmd
    no_print_out = args.no_print_out
    print(cmd_list)

    file_script = args.file_script
    if file_script is not None:
        with open(file_script, 'r') as f:
            cmd_list = [f.read()]

    cols = args.cols
    if cols is not None:
        cols = list(map(int, cols.split(",")))


    # final output
    lines = read_line(file, fs, cols)
    lines = enumerate(lines)

    g = {}
    if cmd_list is not None:
        for cmd in cmd_list:
            lines = map(new_user_fn(cmd, g), lines)

    for (i, line) in lines:
        out = line
        if not no_print_out:
            print(i, out)


if __name__ == "__main__":
    main()
