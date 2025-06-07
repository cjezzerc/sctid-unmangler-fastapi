import time

class MyTimer():
    __slots__=[
        "name",
        "t0", 
        ]
    def __init__(self, name=None):
        self.name=name
        self.t0=time.time()
    def make_split_timer_message(self):
        return f"SECTION_TIMER: {self.name} : took (in s) : {time.time()-self.t0}"
    def make_end_message(self):
        return     f"      SECTION_TIMER: {self.name} : took (in s) : {time.time()-self.t0}"
    def make_elapsed_message(self, master_timer=None, message=None):  
        if master_timer==None:  # this is for if call it as method of master timer
            return f" ANON_ELAPSED_TIMER: {self.name} : elapsed (in s) : {message} : {time.time()-self.t0}"
        else: # this is if call it as method of another timer
            return f"NAMED_ELAPSED_TIMER: {master_timer.name} : {self.name} : elapsed (in s) : {time.time()-master_timer.t0}"
