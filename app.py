from flask import Flask, render_template, request, redirect, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "";
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Hama@localhost:5432/examFlask"
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomU = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    mdp = db.Column(db.String)

    def set_password(self, mdp):
        self.mdp = generate_password_hash(mdp)

    def check_password(self, mdp):
        return check_password_hash(self.mdp, mdp)



class Contact(db.Model):
    idC = db.Column(db.Integer, primary_key=True)
    nomC = db.Column(db.String)
    email = db.Column(db.String)
    num = db.Column(db.String)
    idU = db.Column(db.Integer, db.ForeignKey('user.id'))




@app.route('/')
def index():
    if 'logged_in' in session:
        # L'utilisateur est connecté, récupérez les données nécessaires
        utilisateur_connecte = User.query.get(session['idU'])
        # Calculer le nombre total de contacts de l'utilisateur
        nombre_total_contacts = Contact.query.filter_by(idU=utilisateur_connecte.id).count()
        all_data = Contact.query.filter_by(idU=session["idU"]).all()
        return render_template("index.html", contact=all_data,sessionU=session,totalC=nombre_total_contacts)
    else:
        all_data = Contact.query.all()
        return redirect(url_for('signin'))


@app.route('/logout')
def logout():
    session.clear()
    flash("Vous êtes déconnecté avec succès !","success")
    return redirect(url_for('index'))


@app.route('/ajouterContact', methods=['POST'])
def ajouterContact():
    if 'logged_in' in session:

        if request.method == 'POST':
            nomC = request.form['nomC']
            email = request.form['email']
            num = request.form['num']
            idU = session["idU"]  # Récupérer l'ID de l'utilisateur à partir du formulaire

            # Vérifier si un contact avec le même numéro existe déjà
            existing_contact = Contact.query.filter_by(num=num).first()
            if existing_contact:
                flash("Un contact avec le même numéro existe déjà.", "error")
                return redirect(url_for('index'))

            new_contact = Contact(nomC=nomC, email=email, num=num, idU=idU)

            db.session.add(new_contact)
            db.session.commit()

            flash("Le contact a été ajouté avec succès.", 'success')
            return redirect(url_for('index'))

        else:
            return redirect(url_for('signin'))




@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'logged_in' not in session:

        if request.method == 'POST':
            nomU = request.form['nomU']
            mdp = request.form['mdp']

            user = User.query.filter_by(nomU=nomU).first()
            if user and user.check_password(mdp):
                # Les informations d'identification sont valides, définissez la variable de session
                session['logged_in'] = True
                session['nomU'] = user.nomU
                session['idU'] = user.id

                flash("Vous êtes connecté avec succès !", "success")
                return redirect(url_for('index'))
            else:
                flash("Identifiants invalides. Veuillez réessayer.","error")

        return render_template("signin.html")

    else:
        return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'logged_in' not in session:
        if request.method == 'POST':
            nomU = request.form['nomU']
            email = request.form['email']
            mdp = request.form['mdp']

            existing_user = User.query.filter_by(nomU=nomU).first()
            if existing_user:
                flash("Le nom d'utilisateur existe déjà.", "error")
                return redirect(url_for('signup'))

            new_user = User(nomU=nomU, email=email)
            new_user.set_password(mdp)

            db.session.add(new_user)
            db.session.commit()

            flash("Inscription réussie. Vous pouvez maintenant vous connecter.", "success")
            return redirect(url_for('signin'))

        return render_template('signup.html')
    else:
        return redirect(url_for('index'))


@app.route('/delete/<id>',methods=['GET', 'POST'])
def delete(id):
    if 'logged_in' in session:
        my_data = Contact.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("Supression Réussie", "success")
        return redirect(url_for('index'))
    else:
        return redirect(url_for('signin'))


@app.route('/editerContact',methods=['GET', 'POST'])
def editerContact():
    if 'logged_in' in session:
        if request.method == 'POST':
            idC = request.form['idC']
            nomC = request.form['nomC']
            email = request.form['email']
            num = request.form['num']
            idU = session["idU"]  # Récupérer l'ID de l'utilisateur à partir du formulaire

            # Vérifier si un contact avec le même numéro existe déjà (à l'exception du contact en cours d'édition)
            existing_contact = Contact.query.filter(Contact.num == num, Contact.idC != idC).first()
            if existing_contact:
                flash("Un autre contact avec le même numéro existe déjà.", "error")
                return redirect(url_for('index'))

            contact = Contact.query.get(idC)
            contact.nomC = nomC
            contact.email = email
            contact.num = num
            contact.idU = idU

            db.session.commit()

            flash("Le contact a été modifié avec succès.", "success")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('signin'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
