from models.users import Users
from extensions import db


# pavyzdys jei dirbam su home_route darom pvz: home_check_user, jei pvz: page_route darom page_check_user
# iskvieciam funkcija i ta route kuri pasirinkote: home, page ir t.t.
# isidedant home_view_users funkcija i home_route.py ja importuokite!!!
def home_view_users():
    students = db.session.execute(db.select(Users)).scalars().all()
    return students
