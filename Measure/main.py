if __name__ == "__main__":
    import sys
    from parent import Parent


    if len(sys.argv) != 3:
        print("Usage: python3.x main.py [which_work] [with_freeze]")
        sys.exit(1)

    path = f'/home/Results/{sys.argv[1]}.csv'
    w_freeze = int(sys.argv[2]) != 0

    p = Parent(output=path, do_freeze=w_freeze)

    if sys.argv[1] == 'reduction':
        p.do_reduce(n=100000)
    else:
        print("Unknown work")

