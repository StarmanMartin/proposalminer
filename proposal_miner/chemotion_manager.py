from chemotion_api import Instance, ResearchPlan
from chemotion_api.collection import Collection, SyncPermission
from chemotion_api.user import Group, Person

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

    def new_collection(self, group: list[Person], key: str) -> Collection:
        col: Collection = self.instance.get_root_collection().get_or_create_collection(key)
        col.share(SyncPermission.PassOwnership, *group)
        return col

    def get_all_user(self) -> dict[str, Person]:
        if self._all_user is None:

            conn = psycopg2.connect(**self.pg_connection_dict)
            cur = conn.cursor()
            cur.execute("SELECT t.* FROM public.users t WHERE type='Person'")
            self._all_user = {}
            temp_user={}
            for result in cur.fetchall():
                self._all_user[result[1]] = Person(None)
                for i, d in  enumerate(cur.description):
                    temp_user[d.name] = result[i]
                self._all_user[result[1]] .populate(temp_user)


        return self._all_user
