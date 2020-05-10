from app import app as app
from db import db
# from models.user import UserModel, Role

db.init_app(app)

# def create_users():
#     db.create_all()
#     admin_role = Role.find_or_create_role('admin', u'Admin')
#     member_role = Role.find_or_create_role('member', u'Member')
#     #Create 'member@example.com' user with no roles
#     user = UserModel.find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
#     # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
#     user = UserModel.find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1', member_role)
#     db.session.commit()

@app.before_first_request
def create_tables():
    db.create_all()
    # create_users()
