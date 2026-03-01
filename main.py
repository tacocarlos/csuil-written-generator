from os import listdir, path, makedirs
from subprocess import run

# from gooey import Gooey, GooeyParser
from GooeyEx import Gooey, GooeyParser

from lib.topic import TOPIC_LIST
from lib.generation.utils import find_available_years
from lib.generation.tex.tex import generate_latex_files, generate_packet_tex
from lib.generation.gift import generate_gift_files

@Gooey(show_preview_warning=False, program_name="CS UIL Written Packet Generator")
def main():

    years = find_available_years()
    print("Available years:", years)

    parser = GooeyParser(description="CS UIL Written Packet Generator")

    exec_opt_group = parser.add_argument_group("Program Execution Options", "")
    exec_opt_group.add_argument(
        "--debug", action="store_true", help="Print debug information to console"
    )

    flags_group = parser.add_argument_group("Tooglable Settings", "")
    flags_group.add_argument(
        "--pagebreak", action="store_true", help="Insert page breaks between questions"
    )
    flags_group.add_argument(
        "--key", action="store_true", help="Additionally generate the key"
    )

    flags_group.add_argument(
        "--open",
        action="store_true",
        default=True,
        help="Open file(s) in default application (Linux only)",
    )

    selection_group = parser.add_argument_group("Output Data Selection", "")

    selection_group.add_argument(
        "--years",
        nargs="+",
        widget="Listbox",
        type=int,
        choices=years,
        help="The years to generate packets for",
        gooey_options={
            "background_color": "#ffffff",
            "height": len(years) * 25 + 10,
        },
    )

    selection_group.add_argument(
        "--topic",
        choices=TOPIC_LIST,
        help="Question topic",
    )
    
    selection_group.add_argument("--gift", action="store_true", help="Generate GIFT files instead of LaTeX")

    args = parser.parse_args()
    print(args)

    if(args.gift):
        print("Generating GIFT files...")
        generate_gift_files(args.years, args.topic, debug=args.debug)
        return

    generate_latex_files(args.years, debug=args.debug)
    generate_packet_tex(
        args.topic,
        years=args.years,
        print_key=False,
        debug=args.debug,
        pagebreak=args.pagebreak,
        open_files=args.open,
    )

    if args.key is True:
        generate_packet_tex(
            args.topic,
            years=args.years,
            print_key=True,
            debug=args.debug,
            pagebreak=args.pagebreak,
            open_files=args.open,
        )


if __name__ == "__main__":
    # generate_latex_files()
    main()
