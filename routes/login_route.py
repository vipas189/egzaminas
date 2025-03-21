from flask import render_template, redirect, url_for, request, session
from models.form.admin_login_form import AdminLoginForm
from werkzeug.security import check_password_hash
from config import Config
from database import Session, engine


def login_route(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = AdminLoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                email = form.email.data
                password = form.password.data
                if email == Config.ADMIN_EMAIL and check_password_hash(Config.ADMIN_PASSWORD_HASH, password):
                    session['logged_in'] = True
                    session['admin'] = True
                    return redirect(url_for("panel_admin"))
                
                # with Session() as session:
                #     result = session.execute(select(Admin).filter_by)
                #     result = session.execute(text("SELECT * FROM admin WHERE email = :email"),{"email": email})
                #     admin_from_db = result.fetchone()
                    
                #     # Jei admin rastas ir slaptažodis atitinka
                #     if admin_from_db and check_password_hash(admin_from_db.password, password):
                #         session['logged_in'] = True
                #         session['admin'] = True
                #         session['admin_id'] = admin_from_db.id
                #         session['admin_type'] = 'db'
                #         return redirect(url_for("panel_admin"))
            return redirect(url_for("login")) #esant jau panel_admin ir norint grįžt atgal į /login, meta ne klaidą, o atgal grįžta į /login
        return render_template('login.html',form = form)
    
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# kodas apibrėžia Flask aplikacijos prisijungimo funkcionalumą. Funkcija login_route užregistruoja "/login" URL maršrutą,
# kuris priima GET ir POST užklausas. Kai puslapis užkraunamas, sukuriamas AdminLoginForm objektas. Jei forma pateikiama (POST metodas)
# ir praeina validaciją, kodas išgauna vartotojo įvestą el. paštą bei slaptažodį ir patikrina, ar jie atitinka hardkodintus administratoriaus 
# duomenis, kurie saugomi konfigūracijos faile. Tikrinimui naudojama check_password_hash funkcija, kuri saugiai palygina įvestą slaptažodį su 
# užhashintu administratoriaus slaptažodžiu. Sėkmingo prisijungimo atveju nustatomos sesijos reikšmės, nurodančios, kad vartotojas yra prisijungęs
# kaip administratorius, ir vartotojas nukreipiamas į administratoriaus valdymo skydelį. Jei vartotojas nepraeina autentifikacijos, grąžinamas 
# prisijungimo šablonas su forma.
