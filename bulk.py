import logging
import os
from argparse import ArgumentParser
from tqdm import tqdm as tqdm

import numpy as np
import pandas as pd
import qrcode
import qrcode.constants
import qrcode.image.pil
import qrcode.image.svg

from core import gen_data

log = logging.getLogger("kms_qr")


def main(argv=None):
    parser = ArgumentParser()
    parser.add_argument("-c", "--csv", required=True)
    parser.add_argument("-o", "--output", default=os.path.join("out", "qr_{kms}.svg"))
    parser.add_argument("-v", "--verbose", action="store_true")

    parser.add_argument("--error-correction", default="ERROR_CORRECT_H",
                        choices=[k for k in dir(qrcode.constants) if k.startswith("ERROR_CORRECT")])

    args = parser.parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    out_dir = os.path.dirname(args.output)
    os.makedirs(out_dir, exist_ok=True)

    csv = pd.read_csv(args.csv)
    for index, row in tqdm(csv.iterrows()):
        parameters = {
            "index": index,
            "name": row["Imię"],
            "surname": row["Nazwisko"],
            "kms": row["Nr legitymacji"],
            "email": row["E-mail"],
            # "phone": row["Telefon"],
            "album": row["Nr albumu"],
            "wmii": row["Login WMII"],
        }

        if any([isinstance(k, float) and np.isnan(k) for k in parameters.values()]):
            log.warning("NaN detected: {}".format(parameters))

        out_path = args.output.format(**parameters)
        data = gen_data(**parameters)

        log.debug("generate qr for {name} {surname}: {data}".format(all=len(csv), data=data, **parameters))

        image_factory = qrcode.image.svg.SvgImage
        qr = qrcode.make(
            data,
            image_factory=image_factory,
            error_correction=getattr(qrcode.constants, args.error_correction),
        )
        qr.save(out_path)


if __name__ == '__main__':
    main()
