import string

from chemotion_api import Instance, ResearchPlan
from chemotion_api.collection import Collection, SyncPermission
from chemotion_api.user import Group

import psycopg2
from orm.models import Proposal
from config_manager import Config


class Chemotion:
    def __init__(self):
        self.idx = len(Proposal.objects.all())
        self._all_user = None
        chemotion_config = Config()['chemotion']
        self.instance = Instance(chemotion_config['url']).login(chemotion_config['user_name'],
                                                                chemotion_config['password']).test_connection()

    def get_rp(self, prop: Proposal) -> ResearchPlan:
        return self.instance.get_research_plan(prop.research_plan)

    @property
    def pg_connection_dict(self):
        chemotion_config = Config()['chemotion']
        return {
            'dbname': chemotion_config['db_name'],
            'user': chemotion_config['db_user'],
            'password': chemotion_config['db_password'],
            'port': chemotion_config['db_port'],
            'host': chemotion_config['db_host']
        }

    def next_group(self, title, key, idx=None):
        if idx is not None:
            self.idx = idx
        idx = self.idx
        self.idx += 1
        cases = list(string.ascii_uppercase)
        group_name = ['K']
        for i in range(3):
            group_name.append(cases[idx % len(cases)])
            idx //= len(cases)
        group_name = ''.join(group_name)
        try:
            g = self.instance.get_user().create_group(last_name=key, first_name=title, name_abbreviation=group_name)
            return g
        except:
            return self.next_group(title, key, self.idx)

    def new_collection(self, group: Group, key: str) -> Collection:
        col: Collection = self.instance.get_root_collection().get_or_create_collection(key)
        col.share(SyncPermission.PassOwnership, group)
        return col

    def up_date_group_name(self, group: Group, key: str):
        conn = psycopg2.connect(**self.pg_connection_dict)
        cur = conn.cursor()
        key = key.replace('-', '')[2:]
        cur.execute(f"UPDATE public.users SET name_abbreviation = '{key}'::varchar(12) WHERE id = {group.id}::integer;")
        for result in cur.fetchall():
            print(result)
        return key

    def get_all_user(self) -> dict[str, int]:
        if self._all_user is None:

            conn = psycopg2.connect(**self.pg_connection_dict)
            cur = conn.cursor()
            cur.execute("SELECT t.* FROM public.users t WHERE type='Person'")
            self._all_user = {}
            for result in cur.fetchall():
                self._all_user[result[1]] = result[0]

        return self._all_user
