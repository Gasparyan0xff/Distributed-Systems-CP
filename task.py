import datetime

MAX_PRIORITY = 8

class Task:
    def __init__(self, id, content, priority, timestamp):
        self.id = id
        self.content = content
        self.priority = priority
        self.timestamp = timestamp
        self.mark_complete = False
        self.completed = False
    
    def get_id(self):
        return self.id
    
    def get_content(self):
        return self.content
    
    def get_priority(self):
        return self.priority

    def get_timestamp(self):
        return self.timestamp

    def get_mark_complete(self):
        return self.mark_complete

    def get_completed(self):
        return self.completed

    def set_priority(self, priority):
        self.priority = priority
    
    def set_content(self, content):
        self.content = content
    
    def set_mark_complete(self, mark_compl):
        self.mark_complete = mark_compl

    def set_complete(self, flag_compl):
        self.completed = flag_compl

