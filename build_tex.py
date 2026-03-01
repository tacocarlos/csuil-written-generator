from subprocess import run
from argparse import ArgumentParser

from lib.generation.tex.build import __DEFAULT_AUX_DIR__, __DEFAULT_OUT_DIR__, build_latex

def launch_file(file_path: str):
    return run(["xdg-open", file_path])


def main():
    parser = ArgumentParser()
    parser.add_argument("tex_path", type=str, help="Path to the tex file to build")
    parser.add_argument(
        "--out_dir", type=str, default=__DEFAULT_OUT_DIR__, help="output directory"
    )
    parser.add_argument(
        "--aux-dir", type=str, default=__DEFAULT_AUX_DIR__, help="aux directory"
    )

    args = parser.parse_args()

    build_latex(args.tex_path, args.out_dir, args.aux_dir)


if __name__ == "__main__":
    main()
