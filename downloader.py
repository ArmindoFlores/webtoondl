import argparse
import base64
import os

import webtoon


def get_code(webtoon):
    return f"{webtoon['type']}{webtoon['eid']}"

def search(args):
    if args.name is None:
        print("You must specify a name to search for")
        return
    try:
        originals, canvas = webtoon.search(args.name)
    except Exception:
        print("An error occurred while searching")
        return
    if len(originals) == 0 and len(canvas) == 0:
        print("No results")
        return
    
    if len(originals) != 0:
        print("ORIGINALS:")
        for i in range(len(originals)):
            print(f"\t{i+1}. {originals[i]['name']} - {originals[i]['author']} - {originals[i]['genre']} ({originals[i]['likes']}) [{get_code(originals[i])}]")
    if len(canvas) != 0:
        print("\nCANVAS:")
        for i in range(len(canvas)):
            print(f"\t{i+len(originals)+1}. {canvas[i]['name']} - {canvas[i]['author']} - {canvas[i]['genre']} [{get_code(canvas[i])}]")
    print("\nTo download one of these works, use the option 'download' with --id equal to the webtoon's id (for example, c4324)")

def download(args):
    if args.output is None:
        print("The output directory option is required for downloading")
        return
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
    try:
        if args.id is not None:
            url = webtoon.get_url_from_id(args.id)
            print(url, webtoon.get_name_from_url(url))
            urls, referer = webtoon.get_img_urls(url, 1, int(args.id[1:]))
            webtoon.download_imgs(urls, referer, os.path.join(args.output, webtoon.get_name_from_url(url)))
        else:
            print("Please specify either --id or --url")
    except Exception as e:
        print(e)
        print("An error occurred while downloading")
        return

def main():
    parser = argparse.ArgumentParser(description="Download webtoons")
    parser.add_argument("option", metavar="option", type=str, nargs=1, help="search / download")
    parser.add_argument("--url", help="Specify the download url")
    parser.add_argument("--name", help="Specify the webtoon's name")
    parser.add_argument("--id", help="Specify the webtoon's id")
    parser.add_argument("output", metavar="output", type=str, nargs="?", help="Output directory")
    args = parser.parse_args()
    
    if args.option[0] == "search":
        search(args)
    elif args.option[0] == "download":
        download(args)
    else:
        print(f"Invalid option '{args.option[0]}'")
        parser.print_usage()

if __name__ == "__main__":
    main()