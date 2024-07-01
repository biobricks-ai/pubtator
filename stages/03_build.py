import pandas as pd
from pathlib import Path

raw_dir = Path("raw")
brick_dir = Path("brick")

biocxml_in = raw_dir / "output/BioCXML"
biocxml_out = brick_dir / "BioCXML"


if __name__ == "__main__":

    if not biocxml_out.exists():
        biocxml_out.mkdir(parents=True)

    for f in biocxml_in.iterdir():
        with open(f, "rb") as xml:
            df = pd.read_xml(
                xml,
                iterparse={
                    "document": ["id", "infon", "passage", "relation"],
                    "collection": ["source", "date", "key", "infon", "document"],
                    "passage": ["infon", "offset", "relation"],
                    "annotation": ["infon", "location", "text"]
                },
            )
            df.to_parquet(biocxml_out / f"{f.name}.parquet")
