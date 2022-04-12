@auth.requires_login()
def view():
    completed_schedule = db((db.events.completed==True) & (db.events.season==2022)).select(orderby=db.events.event_number)
    current_event = db((db.events.ready==True) & (db.events.season == 2022)).select(orderby=db.events.event_number)
    if len(current_event) > 0:
        current_event_id = current_event[0].id
        submitted_picks = db(db.picks.event_id==current_event_id).select()
        user_submitted = []
        for picks in submitted_picks:
            user_submitted.append(picks.user_id)
        if current.auth_user.id in user_submitted:
            user_picks = db((db.picks.event_id==current_event_id) & (db.picks.user_id==current.auth_user.id)).select()
            user_picks_id = user_picks[0].id
    playing_event = db((db.events.playing==True) & (db.events.season == 2022)).select(orderby=db.events.event_number)
    upcoming_schedule = db((db.events.completed==False) & (db.events.ready==False) & (db.events.playing==False) & (db.events.season == 2022)).select(orderby=db.events.event_number)
    return locals()

@auth.requires_login()
def results():
    event_info = db(db.events.id == (request.args(0))).select()
    event_logo_url = URL('static', 'images/' + event_info[0].logo)
    course_img_url = URL('static', 'images/' + event_info[0].course_img)
    wide_logos = [21, 24, 27, 31, 32, 36] # list of event ids that have tournaments with wider logos
    rows = db(db.picks.event_id == (request.args(0))).select(orderby=~db.picks.total_points)
    n = 1
    p = -1
    place = 1
    winnings = {1:100, 2:70, 3:45, 4:35, 5:25, 6:20, 7:15}
    _lastpaid = 7 # last key of winnings dictionary
    same_as_last = False
    current_winnings = winnings[1]
    return locals()

@auth.requires_login()
def pick_sheet():
    event_id = (request.args(0))
    # Selecting all picks for the corresponding event
    picks = db(db.picks.event_id==event_id).select(orderby=db.picks.one_name)
    # Selecting event information for corresponding event
    event_info = db(db.events.id==event_id).select()
    event_logo_url = URL('static', 'images/' + event_info[0].logo)
    course_img_url = URL('static', 'images/' + event_info[0].course_img)
    wide_logos = [21, 24, 27, 31, 32, 36] # list of event ids that have tournaments with wider logos
    return locals()
