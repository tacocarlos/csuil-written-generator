from lib.topic import ContestLevel

import json
from os import path, makedirs
from typing import get_args


from .topic import Topic
class Question:
    text: str
    code: list[str]
    num: int
    options: list[str]
    competition: "Competition"
    topic: Topic
    correct_idx: int

    def __init__(
        self,
        t: str,
        c: list[str],
        n: int,
        o: list[str],
        comp: "Competition",
        topic: Topic,
        c_idx: int
    ):
        self.text = t
        self.code = c
        self.num = n
        self.options = o
        self.competition = comp
        self.topic = topic
        self.correct_idx = c_idx

    def get_question_id(self) -> str:
        return f"{self.competition.year}{self.competition.get_letter()}{self.num}"

    def to_latex(self) -> str:
        if self.code is not None and len(self.code) > 0:
            return self.__code_latex__()
        return self.__latex__()
    
    def __create_choices__(self):        
        choices = []
        for i, o in enumerate(self.options):
            question_text = ""
            if i == self.correct_idx:
                question_text = f"\\CorrectChoice{{{o}}}"
            else:
                question_text = f"\\choice {o}"
            choices.append(question_text)
        return choices

    def __latex__(self):
        choices = self.__create_choices__()
        return f"""
\\begin{{questionc}}
    \\begin{{qtext}}{{{self.get_question_id()}}}
{self.text}
    \\end{{qtext}}
    \\begin{{qchoices}}
        {"\n".join(choices)}
    \\end{{qchoices}}
\\end{{questionc}}
"""

    def __code_latex__(self):
        choices = self.__create_choices__()
        return f"""
\\begin{{questionc}}
    \\begin{{qtext}}{{{self.get_question_id()}}}
{self.text}
    \\end{{qtext}}
    \\begin{{minted}}{{java}}
{"\n".join(self.code)}
    \\end{{minted}}
    \\begin{{qchoices}}
        {"\n".join(choices)}
    \\end{{qchoices}}
\\end{{questionc}}
"""

    def __str__(self) -> str:
        return f"[{self.num}] {self.text}\n\t{"\t".join(self.options)}"

    def get_path_strand(self) -> str:
        return f'{self.topic.lower().replace(" ", "_")}/'

class Competition:
    level: ContestLevel
    year: int
    questions: list[Question]

    def __init__(self, level: ContestLevel, year: int):
        self.level = level
        self.year = year
        self.questions = []

    def __str__(self) -> str:
        representation = f"{self.year}{self.level}"
        for q in self.questions:
            representation += "\n\t" + str(q)
        return representation

    def add_question(self, q: Question):
        self.questions.append(q)

    def get_letter(self):
        if self.level == "invA":
            return "A"
        elif self.level == "invB":
            return "B"
        elif self.level == "District":
            return "D"
        elif self.level == "Region":
            return "R"
        elif self.level == "State":
            return "S"

    def from_file(year: int, level: ContestLevel, file_path: str) -> "Competition":
        C = Competition(level, year)
        values = None
        with open(file_path) as file:
            values = json.load(file)
        if values is None:
            raise Exception("failure!")

        # print(json.dumps(values, indent=2))
        for v in values:
            qn = v["question_number"]
            text = v["question_text"]
            code = str(v["code_snippet"])
            correct_text = v["correct"]
            options_raw = v["options"]
            correct_idx = -1
            options = []
            for i, op in enumerate(options_raw):
                op_text = op.replace("%^%", "\\\\").replace("[", "\\[").replace("]", "\\]")
                options.append(op_text)
                if op == correct_text:
                    correct_idx = i

            code_parts = code.split("%^%")
            topic = v["topic"]

            # print(f"Read the following data:\n\ttext{{{text}}}\n\t{{{code_parts}}}\n\t{{{"\n".join(options)}}}")
            Q = Question(text, code_parts, qn, options, C, topic, correct_idx)
            if topic != Q.topic:
                print(f"MISMATCH: {qn} {text}")
            C.add_question(Q)

        return C
    
    def write_latex(self, base_output_path="./out/"):
        num_written = 0
        for q in self.questions:
            output_dir = path.join(base_output_path, q.get_path_strand())
            makedirs(output_dir, exist_ok=True)
            output_path = path.join(output_dir, f"{self.year}{self.level}.tex")
            with open(output_path, "w") as file:
                file.write(q.to_latex())
            num_written += 1

def collect_competitions(year, debug=False):
    C = []
    for level in get_args(ContestLevel):
        fp = f"./data/{year}/{level.lower()}.json"
        if path.exists(fp) is False:
            print(f"Unable to find [{fp}] !")
            continue
        print(f"Reading data from {year} {level}...")
        c = Competition.from_file(year, level, fp)
        if debug:
            print(f"{c.year} {c.level}")
            for q in c.questions:
                print(q)
        C.append(c)
    return C

def generate_latex(year: int, debug=False):
    C = collect_competitions(year, debug)
    for c in C:
        c.write_latex()