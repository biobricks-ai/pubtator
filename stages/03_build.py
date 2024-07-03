from lxml import etree
import pandas as pd
from pathlib import Path

raw_dir = Path("raw")
brick_dir = Path("brick")

biocxml_in = raw_dir / "output/BioCXML"
biocxml_out = brick_dir / "BioCXML"

parser = etree.XMLParser(huge_tree=True)


def parse_element(element):
    element_dict = {
        element.tag: element.text,
    }
    element_dict["children"] = [parse_element(child) for child in element]
    return element_dict


if __name__ == "__main__":

    if not biocxml_out.exists():
        biocxml_out.mkdir(parents=True)

    for f in biocxml_in.iterdir():
        with open(f, "rb") as xml:
            parsed_elements = []
            for event, element in etree.iterparse(xml, events=("end",)):
                if element.tag == "collection":
                    parsed_elements.append(parse_element(element))
                    # Clear the element from memory
                    element.clear()
                    while element.getprevious() is not None:
                        del element.getparent()[0]
            df = pd.DataFrame.from_records(parsed_elements)
            out_path = Path(f.name)
            df.to_parquet(biocxml_out / out_path.with_suffix(".parquet"))
            print(f"done parsing file: {f.name}")
