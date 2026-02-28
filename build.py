from subprocess import run

from argparse import ArgumentParser
from os import makedirs, path

__DEFAULT_OUT_DIR__ = "generated"
__DEFAULT_AUX_DIR__ = "generated/aux"


class LatexGenerationResult:
    tex_path: str
    pdf_path: str | None

    def __init__(self, tex, pdf):
        self.tex_path = tex
        self.pdf_path = pdf

    def is_ok(self):
        return self.pdf_path is not None

    def __str__(self):
        return f"{'Good' if self.is_ok() else 'Bad'}: tex={self.tex_path} pdf_path={self.pdf_path}"


def build_latex(tex_path: str, out_dir=None, aux_dir=None):
    if out_dir is None:
        out_dir = __DEFAULT_OUT_DIR__
    if aux_dir is None:
        aux_dir = __DEFAULT_AUX_DIR__

    tex_path = path.abspath(tex_path)
    out_dir = path.abspath(out_dir)
    aux_dir = path.abspath(aux_dir)

    cmd = [
        "pdflatex",
        "-output-directory",
        aux_dir,
        tex_path,
    ]

    makedirs(out_dir, exist_ok=True)
    makedirs(aux_dir, exist_ok=True)

    ret_code = 0
    try:
        cp = run(cmd)
        ret_code = cp.returncode
    except Exception:
        print("Error when generating latex!")
        ret_code = -1

    print("Successfully generate LaTeX.")
    file_name = path.splitext(path.basename(tex_path))[0]
    pdf_path = f"{aux_dir}/{file_name}.pdf"
    dest_path = f"{out_dir}/{file_name}.pdf"
    try:
        print(f"Copying\n\t{pdf_path}to\n\t{dest_path}")
        cp = run(["cp", pdf_path, dest_path])
        ret_code = cp.returncode
    except Exception:
        ret_code = -1

    return LatexGenerationResult(tex_path, dest_path)


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
