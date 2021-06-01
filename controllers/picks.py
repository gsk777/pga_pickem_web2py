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
    event = 29   #db.events.id
    picks = db(db.picks.event_id==event).select() #selects all picks from given event
    points_dict = {'Phil Mickelson': 125, 'Louis Oosthuizen': 75, 'Brooks Koepka': 75, 'Harry Higgs': 75, 'Paul Casey': 75,
                    'Padraig Harrington': 75, 'Shane Lowry': 75, 'Rickie Fowler': 50, 'Tony Finau': 50, 'Justin Rose': 50,
                    'Kevin Streelman': 50, 'Abraham Ancer': 50, 'Scottie Scheffler': 50, 'Jon Rahm': 50, 'Will Zalatoris': 50,
                    'Collin Morikawa': 50, 'Aaron Wise': 25, 'Patrick Reed': 25, 'Sungjae Im': 25, 'Corey Conners': 25,
                    'Charley Hoffman': 25, 'Keegan Bradley': 25, 'Hideki Matsuyama': 25, 'Billy Horschel': 25, 'Jason Scrivener': 25,
                    'Martin Laird': 25, 'Matthew Fitzpatrick': 25, 'Patrick Cantlay': 25, 'Chan Kim': 25, 'Jordan Spieth': 15,
                    'Joaquin Niemann': 15, 'Christiaan Bezuidenhout': 15, 'Viktor Hovland': 15, 'Webb Simpson': 15, 'Stewart Cink': 15,
                    'Matt Jones': 15, 'Ian Poulter': 15, 'Branden Grace': 15, 'Emiliano Grillo': 15, 'Gary Woodland': 15,
                    'Richy Werenski': 15, 'Bryson DeChambeau': 15, 'Tyrrell Hatton': 15, 'Daniel van Tonder': 15, 'Talor Gooch': 15,
                    'Jason Day': 15, 'Steve Stricker': 15, 'Benjamin Cook': 15, 'Rory McIlroy': 15, 'Jason Kokrak': 15,
                    'Sam Horsfield': 15, 'Robert MacIntyre': 15, 'Harold Varner III': 15, 'Byeong Hun An': 15, 'Joel Dahmen': 5,
                    'Carlos Ortiz': 5, 'Matt Wallace': 5, 'Alex Noren': 5, 'Denny McCarthy': 5, 'Cameron Smith': 5, 'Dean Burmester': 5,
                    'Robert Streb': 5, 'Cameron Davis': 5, 'Tom Hoge': 5, 'Harris English': 5, 'Jimmy Walker': 5, 'Danny Willett': 5,
                    'Adam Hadwin': 5, 'Henrik Stenson': 5, 'Garrick Higgo': 5, 'Lee Westwood': 5, 'Russell Henley': 5, 'Tom Lewis': 5,
                    'Lucas Herbert': 5, 'Daniel Berger': 5, 'Wyndham Clark': 5, 'Brendan Steele': 5, 'Brad Marek': 5, 'Rasmus Hojgaard': 5,
                    'Bubba Watson': 5, 'Brian Gay': 5, 'Sergio Garcia': 0, 'Adam Scott': 0, 'Marc Leishman': 0, 'Brian Harman': 0,
                    'Chez Reavie': 0, 'Dustin Johnson': 0, 'Justin Thomas': 0, 'Xander Schauffele': 0, 'Victor Perez': 0,
                    'Antoine Rozner': 0, 'Mackenzie Hughes': 0, 'Andy Sullivan': 0, 'Peter Malnati': 0, 'Rich Beem': 0, 'Brendon Todd': 0,
                    'Tommy Fleetwood': 0, 'Sebastian J Munoz': 0, 'Maverick McNealy': 0, 'Siwoo Kim': 0, 'Thomas Detry': 0,
                    'Zach Johnson': 0, 'Ryan Palmer': 0, 'Martin Kaymer': 0, 'Jason Dufner': 0, 'Chris Kirk': 0, 'Dylan Frittelli': 0,
                    'Cameron Tringale': 0, 'Lanto Griffin': 0, 'Daniel Balin': 0, 'Bernd Wiesberger': 0, 'Jim Herman': 0,
                    'J.T. Poston': 0, 'Erik van Rooyen': 0, 'Hudson Swafford': 0, 'Greg Koch': 0, 'Matt Kuchar': 0, 'George Coetzee': 0,
                    'Kalle Samooja': 0, 'Kevin Kisner': 0, 'Sami Valimaki': 0, 'Kurt Kitayama': 0, 'John Catlin': 0, 'Max Homa': 0,
                    'Adam Long': 0, 'Brett Walker': 0, 'Charl Schwartzel': 0, 'K.H. Lee': 0, 'Pete Ballo': 0, 'Benjamin Polland': 0,
                    'Mark Geddes': 0, 'Aaron Rai': 0, 'Tim Pearce': 0, 'Kevin Na': 0, 'Rob Labritz': 0, 'Brandon Hagy': 0,
                    'Jazz Janewattananond': 0, 'Y.E. Yang': 0, 'Stuart Smith': 0, 'Cameron Champ': 0, 'Rikuya Hoshino': 0,
                    'Thomas Pieters': 0, 'Shaun Micheel': 0, 'Alexander Beach': 0, 'Takumi Kanaya': 0, 'Brandon Stone': 0,
                    'Patrick Rada': 0, 'Sonny Skinner': 0, 'Larkin Gross': 0, 'Omar Uresti': 0, 'Frank Bensel, Jr': 0, 'Joe Summerhays': 0,
                    'Derek Holmes': 0, 'Tyler Collet': 0, 'John Daly': 0, 'Sam Burns': 0}
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
