from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__, template_folder='static/templates', static_folder='static', static_url_path='/static')
app.config.from_object(Config)

app.secret_key = 'super-secret-key-for-diploma-project'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

TRANSLATIONS = {
    'uk': {
        'brand': 'Система Студентської Активності',
        'home': 'Головна',
        'clubs': 'Гуртки',
        'my_clubs': 'Мої Гуртки',
        'admin_panel': 'Панель Адміна',
        'dashboard': 'Кабінет',
        'logout': 'Вихід',
        'login': 'Вхід',
        'register': 'Реєстрація',
        'main_title': 'Платформа Студентської Активності',
        'main_subtitle': 'Онлайн-система реєстрації в гуртки та позанавчальні секції.',
        'btn_explore': 'Оглянути гуртки',
        'welcome_msg': 'Ласкаво просимо до нашої системи. Авторизуйтесь, щоб записатися на улюблені заняття.',
        'reg_header': 'Реєстрація Студента',
        'label_name': 'Повне ім\'я',
        'label_email': 'Електронна пошта',
        'label_password': 'Пароль',
        'label_group': 'Група',
        'label_speciality': 'Спеціальність',
        'btn_reg_submit': 'Зареєструватися',
        'login_header': 'Авторизація Студента',
        'btn_login_submit': 'Увійти',
        'flash_reg_success': 'Реєстрація успішно завершена!',
        'flash_login_success': 'Вхід виконано успішно!',
        'flash_login_error': 'Невірний email або пароль.',
        'dash_welcome': 'Вітаємо',
        'dash_group': 'Група',
        'dash_speciality': 'Спеціальність',
        'dash_role': 'Роль',
        'dash_my_clubs_title': 'Мої активні гуртки та секції',
        'dash_no_clubs': 'Ви ще не записані до жодного гуртка.',
        'clubs_title': 'Студентські гуртки та секції',
        'club_teacher': 'Викладач / Тренер',
        'club_schedule': 'Розклад занять',
        'club_places': 'Вільних місць',
        'btn_join': 'Записатись у гурток',
        'btn_login_to_join': 'Увійдіть, щоб записатись',
        'admin_header': 'Створити новий гурток',
        'label_club_name': 'Назва гуртка',
        'label_description': 'Опис',
        'label_teacher': 'Викладач / Тренер',
        'label_schedule': 'Розклад',
        'label_max_members': 'Макс. кількість місць',
        'btn_create_club': 'Створити гурток',
        'admin_existing_clubs': 'Існуючі гуртки',
        'btn_edit': 'Редагувати',
        'admin_edit_header': 'Редагування гуртка',
        'btn_save_changes': 'Зберегти зміни'
    },
    'en': {
        'brand': 'Student Activities System',
        'home': 'Home',
        'clubs': 'Clubs',
        'my_clubs': 'My Clubs',
        'admin_panel': 'Admin Panel',
        'dashboard': 'Dashboard',
        'logout': 'Logout',
        'login': 'Login',
        'register': 'Register',
        'main_title': 'Student Activities Platform',
        'main_subtitle': 'Online registration system for clubs and extracurricular activities.',
        'btn_explore': 'Explore Clubs',
        'welcome_msg': 'Welcome to our system. Please log in to register for your favorite activities.',
        'reg_header': 'Student Registration',
        'label_name': 'Full Name',
        'label_email': 'Email',
        'label_password': 'Password',
        'label_group': 'Group',
        'label_speciality': 'Speciality',
        'btn_reg_submit': 'Register',
        'login_header': 'Student Login',
        'btn_login_submit': 'Login',
        'flash_reg_success': 'Registration completed successfully!',
        'flash_login_success': 'Successfully logged in!',
        'flash_login_error': 'Invalid email or password.',
        'dash_welcome': 'Welcome',
        'dash_group': 'Group',
        'dash_speciality': 'Speciality',
        'dash_role': 'Role',
        'dash_my_clubs_title': 'My Active Clubs & Sections',
        'dash_no_clubs': 'You are not registered in any clubs yet.',
        'clubs_title': 'Student Clubs & Sections',
        'club_teacher': 'Teacher / Coach',
        'club_schedule': 'Schedule',
        'club_places': 'Available places',
        'btn_join': 'Join Club',
        'btn_login_to_join': 'Login to Join',
        'admin_header': 'Create New Club',
        'label_club_name': 'Club Name',
        'label_description': 'Description',
        'label_teacher': 'Teacher / Coach',
        'label_schedule': 'Schedule',
        'label_max_members': 'Max Members',
        'btn_create_club': 'Create Club',
        'admin_existing_clubs': 'Existing Clubs',
        'btn_edit': 'Edit',
        'admin_edit_header': 'Edit Club',
        'btn_save_changes': 'Save Changes'
    }
}

