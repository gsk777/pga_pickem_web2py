@auth.requires_login()
def index():
    profile_url = URL(c='default', f='user', args=['profile'])
    schedule_url = URL(c='schedule', f='view')
    return locals()
