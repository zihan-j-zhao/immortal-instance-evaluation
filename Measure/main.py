if __name__ == "__main__":
    import argparse
    from lambdas import invoke

    parser = argparse.ArgumentParser(
        prog="main",
        description="This program measures process statistics for the given task",
        epilog="See more in https://github.com/zihan-j-zhao/immortal-instance-evaluation"
    )

    # ========== ADD POSITIONAL ARGS HERE ========== #
    parser.add_argument(
        'function',
        type=str,
        help='name of the lambda function to invoke'
    )
    # ============================================== #

    # ========== ADD FLAGS HERE ========== #
    parser.add_argument(
        '-f',
        '--freeze',
        action='store_true',
        help='call gc.freeze() before os.fork()'
    )
    parser.add_argument(
        '-c',
        '--collect',
        action='store_true',
        help='call gc.collect() before os.fork()'
    )
    # ==================================== #

    args = parser.parse_args()

    invoke(
        args.function,

        # optional flags
        freeze=args.freeze,
        collect=args.collect,
    )
