import configparser
import json
import os.path
import re

import math

import requests
from bs4 import BeautifulSoup
from pandas import read_excel

from orm.models import Call


class ProposalManager:

    def __init__(self, config: configparser.ConfigParser):
        self._config = config
        self.session = requests.Session()
        self._url = self._config['proposal']['url'].rstrip('/')
        self._role = ''
        self.technology_emails = {}

    def login(self):
        res = self.session.post(f'{self._url}/auth/signIn', data={
            'username': self._config['proposal']['user_name'],
            'password': self._config['proposal']['password'],
            'targetUri': '/timeline/list',
            'login':'Log+In'

        })
        if res.request.path_url != '/timeline/list':
            raise ConnectionError(f"Login failed! {res.status_code} => {res.text}")
        self._change_role_to_api()

    def _change_role_to_api(self):
        if self._role == 'api':
            return
        self._role = 'api'
        return self._change_role('ApiClient')

    def _change_role_to_scientist(self):
        if self._role == 'scientist':
            return
        self._role = 'scientist'
        return self._change_role('Scientist')

    def _change_role(self, role):
        res = self.session.get(f'{self._url}/auth/changeActiveRole?newRole={role}')
        if res.status_code != 200:
            raise ConnectionError(f"Request failed! {res.status_code} => {res.text}")
    def get_all_calls(self):
        self._change_role_to_scientist()
        res = self.session.get(f'{self._url}/proposalCalendar/index')
        if res.status_code != 200:
            raise ConnectionError(f"Request failed! {res.status_code} => {res.text}")
        # Parse the HTML content
        soup = BeautifulSoup(res.content, 'html.parser')
        # Find the select element by its name or id
        if soup is None:
            raise ConnectionError(f"Request failed! {res.status_code} => {res.text}")
        select = soup.find('select', {'name': 'proposalCallFilter'})
        # Get all option elements within the select
        options = select.find_all('option')
        return [int(option['value']) for option in options]

    def get_all_proposals(self):
        latest_call = Call.latest_call()
        all_calls = [f'proposalcallnumber={x}' for x in self.get_all_calls() if x > latest_call]


        self._change_role_to_api()

        data = [f"{k}={v}" for k,v in {'status': 'VALIDATED', 'order': 'desc'}.items()] + all_calls

        #res = self.session.get(f'{self._url}/proposal/exportAsExcel?{"&".join(data)}')
        #if res.status_code != 200:
        #    raise ConnectionError(f"Login failed! {res.status_code} => {res.text}")
        #filename = next(x.split('filename=')[-1] for x in res.headers['Content-disposition'].split(';') if 'filename=' in x)
        #with open(filename, 'wb+') as f:
        #    f.write(res.content)

        filename = '/home/martint/dev/KIT/ProposalMiner/proposal_miner/proposal-overview.xls'

        exel_content = read_excel(filename)
        for (i,x) in exel_content.iterrows():
            reference_key = x.get('Proposal ID')

            res = {
                'referenceKey': reference_key,
                'email': x.get('Proposer Email(s)'),
                'technologies': [y.strip() for y in x.get('Requested technologies').split(',')],
                'title': x.get('Title'),
                'keywords': x.get('Keywords'),
                'text': x.get('Reference text'),
                'call_number': x.get('Call')
            }
            if not isinstance(res['keywords'], str) and math.isnan(res['keywords']):
                res['keywords'] = '-'
            if not isinstance(res['text'], str) and math.isnan(res['text']):
                res['text'] = ''
            co_ops = str(x.get('Co-proposers', '')).split(',')
            res['co_ops'] = [x.split(' ')[-1].strip('<> ') for x in co_ops if x != '']

            yield res


    def _parse_tech_page(self, url_path):
        res = self.session.get(f'https://www.knmf.kit.edu{url_path}')
        if res.status_code != 200:
            raise ConnectionError(f"Request failed! {res.status_code} => {res.text}")
        # Parse the HTML content
        soup = BeautifulSoup(res.content, 'html.parser')
        # Find the select element by its name or id
        if soup is None:
            raise ConnectionError(f"Request failed! {res.status_code} => {res.text}")

        caption = soup.find('caption', text=re.compile(r".*Contact.*\("))
        for e in caption.parent.find_all('a', href=re.compile(r'emailform.*')):
            yield re.sub(r' ', '.', re.sub(r'does-not-exist\.', '', re.sub(r'\s*∂\s*', '@', e.text)))

    def get_all_technology_user(self):
        tp = os.path.join(os.path.dirname(__file__), 'technologies.json')
        with open(tp, 'r', encoding='utf8') as f:
            link_list = json.loads(f.read())
            for t, u in link_list.items():
                try:
                    self.technology_emails[t] = [x for x in self._parse_tech_page(u)]
                except (AttributeError, ConnectionError):
                    self.technology_emails[t] = []
        return self.technology_emails

    def get_emails_for_technology(self, technology):
        technology = re.sub(r'[ _\-]', '', technology).lower()
        return self.technology_emails.get(technology, [])