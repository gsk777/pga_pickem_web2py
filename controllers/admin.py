@auth.requires_membership('admin')
def index(): return dict(message="hello from admin.py")
