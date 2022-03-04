#!/bin/sh
''''exec python3 -u -- "$0" ${1+"$@"} # '''
# vi: syntax=python
import os
import json
import shutil
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dataclasses import dataclass
from pathlib import Path

DIRNAME = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(DIRNAME, 'images')
TEMPLATES_DIR = os.path.join(DIRNAME, 'templates')
VARIANTS_FILE = os.path.join(DIRNAME, 'variants.json')

env = Environment(
  loader=FileSystemLoader(TEMPLATES_DIR),
  autoescape=select_autoescape(),
  keep_trailing_newline=True,
)

@dataclass
class Variant:
  tag: str
  tags: List[str]
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

def main():
  reset()
  for variant in get_variants():
    make_variant(variant)

if __name__ == '__main__':
  main()
