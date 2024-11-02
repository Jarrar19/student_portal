from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import db
from .models import User, Student

# Create a blueprint for your routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST']) 
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Input validation
        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('main.register'))
        
        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists! Please choose a different one.')
            return redirect(url_for('main.register'))

        # Create a new user
        new_user = User(username=username)
        new_user.set_password(password)  # Ensure this method hashes the password
        db.session.add(new_user)
        
        try:
            db.session.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            # Consider logging the error for debugging
            print(f'Error occurred: {e}')  # Simple logging; consider using logging module
            flash('An error occurred while registering. Please try again.')
            return redirect(url_for('main.register'))

    return render_template('register.html')  # Ensure this line is present for GET requests

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Input validation
        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('main.login'))
        
        user = User.query.filter_by(username=username).first()

        # Check for user and validate password
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('main.students'))  # Redirect to students page or dashboard
        else:
            flash('Invalid username or password. Please try again.')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@main.route('/students')
@login_required
def students():
    # Fetch all students from the database
    all_students = Student.query.all()
    return render_template('students.html', students=all_students)

@main.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        usn = request.form.get('usn')
        attendance = request.form.get('attendance')

        # Input validation
        if not name or not age or not usn or not attendance:
            flash('All fields are required.')
            return redirect(url_for('main.add_student'))

        try:
            age = int(age)  # Ensure age is an integer
            new_student = Student(name=name, age=age, usn=usn, attendance=attendance)
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!')
            return redirect(url_for('main.students'))
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            flash('An error occurred while adding the student. Please try again.')
            return redirect(url_for('main.add_student'))

    return render_template('add_student.html')

@main.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.name = request.form.get('name')
        student.age = request.form.get('age')
        student.usn = request.form.get('usn')
        student.attendance = request.form.get('attendance')

        # Input validation
        if not student.name or not student.age or not student.usn or not student.attendance:
            flash('All fields are required.')
            return redirect(url_for('main.edit_student', student_id=student.id))

        try:
            student.age = int(student.age)  # Ensure age is an integer
            db.session.commit()
            flash('Student updated successfully!')
            return redirect(url_for('main.students'))
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            flash('An error occurred while updating the student. Please try again.')
            return redirect(url_for('main.edit_student', student_id=student.id))

    return render_template('edit_student.html', student=student)

@main.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    
    try:
        db.session.commit()
        flash('Student deleted successfully!')
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        flash('An error occurred while deleting the student. Please try again.')

    return redirect(url_for('main.students'))
