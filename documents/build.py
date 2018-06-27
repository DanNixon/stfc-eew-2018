#!/usr/bin/env python

# Requires pypandoc (https://github.com/bebraw/pypandoc)

import glob
import os
import os.path

import pypandoc

output_directory = 'out'

files = glob.glob('*.md')

os.makedirs(output_directory, exist_ok=True)
for f in files:
    output_filename = os.path.join(os.path.dirname(f), output_directory, os.path.basename(f))
    output_filename = os.path.splitext(output_filename)[0] + '.pdf'
    pypandoc.convert_file(f, 'pdf', outputfile=output_filename)
