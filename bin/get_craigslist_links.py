#! /usr/bin/env python3.7


import json
import os
import re
import requests
from constants.craigslist import CL_CONSTANTS
from domain.models import CraigsListLinks

from bs4 import BeautifulSoup
from typing import Dict, List
import click

ISSUE_FILE_REGEX = re.compile(r'^\d+\.json$')

@click.command()
def get_cl_links():

    cl_links: List[CraigsListLinks] = []

    craigs_list_url = "https://{}.craigslist.org/search/sof?employment_type=3"

    state_codes = CL_CONSTANTS.STATE_CODES.split(',')

    for code in state_codes:
        url: str = craigs_list_url.format(code)
        html: str = requests.get(url).text
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', attrs={"class":"result-title hdrlnk"}):
            if link.has_attr('href'):
                cl_links.append(CraigsListLinks(link.get('name'),link.get('href')))

    return click.echo(json.dumps([contributor for k, contributor in cl_links.items()], indent=2))

                
        


if __name__ == '__main__':
    get_cl_links()
