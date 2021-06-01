def index():
    redirect(URL('display'))
    return locals()

@auth.requires_membership('admin')
def display(): # shows currently loaded fields
    field = db(db.tier_one_field).select(orderby=db.tier_one_field.player_rank)
    field2 = db(db.tier_two_field).select(orderby=db.tier_two_field.player_rank)
    field3 = db(db.tier_three_field).select(orderby=db.tier_three_field.player_rank)
    return locals()

@auth.requires_membership('admin')
def update(): # updates current field DBs (tier one, tier two, tier three)
    top_ten = {'Dustin Johnson': '001', 'Justin Thomas': '002', 'Jon Rahm': '003', 'Xander Schauffele': '004', 'Bryson DeChambeau': '005',
                'Collin Morikawa': '006', 'Rory McIlroy': '007', 'Patrick Reed': '008', 'Tyrrell Hatton': '009', 'Webb Simpson': '010'}
    for player, rank in top_ten.items():
        db.tier_one_field.insert(player_name=player, player_rank=rank)

    eleven_to_fifty = {'Viktor Hovland': '011', 'Patrick Cantlay': '012', 'Brooks Koepka': '013', 'Tony Finau': '014',
                        'Hideki Matsuyama': '015', 'Daniel Berger': '016', 'Matthew Fitzpatrick': '017', 'Billy Horschel': '018',
                        'Abraham Ancer': '019', 'Paul Casey': '020', 'Lee Westwood': '021', 'Harris English': '022', 'Sungjae Im': '023',
                        'Scottie Scheffler': '024', 'Cameron Smith': '025', 'Jordan Spieth': '026', 'Tommy Fleetwood': '028',
                        'Joaquin Niemann': '029', 'Will Zalatoris': '030', 'Louis Oosthuizen': '031', 'Ryan Palmer': '032',
                        'Victor Perez': '033', 'Kevin Na': '034', 'Jason Kokrak': '035', 'Sam Burns': '036', 'Marc Leishman': '037',
                        'Adam Scott': '038', 'Corey Conners': '039', 'Max Homa': '040', 'Christiaan Bezuidenhout': '041',
                        'Justin Rose': '042', 'Stewart Cink': '043', 'Kevin Kisner': '044', 'Robert MacIntyre': '045',
                        'Sergio Garcia': '046', 'Brian Harman': '047', 'Shane Lowry': '048', 'Matt Kuchar': '049', 'Siwoo Kim': '050'}
    for player, rank in eleven_to_fifty.items():
        db.tier_two_field.insert(player_name=player, player_rank=rank)

    fiftyone_and_up = {'Garrick Higgo': '051', 'Matt Wallace': '052', 'Gary Woodland': '053', 'Carlos Ortiz': '054', 'Bubba Watson': '055',
                        'Matt Jones': '056', 'Russell Henley': '057', 'Mackenzie Hughes': '058', 'K.H. Lee': '059', 'Brendon Todd': '060',
                        'Lanto Griffin': '061', 'Bernd Wiesberger': '062', 'Chris Kirk': '063', 'Kevin Streelman': '064', 'Jason Day': '065',
                        'Cameron Tringale': '066', 'Ian Poulter': '067', 'Joel Dahmen': '068', 'Rikuya Hoshino': '069', 'Andy Sullivan': '070',
                        'Sebastian J Munoz': '071', 'Talor Gooch': '072', 'Keegan Bradley': '073', 'Antoine Rozner': '074',
                        'Charley Hoffman': '075', 'Emiliano Grillo': '076', 'Takumi Kanaya': '077', 'Erik van Rooyen': '078',
                        'Daniel van Tonder': '079', 'John Catlin': '080', 'Dylan Frittelli': '081', 'Brendan Steele': '082',
                        'Chan Kim': '083', 'Harold Varner III': '084', 'Adam Long': '085', 'Sam Horsfield': '086', 'Brandon Stone': '087',
                        'J.T. Poston': '088', 'Dean Burmester': '089', 'Aaron Rai': '090', 'Danny Willett': '091', 'Branden Grace': '092',
                        'Martin Kaymer': '093', 'Thomas Pieters': '094', 'Cameron Champ': '095', 'George Coetzee': '096',
                        'Lucas Herbert': '097', 'Thomas Detry': '098', 'Alex Noren': '099', 'Sami Valimaki': '100', 'Martin Laird': '101',
                        'Rasmus Hojgaard': '102', 'Maverick McNealy': '104', 'Kurt Kitayama': '106', 'Adam Hadwin': '107',
                        'Charl Schwartzel': '109', 'Jazz Janewattananond': '111', 'Kalle Samooja': '112', 'Tom Hoge': '113',
                        'Richy Werenski': '114', 'Phil Mickelson': '115', 'Tom Lewis': '116', 'Chez Reavie': '117', 'Jason Scrivener': '118',
                        'Byeong Hun An': '119', 'Zach Johnson': '121', 'Robert Streb': '125', 'Cameron Davis': '127', 'Rickie Fowler': '128',
                        'Henrik Stenson': '130', 'Aaron Wise': '136', 'Jim Herman': '143', 'Francesco Molinari': '144', 'Wyndham Clark': '150'}
    for player, rank in fiftyone_and_up.items():
        db.tier_three_field.insert(player_name=player, player_rank=rank)

    unranked = {'Frank Bensel, Jr': '999', 'Alexander Beach': '999', 'Benjamin Cook': '999', 'Benjamin Polland': '999', 'Brad Marek': '999',
                'Brett Walker': '999', 'Brian Gay': '999', 'Daniel Balin': '999', 'Denny McCarthy': '999', 'Derek Holmes': '999',
                'Greg Koch': '999', 'Harry Higgs': '999', 'Hudson Swafford': '999', 'Jason Dufner': '999', 'Jimmy Walker': '999',
                'Joe Summerhays': '999', 'John Daly': '999', 'Larkin Gross': '999', 'Mark Geddes': '999', 'Omar Uresti': '999',
                'Padraig Harrington': '999', 'Patrick Rada': '999', 'Pete Ballo': '999', 'Peter Malnati': '999', 'Rich Beem': '999',
                'Rob Labritz': '999', 'Shaun Micheel': '999', 'Sonny Skinner': '999', 'Steve Stricker': '999', 'Stuart Smith': '999',
                'Tim Pearce': '999', 'Tyler Collet': '999', 'Y.E. Yang': '999'}
    for player, rank in unranked.items():
        db.tier_three_field.insert(player_name=player, player_rank=rank)

    redirect(URL('display'))
    return locals()
