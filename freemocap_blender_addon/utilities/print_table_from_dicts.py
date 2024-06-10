from typing import List, Dict, Any

def convert_to_string(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)

def print_table(data: List[Dict[str, Any]]) -> None:
    """
    Prints a list of dictionaries as a formatted table.

    Parameters
    ----------
    data : List[Dict[str, str]]
        A list of dictionaries containing the data to print.

    Example
    -------
    >>> data = [
    ...     {"Name": "Alice", "Age": "24", "City": "New York"},
    ...     {"Name": "Bob", "Age": "30", "City": "Los Angeles"},
    ...     {"Name": "Charlie", "Age": "22", "City": "Chicago"}
    ... ]
    >>> print_table(data)
    +---------+-----+-------------+
    | Name    | Age | City        |
    +---------+-----+-------------+
    | Alice   | 24  | New York    |
    | Bob     | 30  | Los Angeles |
    | Charlie | 22  | Chicago     |
    +---------+-----+-------------+
    """

    if not data:
        print("No data to display")
        return

        # Extracting headers
    headers = list(data[0].keys())

    # Converting all values to strings and truncating floating point precision
    for row in data:
        for header in headers:
            row[header] = convert_to_string(row[header])

    # Calculating maximum width for each column
    col_widths = {header: len(header) for header in headers}
    for row in data:
        for header in headers:
            col_widths[header] = max(col_widths[header], len(row[header]))

    # Creating a format string for each row
    row_format = '| ' + ' | '.join(f'{{:{col_widths[header]}}}' for header in headers) + ' |'
    separator = '+-' + '-+-'.join('-' * col_widths[header] for header in headers) + '-+'

    # Printing the table
    print(separator)
    print(row_format.format(*headers))
    print(separator)
    for row in data:
        print(row_format.format(*[row[header] for header in headers]))
    print(separator)


if __name__ == "__main__":
   # Example usage
    data = [
        {"Name": "Alice", "Age": 24, "City": "New York"},
        {"Name": "Bob", "Age": 30.3, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": "22", "City": "Chicago"}
    ]

    print_table(data)