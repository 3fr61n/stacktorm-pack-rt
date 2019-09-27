#!/usr/bin/env python

import rt
import os

from st2common.runners.base_action import Action

class rt_create_ticket(Action):
    # Replace url, user, password with env vars
    tracker = rt.Rt(os.environ['RT_API_URL'], os.environ['RT_API_USER'], os.environ['RT_API_PASSWORD'])

    def login(self): 
        # Check if login was succesfull, if not then error
        return self.tracker.login()

    def check_if_a_ticket_already_exist(self, queue, subject):
        id=0
        for item in self.tracker.search(Queue=queue):
            # Adjust the query in order to be more precise.... (ie. closed? hostname?, etc)
            if (item['Subject'] == subject) and (item['Status'] in ['open', 'new']):
                id=str(item['id']).split('/')[-1]
        return id

    def run(self,queue,subject):
        self.logger.debug('Begins' + str(os.environ))
        self.login()
        ticket_id = self.check_if_a_ticket_already_exist(queue,subject)
        if ticket_id == 0:
            ticket_id = self.tracker.create_ticket(Queue=queue, Subject=subject)
            self.logger.info('New ticket created')
        else:
            self.logger.warning('Ticket already exists')
        return ticket_id

if __name__ == '__main__':
    checker = rt_create_ticket()

