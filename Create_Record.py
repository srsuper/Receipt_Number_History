# create record file
# since heroku doesn't allow longer than 30 seconds of process (function) runtime
# and for some reason heroku couldnt retreive the data fast enough (took only 12 second to finish on this machine)
# this is the only alternative i could come up with

from History import Prize_History
ph = Prize_History()

with open("record.txt", 'w') as f:
    f.write(str(ph.get_prize_dict()))
