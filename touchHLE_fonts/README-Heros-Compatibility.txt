Skeuo Heros - TrueType compatibility builds of TeX Gyre Heros

Prepared by SkeuoHLE on 2026-11-20 from unmodified TeX Gyre Heros 2.004
Regular and Bold, downloaded from the official CTAN TeX Gyre distribution.
The old Arial.ttf and helvetica-bold.ttf files are not inputs to this build.

Original work: Copyright 2006, 2009 for TeX Gyre extensions by
B. Jackowski and J.M. Nowacki, on behalf of TeX users groups.
The original copyright notices are retained in the generated fonts.
Original authors do not provide support for these compatibility builds.
Modified version maintained by the SkeuoHLE project:
https://github.com/skeuoHLE/SkeuoHLE

Source package: https://mirrors.ctan.org/fonts/tex-gyre.zip
Project: https://ctan.org/pkg/tex-gyre
Original files are preserved in sources/:
  texgyreheros-regular.otf
    SHA-256 6ae1a09d5a940367b7aaaa91ee8bd8a2c333bfe193e7096e23f931357d62081f
  texgyreheros-bold.otf
    SHA-256 b170162835f4efc288886dd4231406dc47e19b614cf4416836635599d44a7d60

License: GUST Font License (GFL), under LPPL 1.3c or later.
See LICENSE.heros and LICENSE.lppl-1.3c.
The upstream README and manifest are retained in sources/.

Compatibility changes made from the original sources:
- Renamed the generated family to Skeuo Heros and documented this conversion.
- Converted cubic CFF outlines to quadratic TrueType outlines, maximum
  conversion error 0.5 design units at 2048 units per em.
- Normalized to 2048 units per em. Preserved horizontal advance widths.
- Set vertical scale and line metrics to match the guest's established layout:
  Regular cap height 1466, ascent 1854, descent -434, line gap 67;
  Bold cap height 1474, ascent 1577, descent -471, line gap 0.
- Preserved original Unicode coverage and OpenType positioning/substitution.

Arial.ttf and helvetica-bold.ttf are only compatibility filenames requested
by existing guest code; these files contain no proprietary Arial or Helvetica.
The original TeX Gyre OTF files cannot simply replace these files because
the emulator's text rasterizer needs TrueType outlines.

Regenerate with Python and FontTools 4.63.0:
  python3 dev-scripts/build_heros_fonts.py

The CTAN Regular face has small outline differences from the previous guest
font version, while keeping its line metrics and common Latin advances.
All comparisons and maintenance of these builds belong to SkeuoHLE.
