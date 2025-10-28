import logging
import os

from chemotion_api.elements.research_plan import ResearchPlan

from db_manager import setup

setup()

from chemotion_manager import Chemotion
from chemotion_api.elements.research_plan import RichText
from config_manager import Config

from orm.models import Proposal, Call, Report

from proposal_manager import ProposalManager

FORMAT = '%(asctime)s %(message)s'
log_dir = os.environ.get("LOG_DIR", './log_file.txt')
if os.environ.get("MODE", 'DEBUG') != 'DEBUG':
    os.makedirs(os.path.dirname(log_dir), exist_ok=True)
    logging.basicConfig(level=logging.INFO, filename=log_dir, format=FORMAT)
else:
    os.makedirs(os.path.dirname(log_dir), exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler(log_dir), logging.StreamHandler()], format=FORMAT)
logger = logging.getLogger(__name__)


def run(config_path: str):
    logger.info('Started process!')
    Config().read(config_path)
    chemotion = Chemotion()
    logger.info('Successfully, logged in to Chemotion')
    pm = ProposalManager(Config())
    pm.login()
    logger.info('Successfully, logged in to Proposal Manager')
    call_list = set()
    pm.get_all_technology_user()
    logger.info('Fetching all Technology user')
    pm.get_app_status_reports()
    logger.info('Fetching new Proposals')
    for prop_data in pm.get_all_proposals():
        (prop, created) = Proposal.objects.get_or_create(proposal_key=prop_data['referenceKey'])
        if created:
            logger.info('Found Proposal %s', prop_data['title'])
            call_list.add(prop_data['call_number'])
            prop.name = prop_data['title']
            emails = [prop_data['email']] + prop_data['co_ops']
            for technology in prop_data['technologies']:
                emails += pm.get_emails_for_technology(technology)
            # emails += ['martin.starman@kit.edu']
            user = chemotion.get_all_user()
            user = [user[email] for email in emails if email in user]
            logger.info('Selected user: [%s]', ','.join([f"{p.name} <{p.email}>" for p in user]))
            if len(user) > 0:

                logger.info('Create shared collection')
                col = chemotion.new_collection(user, prop.proposal_key)
                rs_1: ResearchPlan = col.new_research_plan()
                rs_1.name = prop_data['title']
                rs_1.add_richtext(f'Keywords: {prop_data["keywords"]}')
                rs_1.add_richtext(prop_data["text"])
                table = rs_1.add_table()
                table.add_columns('E-Mail', 'Technology')
                for technology in prop_data['technologies']:
                    for email in pm.get_emails_for_technology(technology):
                        table.add_row(email, technology)
                pdf_path = pm.download_pdf(prop.proposal_key)
                rs_1.attachments.add_file(pdf_path)
                rs_1.save()
                prop.collection = col.id
                prop.research_plan = rs_1.id
                prop.save()

    logger.info('Proposal done!')
    logger.info('Fetching Proposal Reports!')
    for prop in Proposal.objects.all():
        if prop.research_plan is not None:
            rs_1 = chemotion.get_rp(prop)
            reports = Report.objects.filter(synced=False, proposal_id=prop.proposal_key)
            first = prop.research_plan_status_table is None
            keys = None
            t_idx, table = next(((i, x) for i, x in enumerate(rs_1.body) if x['id'] == prop.research_plan_status_table),
                                (len(rs_1.body), None))
            if table is None:
                table = rs_1.add_table()
                prop.research_plan_status_table = table['id']
                prop.save()

            for report in reports:
                if first:
                    first = False
                    rt = rs_1.add_richtext(at_idx=t_idx)
                    rt.add_text("Reports:\n", header=RichText.HeaderType.H2)
                    rt = rs_1.add_richtext(at_idx=1)
                    rt.add_text(f"Proposal ID:", bold=True).add_text(f"{report.data.get('Proposal ID')}\n",
                                                                     list='bullet')
                    rt.add_text(f"Proposal Type:", bold=True).add_text(f"{report.data.get('Proposal Type')}\n",
                                                                       list='bullet')
                    rt.add_text(f"Start date (scheduled):", bold=True).add_text(
                        f"{report.data.get('Start date (scheduled)')}\n", list='bullet')
                    rt.add_text(f"End date (scheduled):", bold=True).add_text(
                        f"{report.data.get('End date (scheduled)')}\n", list='bullet')

                    keys = [x for x in report.data.keys() if
                            x not in ['Proposal ID', 'Proposal Type', 'Start date (scheduled)', 'End date (scheduled)']]
                    table.add_columns(*keys)
                logger.info(f'Reports for {prop.proposal_key} -> {report.technology}!')
                if table is not None:
                    table.add_row(*[report.data.get(k) for k in keys])
            reports.update(synced=True)

            if not first:
                rs_1.save()

    if len(call_list) > 0:
        Call.add_calls(*call_list)
        Call.call_done(max(call_list))
