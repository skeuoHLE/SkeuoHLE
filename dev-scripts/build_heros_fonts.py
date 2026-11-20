#!/usr/bin/env python3
"""Build Skeuo Heros guest fonts from unmodified CTAN TeX Gyre Heros sources.

Requires fonttools 4.63.0. Outputs keep the guest's legacy filenames and layout
metrics while using the original Heros outlines. No generated font is an input.
"""
import argparse
import copy
import hashlib
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.misc.roundTools import otRound
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.scaleUpem import scale_upem

PROFILES = {
    "regular": ("Arial.ttf", "Regular", "6ae1a09d5a940367b7aaaa91ee8bd8a2c333bfe193e7096e23f931357d62081f",
                (1854, -434, 67), (1491, -431, 307), (1854, 434), 1466),
    "bold": ("helvetica-bold.ttf", "Bold", "b170162835f4efc288886dd4231406dc47e19b614cf4416836635599d44a7d60",
             (1577, -471, 0), (1536, -348, 61), (1966, 475), 1474),
}


def build(source_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for face, (filename, style, checksum, line, typo, win, cap) in PROFILES.items():
        source_path = source_dir / f"texgyreheros-{face}.otf"
        if hashlib.sha256(source_path.read_bytes()).hexdigest() != checksum:
            raise ValueError(f"Unexpected upstream source: {source_path}")
        original = TTFont(source_path, recalcTimestamp=False)
        scale_upem(original, 2048)
        outlines = original.getGlyphSet()
        order = original.getGlyphOrder()
        converted = {}
        vertical_scale = cap / original["OS/2"].sCapHeight
        for glyph_name in order:
            target = TTGlyphPen(None)
            quadratic = Cu2QuPen(target, max_err=0.5, reverse_direction=True)
            outlines[glyph_name].draw(TransformPen(quadratic, (1, 0, 0, vertical_scale, 0, 0)))
            converted[glyph_name] = target.glyph()
        font = FontBuilder(2048, isTTF=True)
        font.setupGlyphOrder(order)
        font.setupCharacterMap(original.getBestCmap())
        font.setupGlyf(converted)
        metrics = {
            name: (original["hmtx"][name][0], converted[name].xMin if converted[name].numberOfContours else 0)
            for name in order
        }
        font.setupHorizontalMetrics(metrics)
        font.setupHorizontalHeader(ascent=line[0], descent=line[1], lineGap=line[2])
        font.setupNameTable({
            "familyName": "Skeuo Heros", "styleName": style,
            "uniqueFontIdentifier": f"SkeuoHeros-{style}-1.000",
            "fullName": f"Skeuo Heros {style}", "psName": f"SkeuoHeros-{style}",
            "version": "Version 1.000; based on TeX Gyre Heros 2.004",
            "copyright": original["name"].getDebugName(0),
            "manufacturer": "SkeuoHLE",
            "description": "Independently converted from the original TeX Gyre Heros OTF. "
                "TrueType outlines and guest layout metrics prepared by SkeuoHLE. "
                "See README-Heros-Compatibility.txt for sources and changes.",
            "licenseDescription": "GUST Font License; LPPL 1.3c or later. See LICENSE.heros and LICENSE.lppl-1.3c.",
            "licenseInfoURL": "https://www.gust.org.pl/projects/e-foundry/licenses/GUST-FONT-LICENSE.txt",
        })
        font.setupOS2()
        font.font["OS/2"] = copy.deepcopy(original["OS/2"])
        os2 = font.font["OS/2"]
        os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap = typo
        os2.usWinAscent, os2.usWinDescent = win
        os2.sCapHeight = cap
        os2.sxHeight = otRound(os2.sxHeight * vertical_scale)
        os2.fsSelection = 32 if face == "bold" else 64
        os2.fsType = 0
        font.setupPost(keepGlyphNames=True, underlinePosition=original["post"].underlinePosition,
                       underlineThickness=original["post"].underlineThickness)
        for tag in ("GDEF", "GPOS", "GSUB"):
            if tag in original:
                font.font[tag] = copy.deepcopy(original[tag])
        font.font["head"].created = original["head"].created
        font.font["head"].modified = 3877977600  # Fixed conversion date: 2026-11-20 UTC.
        font.font["head"].macStyle = 1 if face == "bold" else 0
        path = output_dir / filename
        font.save(path)
        check = TTFont(path)
        assert "glyf" in check and "CFF " not in check
        assert check["hhea"].ascent == line[0]
        assert check["glyf"][check.getBestCmap()[ord("H")]].yMax == cap
        print(f"{filename}: {len(check.getBestCmap())} characters, {style}, 2048 UPM")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent.parent
    parser.add_argument("--sources", type=Path, default=root / "touchHLE_fonts/sources")
    parser.add_argument("--output", type=Path, default=root / "touchHLE_fonts")
    args = parser.parse_args()
    build(args.sources, args.output)
