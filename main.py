import argparse
import logging
import random
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_argparse():
    """
    Sets up the argparse for the command-line interface.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="Rounds numerical data to a specified precision for data masking.")
    parser.add_argument("input_data", nargs="?", type=str, help="Numerical data to round (single number or comma-separated list).  If not provided, will read from stdin.")
    parser.add_argument("-p", "--precision", type=int, default=0, help="Number of decimal places to round to (default: 0).")
    parser.add_argument("-r", "--randomize", action="store_true", help="Add a small random value before rounding.")
    parser.add_argument("-m", "--multiplier", type=float, default=1.0, help="Multiplier to apply to the number before rounding (default: 1.0).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    return parser


def round_and_mask(data, precision, randomize, multiplier):
    """
    Rounds a single numerical value to the specified precision.

    Args:
        data (float): The numerical data to round.
        precision (int): The number of decimal places to round to.
        randomize (bool): Whether to add a small random value before rounding.
        multiplier (float): Multiplier to apply before rounding.

    Returns:
        float: The rounded data.
    """
    try:
        data = float(data)  # Convert to float to handle integers and decimals
    except ValueError:
        logging.error(f"Invalid input: '{data}' is not a valid number.")
        return None

    try:
        data *= multiplier
    except TypeError:
        logging.error(f"Invalid multiplier: '{multiplier}' is not a number.")
        return None

    if randomize:
        data += random.uniform(-0.5 / (10**precision), 0.5 / (10**precision))  # Add a small random value

    try:
        return round(data, precision)
    except TypeError:
        logging.error(f"Precision must be an integer.")
        return None


def main():
    """
    Main function to parse arguments, read input, and round data.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose logging enabled.")

    input_data = args.input_data

    if not input_data:  # Read from stdin if no data provided as argument
        try:
            input_data = sys.stdin.read().strip()
            logging.debug("Reading input from stdin.")
        except Exception as e:
            logging.error(f"Error reading from stdin: {e}")
            sys.exit(1)

    if not input_data:
        logging.error("No input data provided.")
        parser.print_help()
        sys.exit(1)

    try:
        # Attempt to split the input string into individual numbers by comma
        numbers = [s.strip() for s in input_data.split(",")]
    except AttributeError:
        # Handles the case when data is already in list form
        logging.error("Invalid input format. Expected comma-separated values or a single number.")
        sys.exit(1)
    
    results = []
    for number_str in numbers:
        result = round_and_mask(number_str, args.precision, args.randomize, args.multiplier)
        if result is not None:
            results.append(str(result))

    if results:
        print(",".join(results))


if __name__ == "__main__":
    # Example Usage (not part of the final script, but illustrates how to use it)
    # 1. Round a single number to 2 decimal places: python main.py 123.456 -p 2
    # 2. Round multiple numbers separated by commas: python main.py 123.456,789.012 -p 1
    # 3. Round and randomize: python main.py 123.456 -p 2 -r
    # 4. Round with multiplier: python main.py 10 -p 0 -m 2.5
    # 5. Read from stdin: echo "456.789,987.654" | python main.py -p 0

    main()