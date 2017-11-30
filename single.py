import logging
from argparse import ArgumentParser

import qrcode
import qrcode.constants
import qrcode.image.pil
import qrcode.image.svg

from core import gen_data

log = logging.getLogger("kms_qr")


def main(argv=None):
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-s", "--surname", required=True)
    parser.add_argument("-l", "--kms", required=True)
    parser.add_argument("-a", "--album", required=True)
    parser.add_argument("-w", "--wmii", required=True)
    parser.add_argument("-o", "--output")
    parser.add_argument("-v", "--verbose", action="store_true")

    parser.add_argument("--error-correction", default="ERROR_CORRECT_H",
                        choices=[k for k in dir(qrcode.constants) if k.startswith("ERROR_CORRECT")])

    args = parser.parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    data = gen_data(**vars(args))
    log.info("data: {}".format(data))
    image_factory = None

    if args.output is None:
        image_factory = qrcode.image.pil.PilImage
    elif args.output.endswith(".svg"):
        image_factory = qrcode.image.svg.SvgImage
    elif args.output.endswith(".png"):
        image_factory = qrcode.image.pil.PilImage
    else:
        log.error("unknown output file extension: {}".format(args.output))
        exit(1)

    qr = qrcode.make(
        data,
        image_factory=image_factory,
        error_correction=getattr(qrcode.constants, args.error_correction),
    )

    if args.output is None:
        qr.show()
    else:
        qr.save(args.output)


if __name__ == '__main__':
    main()
