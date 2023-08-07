from argparse import ArgumentParser

from opencc import OpenCC
from lxml import etree


cc = OpenCC("s2twp.json")


def translate(text: str) -> str:
    """Translate a string from simplified Chinese to traditional Chinese."""
    return cc.convert(text)


def translate_xliff(xliff_file: str):
    """Parse an XLIFF file into a dictionary of strings and their translations."""
    parser = etree.XMLParser()
    tree: etree._ElementTree = etree.parse(xliff_file)
    nsmap = tree.getroot().nsmap
    nsname = nsmap[list(nsmap.keys())[0]]
    ns = {"ns": nsname}
    root = tree.getroot()
    nodes = root.xpath("//ns:trans-unit", namespaces=ns)
    for unit in list(nodes):
        try:
            source: etree._Element = unit.xpath("ns:source", namespaces=ns)[0]
            target: etree._Element = unit.xpath("ns:target", namespaces=ns)[0]
            if source.text is None:
                continue
            if unit.get("translate") != "no":
                target.text = translate(source.text)
        except:
            continue

    return etree.tostring(root, pretty_print=True, encoding="utf-8").decode("utf-8")


if __name__ == "__main__":
    parser = ArgumentParser(prog="caster", description="Translate XLIFF files from simplified Chinese to traditional Chinese. Integrate with Crowdin.")
    subparsers = parser.add_subparsers()
    local_parser = subparsers.add_parser("local", help="Translate a local XLIFF file.")
    local_parser.add_argument("-f", "--file", help="The XLIFF file to translate. (zh-CN)")
    local_parser.add_argument("-o", "--output", help="The output file. (zh-TW)")
    args = parser.parse_args()
    result = translate_xliff(args.file)
    with open(args.output, "w") as f:
        f.write(result)
