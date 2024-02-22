import string

from chemotion_api import Instance
from chemotion_api.collection import Collection
from chemotion_api.user import Person, Group

from orm.models import Proposal
from config_manager import Config


class Chemotion:
    def __init__(self):
        self.idx = len(Proposal.objects.all())
        chemotion_config = Config()['chemotion']
        self.instance = Instance(chemotion_config['url']).login(chemotion_config['user'],
                                                                chemotion_config['password']).test_connection()

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
            return self.instance.get_user().create_group(last_name=key, first_name=title, name_abbreviation=group_name)
        except:
            return self.next_group(title, key, self.idx)

    def new_collection(self, group: Group, key: str):
        col: Collection = self.instance.get_root_collection().get_or_create_collection(key)
        col.share()
        pass
    def get_all_user(self) -> list[Person]:
        pass