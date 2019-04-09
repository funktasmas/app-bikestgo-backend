from django_cron import CronJobBase, Schedule
from .process import save_data_api


class CronJobData(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'cron.data'

    def do(self):
        save_data_api()
