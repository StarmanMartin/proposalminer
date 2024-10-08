import os.path
import subprocess

from .models import Report, Proposal, Call


def clean_all(fp: str | None = None):
    Report.objects.all().delete()
    Proposal.objects.all().delete()
    Call.objects.all().delete()
    if fp is not None:
        path_dir = os.path.dirname(fp)
        CHEMOTION_PROCESS = subprocess.Popen(fp, shell=True, executable='/bin/bash', cwd=path_dir,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)

        while True:
            line = CHEMOTION_PROCESS.stdout.readline().decode("utf-8")
            if not line:
                return
            print(line.strip())
