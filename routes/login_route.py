from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_user
from models.form.admin_login_form import AdminLoginForm
from werkzeug.security import check_password_hash
from config import Config
from services.admin_login_services import admin_exists
from models.users import Users



def login_route(app):
    @app.route("/login")
    def login():
        return render_template("login.html", admin_form=AdminLoginForm())
    
    @app.route("/login/admin", methods=["POST"])
    def login_admin():
        form = AdminLoginForm()

        print(f"Login attempt with email: {form.email.data}")  # Debugging
        print(f"Expected admin email: {Config.ADMIN_EMAIL}")   # Debugging

        if form.email.data == Config.ADMIN_EMAIL and check_password_hash(Config.ADMIN_PASSWORD_HASH, form.password.data):
            
            print("Main admin credentials matched!")

            admin_user = Users(
            id = 0,
            name = Config.ADMIN_NAME,
            last_name = Config.ADMIN_LAST_NAME,
            email = Config.ADMIN_EMAIL,
            password = Config.ADMIN_PASSWORD_HASH,
            role = Config.ADMIN_ROLE
            )
            login_user(admin_user)

            login_result = login_user(admin_user)
            print(f"Login result: {login_result}")

            return redirect(url_for("panel_superadmin"))
        admin = admin_exists(form.email.data, form.password.data)
        if admin:
            login_user(admin)
            return redirect(url_for("panel_admin"))
        flash("Neteisingas el. paštas arba slaptažodis", category="admin_login")
        return redirect(url_for("login"))
    

   

        



    
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# kodas apibrėžia Flask aplikacijos prisijungimo funkcionalumą. Funkcija login_route užregistruoja "/login" URL maršrutą,
# kuris priima GET ir POST užklausas. Kai puslapis užkraunamas, sukuriamas AdminLoginForm objektas. Jei forma pateikiama (POST metodas)
# ir praeina validaciją, kodas išgauna vartotojo įvestą el. paštą bei slaptažodį ir patikrina, ar jie atitinka hardkodintus administratoriaus 
# duomenis, kurie saugomi konfigūracijos faile. Tikrinimui naudojama check_password_hash funkcija, kuri saugiai palygina įvestą slaptažodį su 
# užhashintu administratoriaus slaptažodžiu. Sėkmingo prisijungimo atveju nustatomos sesijos reikšmės, nurodančios, kad vartotojas yra prisijungęs
# kaip administratorius, ir vartotojas nukreipiamas į administratoriaus valdymo skydelį. Jei vartotojas nepraeina autentifikacijos, grąžinamas 
# prisijungimo šablonas su forma.
