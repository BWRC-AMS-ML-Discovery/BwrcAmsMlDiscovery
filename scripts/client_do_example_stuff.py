from example_client import (
    do_example_stuff,
    example_client_start,
)


def main():
    example_client_start()

    try:
        do_example_stuff()
    except RecursionError:
        print("RecursionError: needs renaming to avoid the same function name")
        pass


if __name__ == "__main__":
    main()
