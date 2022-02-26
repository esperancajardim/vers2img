import argparse
import gettext
import sys
import tkinter as tk

from pathlib import Path

import core
import ui

_ = gettext.gettext
defaults = core.load_default()

# Read/Interpret Input
parser = argparse.ArgumentParser(
    description=_("Generate versicle images"),
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=_("\t- If you wish to change default configurations, please edit {}\n \
    \t- Add extra bible versions in {}\n \
    \t- Add extra fonts in {}")
    .format(str(Path(core.home_path) / "default.json"), str(Path(core.home_path) / "versions"), str(Path(core.home_path) / "fonts") ))
parser.add_argument("reference", nargs='?',
    action="store", help=_("Text reference abbreviation. Eg: 1Ts_1_1-33"))
parser.add_argument("--version",
	dest="version", action="store", default=f'{defaults["version"].lower()}', help=_("Bible version to be used. Available (PT): AA, ACF, NVI. Default: {}").format(defaults["version"].upper()))
parser.add_argument("--output",
    dest="output", action="store", default=".", help=_("Select output path. Default: ."))
parser.add_argument("--gui", 
    action="store_true", help=_("Start GUI version"))
parser.add_argument("--preview", 
    action="store_true", help=_("View image preview with style applied to dummy text"))
parser.add_argument("--list-versions", 
    dest="list_versions", action="store_true", help=_("List available bible versions"))
parser.add_argument("--background", 
    action="store", default=f'{defaults["background"]}', help=_("Select background image to use. Size must be 1920x1080"))
parser.add_argument("--title-font", 
    action="store", dest="title_font", default=defaults["fonts"]["title"], help=_("Font that will be used in the title (reference)"))
parser.add_argument("--title-size", 
    action="store", dest="title_size", default=defaults["fonts"]["title_size"], help=_("Title size"))
parser.add_argument("--text-font", 
    action="store", dest="text_font", default=defaults["fonts"]["text"], help=_("Font that will be used in the text"))
parser.add_argument("--text-size", 
    action="store", dest="text_size", default=defaults["fonts"]["text_size"], help=_("Text size"))
parser.add_argument("--save-default", 
    action="store_true", dest="save_default", help=_("Save options to default file"))
args = parser.parse_args()

if args.gui is True:
    root = tk.Tk()
    ui.Application(root)
    root.mainloop()
    sys.exit(0)

if args.preview is True:
    core.render_preview(
        title_font=args.title_font,
        title_size=args.title_size,
        text_font=args.text_font,
        text_size=args.text_size,
        background=args.background
    )
    sys.exit(0)

if args.list_versions is True:
    versions = [version.stem.upper() for version in Path(f"{core.install_path}/assets/versions").iterdir() if version.name.endswith(".json")]
    if Path(f"{core.home_path}/versions").exists():
        versions.extend([version.stem.upper() for version in Path(f"{core.home_path}/versions").iterdir() if version.name.endswith(".json")])
    print(*versions)
    sys.exit(0)

if args.save_default is True:
    core.save_default(defaults, background=args.background, version=args.version, title_font=args.title_font, title_size=args.title_size, text_font=args.text_font, text_size=args.text_size)

if args.reference is None or (len(args.reference.split("_")) != 3):
    print(_("Reference non existent or format is invalid"))
    parser.print_help()
    sys.exit(1)

bible = core.load_bible(version=args.version)
book, chapter, versicles = core.prepare_text(bible=bible, reference=args.reference)

core.render_text(
    book=book,
    chapter=chapter,
    versicle=versicles,
    title_font=args.title_font,
    title_size=args.title_size,
    text_font=args.text_font,
    text_size=args.text_size,
    output=args.output,
    background=args.background
)