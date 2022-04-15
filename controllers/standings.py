@auth.requires_login()
def index():
    standings = []

    rows = db((db.auth_user.league == 27) & (db.auth_user.is_active == True)).select(orderby=~db.auth_user.season_points)
    rows_2021 = db((db.auth_user.league == 27) & (db.auth_user.twenty_one_points > 0)).select(orderby=~db.auth_user.twenty_one_points)
    year_dict = {
        "2022": [rows, "season_points"],
        "2021": [rows_2021, "twenty_one_points"]
        }

    selected_year = rows
    selected_points = "season_points"

    def build_standings():
        n = 1
        p = -1
        place = 1

        for user in selected_year:
            user_dict = {"id": user.id}
            # Check to see if it's the first player
            if user == selected_year[0]:
                # If the total points are equal to the next player a "T" is added to the placement
                if user[selected_points] > selected_year[n][selected_points]:
                    user_dict["place"] = place
                else:
                    user_dict["place"] = "T" + str(place)
            # Check to see if it's the last player
            elif user == selected_year[len(selected_year) - 1]:
                # If the total points are equal to the previous player no placement is needed
                if user[selected_points] == selected_year[p][selected_points]:
                    user_dict["place"] = ""
                else:
                    user_dict["place"] = place
            # Any other player is checked against previous and next place to assign placement
            else:
                if user[selected_points] == selected_year[p][selected_points]:
                    user_dict["place"] = ""
                elif user[selected_points] == selected_year[n][selected_points]:
                    user_dict["place"] = "T" + str(place)
                else:
                    user_dict["place"] = place
            # Add name & points
            user_dict["fname"] = user.first_name
            user_dict["lname"] = user.last_name[0]
            user_dict["points"] = user[selected_points]
            n += 1
            p += 1
            place += 1
            standings.append(user_dict)

    build_standings()

    form = FORM(SELECT('2022', '2021', value='2022', _name='year'), INPUT(_type="submit", _value="Update"))
    if form.process(keepvalues=True).accepted:
        selected_year = year_dict[form.vars.year][0]
        selected_points = year_dict[form.vars.year][1]
        standings = []
        build_standings()
    return locals()
