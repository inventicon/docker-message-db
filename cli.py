#!/usr/bin/env python3
# vi: syntax=python
import os
import json
import shutil
import sys
import subprocess
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dataclasses import dataclass
from pathlib import Path

DIRNAME = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(DIRNAME, 'images')
TEMPLATES_DIR = os.path.join(DIRNAME, 'templates')
VARIANTS_FILE = os.path.join(DIRNAME, 'variants.json')

IMAGE_NAME = 'inventicon/message-db'

env = Environment(
  loader=FileSystemLoader(TEMPLATES_DIR),
  autoescape=select_autoescape(),
  keep_trailing_newline=True,
)

@dataclass
class Variant:
  tag: str
  aliases: List[str]
  vars: Dict
  template: str

def reset():
  shutil.rmtree(IMAGES_DIR)
  os.makedirs(IMAGES_DIR)
  pass

def get_variants():
  f = open(VARIANTS_FILE, 'r')
  data = json.load(f)
  variants = []
  for tag, variant in data.items():
    variants.append(Variant(tag, **variant))
  return sorted(variants, key = lambda i: i.tag)

def make_variant(variant: Variant):
  # create variant folder
  dir = os.path.join(IMAGES_DIR, variant.tag)
  os.makedirs(dir, exist_ok=True)
  # copy template files
  template_files = os.listdir(os.path.join(TEMPLATES_DIR, variant.template))
  for template_file in template_files:
    dest = os.path.join(dir, Path(template_file).name)
    template = env.get_template(os.path.join(variant.template, template_file))
    with open(dest, 'w') as fh:
      fh.write(template.render(variant.vars))

def build_variant(variant: Variant):
  main_tag = IMAGE_NAME + ':' + variant.tag
  print(f'[{main_tag}]')
  proc = subprocess.Popen(
    ['docker', 'build', '--tag', main_tag, '.'],
    cwd=os.path.join(IMAGES_DIR, variant.tag)
  )
  proc.wait()
  for alias in variant.aliases:
    alias_tag = IMAGE_NAME + ':' + alias
    print(f'[{main_tag}] => [{alias_tag}]')
    subprocess.Popen(['docker', 'tag', main_tag, alias_tag]).wait()
  pass

def build():
  print('Building...')
  for variant in get_variants():
    build_variant(variant)

def generate():
  print('Generating...')
  reset()
  for variant in get_variants():
    make_variant(variant)

def main():
  command = sys.argv[1].lower() if len(sys.argv) > 1 else None
  if command == 'build':
    build()
  elif command == 'generate':
    generate()
  else:
    generate()
    build()

if __name__ == '__main__':
  main()
