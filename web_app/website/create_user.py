from . import db
from .models import User



# Maybe a new permission lvl where someone can add a new user
def create_user(username, password, phy_cfg, release_date, perm_lvl):
    # TODO: input checks
    
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'), phy_cfg=phy_cfg, release_date=release_date, perm_lvl=perm_lvl)
    db.session.add(new_user)   
    db.session.commit()
    