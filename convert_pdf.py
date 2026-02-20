import os
import subprocess
import sys
import glob
from PIL import Image # pip install Pillow

# check input file
if len(sys.argv) <= 1:
    print(f'Usage: {sys.argv[0]} input.pdf')
    exit(1)
input_fn = sys.argv[1]
if not input_fn.endswith('.pdf'):
    print(f'Error: {input_fn} is not a PDF file!')
    exit(1)
if not os.path.exists(input_fn):
    print(f'Error: {input_fn} not found!')
    exit(1)
# create tmp folder
print('[INFO] preparing tmp ...')
subprocess.run('mkdir -p tmp'.split())
subprocess.run(['rm', '-rf', './tmp'])
subprocess.run('mkdir -p tmp'.split())
# convert pdf to images and get page numbers
cmd = f'./helper/magick -density 120 {input_fn.replace(' ', '\\ ')} -alpha remove ./tmp/page-%d.png'
print('[INFO] converting pages ...')
subprocess.run(cmd.split())
fps = glob.glob('./tmp/page-*.png')
page_nums = sorted([fp.split('/')[-1][5:-4] for fp in fps])
# examine page size
image = Image.open(f'./tmp/page-{page_nums[0]}.png')
width, height = image.size
print(f'[INFO] page size = ({width}, {height})')
# set output file
output_fn = f'{input_fn[:-4]}_tagged.typ'
# write output file
print('[INFO] processing pages ...')
with open(output_fn, 'w') as f:
    f.write(f'#set page(width: {width*2}pt, height: {height*2}pt, margin: 1pt)\n')
    f.write('#set document(title: [Handwritten Lecture Notes])\n')
    f.write('\n')
    for pg in page_nums:
        f.write(f'#heading("Slide {pg}")\n')
        f.write(f'#image("tmp/page-{pg}.png", width: 90%, alt: "page {pg}")\n')
# compile typ to pdf
print('[INFO] generating tagged PDF ...')
subprocess.run(['./helper/typst', 'compile', output_fn.replace(' ', '\\ ')])
print(f'[INFO] output pdf is saved!')
# subprocess.run(['rm', '-rf', './tmp']) # don't remove tmp folder if you want to manually edit and compile the typ file.
# done

print('[INFO] DONE!')
