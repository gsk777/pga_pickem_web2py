@auth.requires_membership('admin')
def index(): return dict(message="hello from admin.py")

@auth.requires_membership('admin')
def end_season():
    # enter league number
    league = 23
    members = db(db.auth_user.league == league).select(orderby=~db.auth_user.season_points)
    size = len(members)
    print(size)
    place = 1
    index = 0
    for member in members:
        if member == members[0]:
            db(db.auth_user.id == member.id).update(twenty_one_points = member.season_points,
                                                    twenty_one_placement = (str(place) + '/' + str(size)))
            index += 1
        else:
            if member.season_points == members[index-1].season_points:
                db(db.auth_user.id == member.id).update(twenty_one_points = member.season_points,
                                                    twenty_one_placement = (str(place) + '/' + str(size)))
                index += 1
            else:
                place = index+1
                db(db.auth_user.id == member.id).update(twenty_one_points = member.season_points,
                                                    twenty_one_placement = (str(place) + '/' + str(size)))
                index += 1
    return locals()

@auth.requires_membership('admin')
def clear_season_points():
    # enter league number
    league = 23
    for member in db(db.auth_user.league == league).select():
        db(db.auth_user.id == member.id).update(season_points = 0)
    return locals()

@auth.requires_membership('admin')
def clear_topten_picks():
    # enter league number
    league = 27
    for member in db(db.auth_user.league == league).select():
        db(db.auth_user.id == member.id).update(top_ten_picks = ["Default"])
    return locals()