@app.context_processor
def inject_lang():
    lang = session.get('lang', 'uk')
    return dict(lang=lang, text=TRANSLATIONS[lang])

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['uk', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

class ClubTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), unique=True)
    club_name_en = db.Column(db.String(100))
    description_en = db.Column(db.Text)
    teacher_en = db.Column(db.String(100))
    schedule_en = db.Column(db.String(100))

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    group_name = db.Column(db.String(50))
    speciality = db.Column(db.String(100))
    role = db.Column(db.String(20), default='student')

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    teacher = db.Column(db.String(100))
    schedule = db.Column(db.String(100))
    max_members = db.Column(db.Integer)

    translation = db.relationship('ClubTranslation', backref='base_club', uselist=False)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    registration_date = db.Column(db.String(100))
    status = db.Column(db.String(50))
    student = db.relationship('Student', backref='registrations')
    club = db.relationship('Club', backref='registrations')

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clubs')
def clubs():
    all_clubs = Club.query.all()
    return render_template('clubs.html', clubs=all_clubs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    current_lang = session.get('lang', 'uk')
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        group_name = request.form['group_name']
        speciality = request.form['speciality']

        new_student = Student(
            full_name=full_name,
            email=email,
            password=password,
            group_name=group_name,
            speciality=speciality,
            role='student'
        )

        db.session.add(new_student)
        db.session.commit()

        flash(TRANSLATIONS[current_lang]['flash_reg_success'])
        return redirect('/')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_lang = session.get('lang', 'uk')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        student = Student.query.filter_by(email=email).first()

        if student and check_password_hash(student.password, password):
            login_user(student)
            flash(TRANSLATIONS[current_lang]['flash_login_success'])
            return redirect(url_for('dashboard'))
        else:
            flash(TRANSLATIONS[current_lang]['flash_login_error'])

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        return redirect(url_for('home'))

    if request.method == 'POST':
        new_club = Club(
            club_name=request.form['club_name'],
            description=request.form['description'],
            teacher=request.form['teacher'],
            schedule=request.form['schedule'],
            max_members=int(request.form['max_members'])
        )
        db.session.add(new_club)
        db.session.commit()
        return redirect(url_for('admin'))

    all_clubs = Club.query.all()
    return render_template('admin.html', clubs=all_clubs)

@app.route('/admin/edit/<int:club_id>', methods=['GET', 'POST'])
@login_required
def edit_club(club_id):
    if current_user.role != 'admin':
        return redirect(url_for('home'))

    club = Club.query.get_or_404(club_id)

    if request.method == 'POST':
        club.club_name = request.form['club_name']
        club.description = request.form['description']
        club.teacher = request.form['teacher']
        club.schedule = request.form['schedule']
        club.max_members = int(request.form['max_members'])
        
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('edit_club.html', club=club)

@app.route('/register_club/<int:club_id>')
@login_required
def register_club(club_id):
    club = Club.query.get_or_404(club_id)

    registrations_count = Registration.query.filter_by(club_id=club.id).count()

    if registrations_count >= club.max_members:
        return "No available places."

    existing_registration = Registration.query.filter_by(
        student_id=current_user.id,
        club_id=club.id
    ).first()

    if existing_registration:
        return "You are already registered."

    registration = Registration(
        student_id=current_user.id,
        club_id=club.id,
        registration_date='2026',
        status='Pending'
    )

    db.session.add(registration)
    db.session.commit()

    return redirect('/my_clubs')

@app.route('/my_clubs')
@login_required
def my_clubs():
    user_registrations = Registration.query.filter_by(student_id=current_user.id).all()
    return render_template('my_clubs.html', registrations=user_registrations)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin_exists = Student.query.filter_by(email='admin@gmail.com').first()

        if not admin_exists:
            admin = Student(
                full_name='Administrator',
                email='admin@gmail.com',
                password=generate_password_hash('admin123'),
                group_name='Administration',
                speciality='System Management',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True, host='0.0.0.0', port=5000)