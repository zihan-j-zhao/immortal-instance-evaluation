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
        '-v',
        '--verbose',
        action='store_true',
        help='collect and print more statistics'
    )
    parser.add_argument(
        '--enable-object-tracker',
        action='store_true',
        help='collect info about gc-tracked objects'
    )
    # ==================================== #

    args = parser.parse_args()

    print('----start----')

    invoke(
        args.function,

        # optional flags
        verbose=args.verbose,
        enable_object_tracker=args.enable_object_tracker,
    )

    print('----end----')
