from concurrent.futures import as_completed, ThreadPoolExecutor
from queue import Full, Queue
import logging
from typing import Dict, List
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field

raw_dir = Path("raw")
brick_dir = Path("brick")

biocxml_in = raw_dir / "output/BioCXML"
biocxml_out = brick_dir / "BioCXML"


@dataclass(frozen=True)
class Pubtator:
    logger: logging.Logger = field(default=logging.getLogger(__name__))
    exec: ThreadPoolExecutor = field(default=ThreadPoolExecutor(max_workers=6))
    xml_queue: Queue = field(default=Queue(maxsize=100))

    def create_out_dir(self) -> Path:
        brick_dir = Path("brick/BioCXML")
        if not brick_dir.exists():
            brick_dir.mkdir(parents=True)
        return brick_dir

    def create_parquet(self, file, df) -> None:
        name = file.with_suffix(".parquet").name
        df.to_parquet(biocxml_out / name)

    def parse_xml(self, xml_file) -> List[Dict]:
        return pd.read_xml(xml_file), xml_file

    def take_from_xml_queue(self):
        fut = self.xml_queue.get(timeout=10.0)
        result, fname = fut.result()
        logging.info(f"creating Parquet from {fname}")
        self.create_parquet(fname, result)

    def config_logger(self):
        logging.basicConfig(
            filename="pubtator.log",
            level=logging.INFO,
            format="%(asctime)s:%(levelname)s:%(message)s",
        )

    def run(self):
        self.config_logger()
        self.create_out_dir()
        futures = [
            self.exec.submit(self.parse_xml, file) for file in biocxml_in.iterdir()
        ]
        for fut in as_completed(futures):
            try:
                self.xml_queue.put(fut, timeout=20.0)
            except Full:
                print("Queue is full and timeout exceeded.")
                continue

            if not self.xml_queue.empty():
                self.take_from_xml_queue()
            


if __name__ == "__main__":
    pubtator = Pubtator()
    pubtator.run()
