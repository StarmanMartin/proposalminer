import configparser

import requests
from bs4 import BeautifulSoup

from orm.models import Call


class ProposalManager:

    def __init__(self, config: configparser.ConfigParser):
        self._config = config
        self.session = requests.Session()
        self._url = self._config['proposal']['url'].rstrip('/')

    def login(self):
        res = self.session.post(f'{self._url}/auth/signIn', data={
            'username': self._config['proposal']['user'],
            'password': self._config['proposal']['password'],
            'targetUri': '/timeline/list',
            'login':'Log+In'

        })
        if res.request.path_url != '/timeline/list':
            raise ConnectionError(f"Login failed! {res.status_code} => {res.text}")

    def get_all_calls(self):
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
        offset = 0
        page_size = 5
        total = 0
        while offset <= total:
            data = [f"{k}={v}" for k,v in {'projectfinishedstatus': 'not_finished', 'max': page_size, 'offset': offset}.items()] + all_calls

            res = self.session.get(f'{self._url}/proposalListApi/acceptedProposalPage?{"&".join(data)}', data={'projectfinishedstatus': 'not_finished', 'max': page_size})
            if res.status_code != 200:
                raise ConnectionError(f"Login failed! {res.status_code} => {res.text}")
            data = res.json()
            total = data['count']
            offset += page_size
            for prop in data['list']:
                yield prop