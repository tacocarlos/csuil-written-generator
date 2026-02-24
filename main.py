from lib.competition import generate_latex
from lib.topic import TOPIC_LIST

from gooey import Gooey, GooeyParser

from os import listdir, path


def generate_latex_files(years, debug=False):
    for year in years:
        generate_latex(year, debug=debug)
        print("=" * 30)

def find_available_years(search_path="data") -> list[int]:
    dirs = [d for d in listdir(search_path) if path.isdir(path.join(search_path, d))]
    years = []
    for d in dirs:
        if d.isdigit():
            years.append(int(d))
    return years


# Rather than use \include to pull in the template parts, I instead copy them directly into the resulting TeX
# as the latex-components dir shouldn't exist in the actual latex project, and is exclusively a logical thing.
def generate_packet_tex(topic: str, years: list[int],print_key=False, debug=False, pagebreak=False) -> None:
    print(f"Generating {topic} packet...")
    with open(f"{topic.lower().replace(' ', '_')}-problem-packet.tex", "w") as output_tex:
        if print_key:
            output_tex.write("\\documentclass[answers, 12pt]{{exam}}\n")
        else:
            output_tex.write("\\documentclass[12pt]{{exam}}\n")

        with open("./latex-components/preamble.tex") as preamble:
            output_tex.write(preamble.read())
        output_tex.write("\n")
        if pagebreak:
            output_tex.write("\\toggletrue{separatePages}")
        else:
            output_tex.write("\\togglefalse{separatePages}")
        output_tex.write("\n")

        years_str = ", ".join(str(year) for year in years)
        output_tex.write(f"\\def\\years{{{years_str}}}\n")
        output_tex.write(f"\\def\\topic{{{topic}}}\n")
        output_tex.write("\\begin{document}\n")

        with open("./latex-components/title.tex") as title:
            output_tex.write(title.read())
        output_tex.write("\n")

        # TODO: instead of having latex do the work, maybe generate it ourselves so the compilation on Overleaf goes faster?
        with open("./latex-components/import-generator.tex") as import_generator:
            output_tex.write(import_generator.read())
        output_tex.write("\n")


        output_tex.write("\\end{document}")

@Gooey
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
    flags_group.add_argument("--key", action="store_true", help="Generate with answer key")

    selection_group = parser.add_argument_group("Output Data Selection", "")

    selection_group.add_argument(
        "--years", nargs="+", widget="Listbox", type=int, choices=years, help="The years to generate packets for",
        gooey_options={
            "background_color": "#ffffff",
            "height": len(years) * 25 + 10,
        }
    )

    selection_group.add_argument(
        "--topic",
        choices=TOPIC_LIST,
        help="Question topic",
    )

    args = parser.parse_args()
    print(args)
    generate_latex_files(args.years, debug=args.debug)
    generate_packet_tex(args.topic, years=args.years, print_key=args.key, debug=args.debug, pagebreak=args.pagebreak)


if __name__ == "__main__":
    # generate_latex_files()
    main()
