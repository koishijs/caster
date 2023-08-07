from argparse import ArgumentParser
from typing import Any, List

from crowdin_api import CrowdinClient
from opencc import OpenCC
import requests
from lxml import etree


cc = OpenCC("s2twp.json")


def translate(text: str) -> str:
    """Translate a string from simplified Chinese to traditional Chinese."""
    return cc.convert(text)


def translate_xliff(args: Any):
    """Parse an XLIFF file into a dictionary of strings and their translations."""
    xliff_file = args.file
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
            if target.get("state") == "needs-translation" and unit.get("translate") != "no":
                target.text = translate(source.text)
                target.set("state", "translated")
        except:
            continue

    result = etree.tostring(root, pretty_print=True, encoding="utf-8").decode("utf-8")
    output_file = args.output
    with open(output_file, "w") as f:
        f.write(result)


def download_xliff_from_crowdin(project_id: str, token: str, file_id: str = None):
    """Download an XLIFF file from Crowdin."""
    client = CrowdinClient(token=token)
    down = client.translations.export_project_translation(project_id, "zh-TW", "xliff", fileIds=[int(file_id)])
    url = down["data"]["url"]
    res = requests.get(url)
    filename = "temp/" + file_id + ".xliff"
    with open(filename, "wb") as f:
        f.write(res.content)
    return filename


def translate_crowdin(args):
    """Translate a Crowdin project."""
    project_id = int(args.project)
    token = args.token
    file_glob = args.file
    file = download_xliff_from_crowdin(project_id, token, file_glob)
    output_file = file.replace(".xliff", ".tw.xliff")

    class Args:
        file: str
        output: str
    fake_args = Args()
    fake_args.file = file
    fake_args.output = output_file

    translate_xliff(fake_args)
    if not args.dry_run:
        client = CrowdinClient(token=token)
        storageId = client.storages.add_storage(open(file, "rb"))["data"]["id"]
        client.translations.upload_translation(project_id, "zh-TW", storageId, int(args.file))


if __name__ == "__main__":
    parser = ArgumentParser(prog="caster", description="Translate XLIFF files from simplified Chinese to traditional Chinese. Integrate with Crowdin.")
    subparsers = parser.add_subparsers()
    local_parser = subparsers.add_parser("local", help="Translate a local XLIFF file.")
    local_parser.add_argument("-f", "--file", help="The XLIFF file to translate. (zh-CN)", required=True)
    local_parser.add_argument("-o", "--output", help="The output file. (zh-TW)", required=True)
    local_parser.set_defaults(func=translate_xliff)

    remote_parser = subparsers.add_parser("remote", help="Translate a remote XLIFF file from Crowdin.")
    remote_parser.add_argument("-p", "--project", help="The Crowdin project ID.", required=True)
    remote_parser.add_argument("-t", "--token", help="The Crowdin API token.", required=True)
    remote_parser.add_argument("-f", "--file", help="The XLIFF file glob to translate.")
    remote_parser.add_argument("--dry-run", help="Don't actually upload the translated file to Crowdin.", action="store_true", default=False)
    remote_parser.set_defaults(func=translate_crowdin)

    args = parser.parse_args()
    args.func(args)
