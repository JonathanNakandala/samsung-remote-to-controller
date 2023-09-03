"""
Output to the text console
"""
import sys

from rich.table import Table
from rich.console import Console


def get_user_selection(items: list[dict[str, str]]) -> dict[str, str]:
    """
    Create and display a table for user selection using dictionary keys as headers.
    """
    if not items:
        raise ValueError("The items list is empty.")

    # Get column headers from the keys of the first dictionary
    headers = list(items[0].keys())

    table = Table(show_header=True, header_style="bold magenta")
    for header in headers:
        table.add_column(header, style="magenta")

    for _, item in enumerate(items):
        table.add_row(*[str(item[header]) for header in headers])

    console = Console()
    console.print(table)

    while True:
        try:
            user_input = input(f"Select a number (0-{len(items) - 1}): ")

            match user_input:
                case str(selection) if (sel := int(selection)) in range(len(items)):
                    return items[sel]
                case _:
                    print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit()
