@auth.requires_login()
def index():
    rows = db(db.auth_user.league == 27).select(orderby=~db.auth_user.season_points)
    n = 1
    p = -1
    place = 1
    return locals()