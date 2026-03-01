from os import makedirs, path

from lib.topic import normalize_topic
from lib.generation.utils import collect_competitions


__DEFAULT_GIFT_OUTPUT_DIR__ = "./gift"

def generate_gift_files(years: list[int], topic: str, debug: bool = False, output_dir=None):
    if output_dir is None:
        output_dir = __DEFAULT_GIFT_OUTPUT_DIR__

    output_dir = path.abspath(output_dir)
    makedirs(output_dir, exist_ok=True) 
    print(f"Outputting GIFT files to {output_dir}...")


    with open(f"{output_dir}/{normalize_topic(topic)}.gift", "w", encoding="utf-8") as output_file:
        for year in years:
            C = collect_competitions(year, debug)
            for c in C:
                for q in c.questions:
                    if q.topic == topic:
                        gift_str = q.to_GIFT()
                        output_file.write(gift_str)
                        output_file.write("\n\n")