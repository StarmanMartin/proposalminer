from chemotion_api.elements.research_plan import ResearchPlan

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
    pm.get_all_technology_user()
    for prop_data in pm.get_all_proposals():
        (prop, created) = Proposal.objects.get_or_create(proposal_key=prop_data['referenceKey'])
        if created:
            call_list.add(prop_data['call_number'])
            prop.name = prop_data['title']
            emails = [prop_data['email']] + prop_data['co_ops']
            for technology in prop_data['technologies']:
                emails += pm.get_emails_for_technology(technology)
            user = chemotion.get_all_user()
            user = [user[email] for email in emails if email in user]
            if len(user) > 0:
                group = chemotion.next_group(prop.name, prop.proposal_key)
                group.add_users_by_id(*user)
                prop.group = group.id
                col = chemotion.new_collection(group, prop.proposal_key)
                rs_1: ResearchPlan = col.new_research_plan()
                rs_1.name = prop_data['title']
                rs_1.add_richtext(f'Keywords: {prop_data["keywords"]}')
                rs_1.add_richtext(prop_data["text"])
                table = rs_1.add_table()
                table['value']['columns'] = table['value']['columns'][:2]
                table['value']['columns'][0]['headerName'] = 'E-Mail'
                table['value']['columns'][1]['headerName'] = 'Technology'
                table['value']['rows'] = []
                for technology in prop_data['technologies']:
                    for email in pm.get_emails_for_technology(technology):
                        table['value']['rows'].append({'a': email, 'b': technology})
                rs_1.save()
                prop.collection = col.id
                prop.save()
    if len(call_list) > 0:
        Call.add_calls(*call_list)
        Call.call_done(max(call_list))
