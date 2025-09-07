"""exported"""

from pathlib import Path
import logging
from dataclasses import dataclass, field
import re
import hashlib
import base64


LOGGER = logging.getLogger(__name__)
MATCHER = re.compile(r'''"data:(?P<mimetype>.+?);base64,(?P<b64data>.+?)"''')


@dataclass
class Exporter:
    """Export data urls from RUNE output"""

    filepath: Path = field()
    placeholder: str = field()

    def process(self) -> None:
        """Process the file, we assume data-urls are always on one line"""
        newpath = self.filepath.with_suffix(".new")
        LOGGER.info("filepath={}, newpath={}".format(self.filepath, newpath))
        outdir = self.filepath.parent
        assets = outdir / "assets"
        if not assets.is_dir():
            assets.mkdir(parents=True, exist_ok=True)
        with newpath.open("wt", encoding="utf-8") as outpntr:
            with self.filepath.open("rt", encoding="utf-8") as inptr:
                for line in inptr:
                    match = MATCHER.search(line)
                    if not match:
                        outpntr.write(line)
                        continue
                    bincontent = base64.b64decode(match.group("b64data"))
                    binhash = hashlib.sha256(bincontent).hexdigest()
                    _mtype, ext = match.group("mimetype").split("/", maxsplit=2)
                    binpath = assets / f"{binhash}.{ext}"
                    if not binpath.is_file():
                        binpath.write_bytes(bincontent)
                        LOGGER.info("Created {}".format(binpath))
                    newline = line.replace(match.group(0), f'"{self.placeholder}/{binpath.name}"')
                    outpntr.write(newline)
        self.filepath.rename(self.filepath.with_suffix(".old"))
        newpath.rename(newpath.with_suffix(".json"))
