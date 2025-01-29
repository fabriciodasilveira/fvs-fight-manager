# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    permissions = db.relationship('Permission', backref='user', lazy=True, cascade='all, delete-orphan')

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Invalid email address')
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        if phone and not re.match(r"^\+?1?\d{9,15}$", phone):
            raise ValueError('Invalid phone number')
        return phone

    def set_password(self, password):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, module, action):
        permission = Permission.query.filter_by(
            user_id=self.id,
            module_name=module
        ).first()
        if not permission:
            return False
        return getattr(permission, f'can_{action}', False)

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    mother_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    guardian_name = db.Column(db.String(120))
    guardian_phone = db.Column(db.String(20))
    guardian_email = db.Column(db.String(120))
    medical_info = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    photo_path = db.Column(db.String(255))
    
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    personal_bookings = db.relationship('PersonalBooking', backref='student', lazy=True)

    @validates('email')
    def validate_email(self, key, email):
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Invalid email address')
        return email

    @validates('birth_date')
    def validate_birth_date(self, key, birth_date):
        if (datetime.now().date() - birth_date).days < 0:
            raise ValueError('Birth date cannot be in the future')
        return birth_date

    def age(self):
        today = datetime.now().date()
        return (today - self.birth_date).days // 365

    def needs_guardian(self):
        return self.age() < 18

class MartialArt(db.Model):
    __tablename__ = 'martial_arts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    
    teachers = db.relationship('Teacher', backref='martial_art', lazy=True)
    classes = db.relationship('Class', backref='martial_art', lazy=True)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    mother_name = db.Column(db.String(120))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String(200))
    martial_art_id = db.Column(db.Integer, db.ForeignKey('martial_arts.id'))
    certification = db.Column(db.String(100))
    bio = db.Column(db.Text)
    photo_path = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    commission_rate = db.Column(db.Float, default=0.0)
    
    classes = db.relationship('Class', backref='teacher', lazy=True)
    personal_bookings = db.relationship('PersonalBooking', backref='teacher', lazy=True)

class Class(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    martial_art_id = db.Column(db.Integer, db.ForeignKey('martial_arts.id'))
    capacity = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    schedule = db.relationship('Schedule', backref='class', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='class', lazy=True)

    def current_enrollment_count(self):
        return Enrollment.query.filter_by(
            class_id=self.id,
            active=True
        ).count()

    def has_capacity(self):
        if not self.capacity:
            return True
        return self.current_enrollment_count() < self.capacity

class Plan(db.Model):
    __tablename__ = 'plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(20), nullable=False)  # 'monthly', 'quarterly', 'semiannual', 'annual'
    classes_per_week = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    enrollments = db.relationship('Enrollment', backref='plan', lazy=True)

    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError('Price must be greater than 0')
        return price

    def duration_in_months(self):
        durations = {
            'monthly': 1,
            'quarterly': 3,
            'semiannual': 6,
            'annual': 12
        }
        return durations.get(self.duration, 0)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, default=True)
    
    payments = db.relationship('Payment', backref='enrollment', lazy=True)

    def generate_next_payment(self):
        """Gera o próximo pagamento baseado no plano"""
        last_payment = Payment.query.filter_by(
            enrollment_id=self.id
        ).order_by(Payment.due_date.desc()).first()

        if not last_payment:
            due_date = self.start_date
        else:
            # Calcula próximo vencimento baseado no último pagamento
            due_date = last_payment.due_date + relativedelta(months=1)

        if due_date > self.end_date:
            return None

        return Payment(
            enrollment_id=self.id,
            amount=self.plan.price,
            due_date=due_date,
            status='pending'
        )

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'))
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(20))  # 'pix', 'credit_card'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'paid', 'overdue', 'cancelled'
    transaction_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def mark_as_paid(self, payment_method, transaction_id=None):
        self.status = 'paid'
        self.payment_date = datetime.utcnow()
        self.payment_method = payment_method
        self.transaction_id = transaction_id

    def is_overdue(self):
        return self.status == 'pending' and datetime.now().date() > self.due_date

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'paid'
    category = db.Column(db.String(50))
    recurring = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    attachments = db.relationship('ExpenseAttachment', backref='expense', lazy=True)

class ExpenseAttachment(db.Model):
    __tablename__ = 'expense_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'))
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Schedule(db.Model):
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    day_of_week = db.Column(db.Integer)  # 0-6 (Segunda-Domingo)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(50))
    
    @validates('start_time', 'end_time')
    def validate_times(self, key, value):
        if key == 'end_time' and value <= self.start_time:
            raise ValueError('End time must be after start time')
        return value

    def has_conflict(self, other_schedule):
        """Verifica se há conflito com outro horário"""
        if self.day_of_week != other_schedule.day_of_week:
            return False
        
        return not (self.end_time <= other_schedule.start_time or 
                   self.start_time >= other_schedule.end_time)

class PersonalBooking(db.Model):
    __tablename__ = 'personal_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'cancelled'
    price = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    payment = db.relationship('Payment', backref='personal_booking', lazy=True, uselist=False)

    def confirm(self):
        if self.status == 'pending':
            self.status = 'confirmed'
            # Criar pagamento associado
            payment = Payment(
                amount=self.price,
                due_date=self.date,
                status='pending'
            )
            self.payment = payment
            return True
        return False
    
class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    module_name = db.Column(db.String(50), nullable=False)
    can_view = db.Column(db.Boolean, default=False)
    can_create = db.Column(db.Boolean, default=False)
    can_edit = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Permission {self.module_name}>'

    @staticmethod
    def create_default_permissions(user_id):
        """Cria permissões padrão para um novo usuário"""
        default_modules = [
            'dashboard',
            'students',
            'teachers',
            'classes',
            'plans',
            'payments',
            'expenses',
            'reports',
            'schedule'
        ]
        
        permissions = []
        for module in default_modules:
            perm = Permission(
                user_id=user_id,
                module_name=module,
                can_view=True,
                can_create=False,
                can_edit=False,
                can_delete=False
            )
            permissions.append(perm)
        
        return permissions