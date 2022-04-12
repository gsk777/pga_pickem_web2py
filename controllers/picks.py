def index():
    redirect(URL(c='default', f='index'))

def check_first_pick(form): #checking to see if the first pick selected has already been used by the user this season
    first_pick = form.vars.pick_one
    for row in db(db.tier_one_field.id==first_pick).select():
        player = row.player_name
    top_ten_picks = current.auth_user.top_ten_picks
    event = db(db.events.id==form.vars.event_id).select()
    event_num = event[0].event_number
    # checking if current user has already submitted picks for this event
    submitted_picks = db(db.picks.event_id==form.vars.event_id).select()
    user_submitted = []
    for picks in submitted_picks:
        user_submitted.append(picks.user_id)
    if current.auth_user.id in user_submitted:
        form.errors.pick_one = 'Picks already submitted. Return to SCHEDULE page to delete and reselect.'
    if player in top_ten_picks[0:event_num]:
        form.errors.pick_one = 'Player already used as top 10 pick this year.'
    if form.vars.pick_two == form.vars.pick_three:
        form.errors.pick_three = 'Duplicate pick. Please select another player.'
    if form.vars.pick_four == form.vars.pick_five:
        form.errors.pick_five = 'Duplicate pick. Please select another player.'

@auth.requires_login()
def submit_picks():
    form = SQLFORM(db.picks,
                   showid=False,
                   labels={'user_id':'User',
                           'event_id':'Event',
                           'pick_one':'1-10',
                           'pick_two':'11-50',
                           'pick_three':'11-50',
                           'pick_four':'51+',
                           'pick_five':'51+'}
                   )
    form.vars.user_id=current.auth_user.id
    form.vars.event_id=(request.args(0))
    if form.process(onvalidation=check_first_pick).accepted:
        first_pick = form.vars.pick_one
        second_pick = form.vars.pick_two
        third_pick = form.vars.pick_three
        fourth_pick = form.vars.pick_four
        fifth_pick = form.vars.pick_five
        # Adding first pick to top ten picks list of current user
        for row in db(db.tier_one_field.id==first_pick).select():
            player = row.player_name
        event = db(db.events.id==form.vars.event_id).select()
        event_num = event[0].event_number
        db(db.auth_user.id == current.auth_user.id).update(top_ten_picks = current.auth_user.top_ten_picks[0:event_num] + [player])
        # Adding names to picks so they aren't lost when tier lists are refreshed
        db(db.picks.id == form.vars.id).update(one_name = player)
        #pick2
        for row in db(db.tier_two_field.id==second_pick).select():
            player = row.player_name
        db(db.picks.id == form.vars.id).update(two_name = player)
        #pick3
        for row in db(db.tier_two_field.id==third_pick).select():
            player = row.player_name
        db(db.picks.id == form.vars.id).update(three_name = player)
        #pick4
        for row in db(db.tier_three_field.id==fourth_pick).select():
            player = row.player_name
        db(db.picks.id == form.vars.id).update(four_name = player)
        #pick5
        for row in db(db.tier_three_field.id==fifth_pick).select():
            player = row.player_name
        db(db.picks.id == form.vars.id).update(five_name = player)
        redirect(URL('picks_accepted' + '/' + str(form.vars.id)))
    else:
        response.flash = 'submit your picks'
    return dict(form=form)

@auth.requires_login()
def picks_accepted():
    message = 'Thanks!'
    picks = db(db.picks.id == request.args(0)).select()
    picks_owner_id = picks[0].user_id
    if current.auth_user.id != picks_owner_id: # prevents users from accessing other picks
        redirect(URL(c='default', f='index'))
    return locals()

@auth.requires_login()
def delete_picks():
    picks = db(db.picks.id == request.args(0)).select()
    picks_event_id = picks[0].event_id
    event = db(db.events.id == picks_event_id).select()
    number_of_events = event[0].event_number
    db(db.picks.id==request.args(0)).delete()
    db(db.auth_user.id == current.auth_user.id).update(top_ten_picks = current.auth_user.top_ten_picks[0:(number_of_events)])
    redirect(URL(c='schedule', f='view'))
    return locals()

