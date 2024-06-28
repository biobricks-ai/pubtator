import pandas as pd
import pyarrow as pa
from pyarrow.csv import open_csv, ParseOptions, ReadOptions
from pyarrow.parquet import write_table
from pathlib import Path

raw_dir = Path("raw")
brick_dir = Path("brick")

biocxml_out = brick_dir / "BioCXML"


def read_csv(filename):
    return open_csv(
        filename,
        parse_options=ParseOptions(
            delimiter="\t",
            invalid_row_handler=lambda _: "skip",
            newlines_in_values=True,
        ),
        read_options=ReadOptions(
            block_size=1024 * 1024 * 1024
        ),  # can't go higher than this or it overflows an int32...
        memory_pool=pa.system_memory_pool()
    )


if __name__ == "__main__":

    if not biocxml_out.exists():
        biocxml_out.mkdir(parents=True)

    for f in raw_dir.iterdir():
        if f.is_file() and f.suffix == "":
            try:
                table: pa.Table = read_csv(f).read_all()
                write_table(table, brick_dir / f"{f.name}.parquet")
            except Exception as e:
                print(e)
        elif f.is_dir():
            output = f / "BioCXML"
            for xml in output.iterdir():
                df = pd.read_xml(xml)
                df.to_parquet(brick_dir / f"BioCXML/{f.name}.parquet")
