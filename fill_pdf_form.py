import json
import os

from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import click
from PyPDF2.generic import StreamObject, NameObject, NumberObject
from PyPDF2.pdf import ContentStream, PageObject
from fillpdf import fillpdfs
from shutil import copyfile


def _remove_watermarks(path: str):
    output_path = str(os.path.splitext(path)[0]) + "_m.pdf"

    if os.path.exists(output_path):
        os.remove(output_path)
    copyfile(path, output_path)

    pdf_merger = PdfFileMerger()

    with open(path, "rb") as file:
        doc = PdfFileReader(file)
        pdf_merger.append(doc)

        for merged_page in pdf_merger.pages:
            page: PageObject = merged_page.pagedata
            found_watermark = False

            for el in page:
                content_object = page[el].getObject()
                if isinstance(content_object, StreamObject):
                    content = ContentStream(content_object, page)
                    for operands, operator in content.operations:
                        op = operator.decode("ascii")
                        if op == "cm" and found_watermark:
                            for i in range(len(operands)):
                                operands[i] = NumberObject(0)
                        if op == "BDC":
                            if (
                                len(operands) == 2
                                and operands[0] == "/Artifact"
                                and operands[1]["/Subtype"] == "/Watermark"
                            ):
                                found_watermark = True
                        if op == "EMC":
                            found_watermark = False
                            print("---END---")
                        print(op, operands if len(operands) > 0 else "")

            page.__setitem__(NameObject("/Contents"), content)

    output_path = str(os.path.splitext(path)[0]) + "_m.pdf"
    with open(output_path, "wb") as file:
        print(f"Saving file into {output_path}")
        pdf_merger.write(file)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path")
def get_form_fields(path: str):
    print(fillpdfs.get_form_fields(path))


@cli.command()
@click.argument("pdf_path")
@click.argument("data_path")
def fill_pdf_forms(pdf_path: str, data_path: str):
    """Fill pdf form using data from json file + removes watermark from the source pdf file

    Json file format:
    { "common": {}, "seperate": [] }

    For each of the "seperate" item, which has to be a dictionary, generates new data concatenating "common" + "seperate"[idx].
    Allows to define common data for every generated pdf, and for each of the 'seperate' list item generates new pdf with the data
    comming from that dictionary.

    An example:
    {
        "common": {"name": "John Unknown", "address": "WWW"},
        "seperate": [
            {"year": 2020, "net": 100, "gross": 120},
            {"year": 2021, "net": 10, "gross": 12}
        ]
    }
    Args:
        pdf_path (str): source form pdf file path
        data_path (str): data json file path
    """
    with open(data_path, "rb") as file:
        data = json.load(file)

    common_data = data["common"]

    for idx, separate_data in enumerate(data["separate"]):
        output_path = str(os.path.splitext(pdf_path)[0]) + f"_d{idx}.pdf"
        data = {**common_data, **separate_data}
        fillpdfs.write_fillable_pdf(pdf_path, output_path, data)
        _remove_watermarks(output_path)

    # If you want it flattened:
    # fillpdfs.flatten_pdf('new.pdf', 'newflat.pdf')


@cli.command()
@click.argument("path")
def remove_watermarks(path: str):
    _remove_watermarks(path)


@cli.command()
@click.argument("path")
def find_images(path: str):
    with open(path, "rb") as file:
        doc = PdfFileReader(file)
        page0 = doc.getPage(0)
        if "/XObject" in page0["/Resources"]:
            xObject = page0["/Resources"]["/XObject"].getObject()

            for obj in xObject:
                if xObject[obj]["/Subtype"] == "/Image":
                    size = (xObject[obj]["/Width"], xObject[obj]["/Height"])
                    if "/Filter" in xObject[obj]:
                        if xObject[obj]["/Filter"] == "/FlateDecode":
                            print(obj[1:] + ".png")
                        elif xObject[obj]["/Filter"] == "/DCTDecode":
                            print(obj[1:] + ".jpg")
                        elif xObject[obj]["/Filter"] == "/JPXDecode":
                            print(obj[1:] + ".jp2")
                        elif xObject[obj]["/Filter"] == "/CCITTFaxDecode":
                            print(obj[1:] + ".tiff")
                    else:
                        print(obj[1:] + ".png")
                    print(f"Size: {size}")
        else:
            print("No image found.")


if __name__ == "__main__":
    cli()
