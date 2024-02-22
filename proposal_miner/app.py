from db_manager import setup

setup()

from chemotion_manager import Chemotion
from config_manager import Config

from orm.models import Proposal, Call

from proposal_manager import ProposalManager


def run(config_path: str):
    Config().read(config_path)
    chemotion = Chemotion()
    pm = ProposalManager(Config())
    pm.login()
    call_list = set()
    for prop_data in pm.get_all_proposals():
        (prop, created) = Proposal.objects.get_or_create(proposal_id=prop_data['id'],
                                                       proposal_key=prop_data['referenceKey'])
        if created:
            call_list.add(prop_data['callNumber'])
            prop.name = prop_data['title']
            group = chemotion.next_group(prop.name, prop.proposal_key)
            prop.group = group.id
            prop.collection = chemotion.new_collection(group, prop.proposal_key)
            prop.save()
    Call.add_calls(*call_list)
    Call.call_done(min(call_list))
