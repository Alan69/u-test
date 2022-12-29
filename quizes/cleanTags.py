import re

CLEANR = re.compile('_x000D_')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext


remove_path = re.compile('public/images/')

def removepath(raw_html):
  replacetext = re.sub(remove_path, 'https://u-test.kz/static/public/images/', raw_html)
  return replacetext