@auth.requires_membership('admin')
def add_points():
    event = 33   #db.events.id
    picks = db(db.picks.event_id==event).select() #selects all picks from given event
    points_dict = {'Scottie Scheffler': 150, 'Rory McIlroy': 100, 'Shane Lowry': 90, 'Cameron Smith': 90, 'Collin Morikawa': 75, 'Will Zalatoris': 70, 'Corey Conners': 70,
                    'Sungjae Im': 60, 'Justin Thomas': 60, 'Charl Schwartzel': 50, 'Cameron Champ': 50, 'Danny Willett': 25, 'Dustin Johnson': 25, 'Tommy Fleetwood': 25,
                    'Jason Kokrak': 25, 'Lee Westwood': 25, 'Kevin Na': 25, 'Harry Higgs': 25, 'Min Woo Lee': 25, 'Hideki Matsuyama': 25, 'Matt Fitzpatrick': 25,
                    'Talor Gooch': 25, 'J.J. Spaun': 25, 'Sergio Garcia': 25, 'Harold Varner III': 25, 'Robert MacIntyre': 25, 'Seamus Power': 15, 'Viktor Hovland': 15,
                    'Jon Rahm': 15, 'Sepp Straka': 15, 'Russell Henley': 15, 'Hudson Swafford': 15, 'Lucas Glover': 15, 'Marc Leishman': 15, 'Tony Finau': 15,
                    'Webb Simpson': 15, 'Patrick Reed': 15, 'Joaquin Niemann': 15, 'Patrick Cantlay': 15, 'Siwoo Kim': 15, 'Tom Hoge': 15, 'Bubba Watson': 15,
                    'Billy Horschel': 15, 'Kevin Kisner': 15, 'Christiaan Bezuidenhout': 15, 'Cameron Davis': 15, 'Tiger Woods': 15, 'Adam Scott': 15, 'Max Homa': 15,
                    'Daniel Berger': 15, 'Mackenzie Hughes': 15, 'Tyrrell Hatton': 5, 'Sam Burns': 0, 'Takumi Kanaya': 0, 'Zach Johnson': 0, 'Padraig Harrington': 0,
                    'Brian Harman': 0, 'Kyoung-Hoon Lee': 0, 'Jordan Spieth': 0, 'Brooks Koepka': 0, 'Lucas Herbert': 0, 'Ryan Palmer': 0, 'Mike Weir': 0,
                    'Abraham Ancer': 0, 'Xander Schauffele': 0, 'Keita Nakajima': 0, 'Stewart Cink': 0, 'Austin Greaser': 0, 'Guido Migliozzi': 0, 'Erik van Rooyen': 0,
                    'Justin Rose': 0, 'Francesco Molinari': 0, 'Luke List': 0, 'Bernhard Langer': 0, 'Gary Woodland': 0, 'Fred Couples': 0, 'Cameron Young': 0,
                    'Larry Mize': 0, 'Garrick Higgo': 0, 'James Piot': 0, 'Aaron Jarvis': 0, 'Bryson DeChambeau': 0, 'Sandy Lyle': 0, 'Vijay Singh': 0, 'Thomas Pieters': 0,
                    'Matthew Wolff': 0, 'Stewart Hagestad': 0, 'Jose Maria Olazabal': 0, 'Laird Shepherd': 0, 'Louis Oosthuizen': 0}
    for player in picks:
        p1 = points_dict[player.one_name]
        p2 = points_dict[player.two_name]
        p3 = points_dict[player.three_name]
        p4 = points_dict[player.four_name]
        p5 = points_dict[player.five_name]
        total = p1 + p2 + p3 + p4 + p5       #totals the points of all five picks
        user = player.user_id
        db(db.picks.id == player.id).update(one_points = p1,       #Updates the picks with the point totals
                                            two_points = p2,
                                            three_points = p3,
                                            four_points = p4,
                                            five_points = p5,
                                            total_points = total)
        for row in db(db.auth_user.id==user).select(): #looks up the previous total of the user's season points and adds the current event's total
            weekly_total = total
            previous_total = row.season_points
            db(db.auth_user.id==user).update(season_points = (previous_total + weekly_total))
    redirect(URL(c='admin', f='index', args=['points_added']))

@auth.requires_membership('admin')
def status():
    try:
#---Find events.id of current event accepting picks
        current_event = db(db.events.ready==True).select()
        current_event_id = current_event[0].id
#---Finds all memberships to league group and creates a list of their user_id's
        league_list = []
        rows = db(db.auth_membership.group_id==27).select()
        for x in rows:
            user = x.user_id
            for row in db(db.auth_user.id==user).select():
                if row.is_active == True:
                    league_list.append(x.user_id)
#---Finds all submitted picks and creates a list of their user_id's
        picks_list = []
        submitted_picks = db(db.picks.event_id==current_event_id).select()
        for x in submitted_picks:
            picks_list.append(x.user_id)
#---Compares membership list with submitted picks list. Creates list of users missing picks
        missing_list = []
        for x in league_list:
            if x not in picks_list:
                user = db(db.auth_user.id==x).select()
                name = (user[0].first_name) + " " + (user[0].last_name)
                missing_list.append(name)
        return locals()
    except IndexError:
        redirect(URL(c='admin', f='index', args=['picks_status_error']))
