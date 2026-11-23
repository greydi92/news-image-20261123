// news-image-20261123 entry (Node 22, standard library only): its image is
// the entry.png beside this file, drawn at build time by gen_image.py
// (Pillow + DejaVu fonts, every pixel drawn in code), and the program
// copies it to /output/entry.png. The gate takes a whole PNG of at most
// 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes
// copied. No network, no drawing at run time: two runs write identical
// bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { chmodSync, copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);
// The grader collects outputs as another user: leave the file readable.
chmodSync(dest, 0o644);
