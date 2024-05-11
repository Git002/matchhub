from models import db, EmployeeTable
import bcrypt


def generate_password_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")


def check_login_credentials(username, password):
    emp = EmployeeTable.query.filter_by(username=username).first()

    if not emp:
        return False

    if bcrypt.checkpw(password.encode("utf-8"), emp.password.encode("utf-8")):
        return True
    else:
        return False


def check_username(username):
    emp = EmployeeTable.query.filter_by(username=username).first()
    if emp:
        return True
    else:
        return False


def employee_exists(emp_id):
    emp = EmployeeTable.query.filter_by(emp_id=emp_id).first()
    if emp:
        return True
    else:
        return False


class Helper:
    def __init__(self, flask_instance):
        self.flask_instance = flask_instance

    def is_table_empty(self):
        with self.flask_instance.app_context():
            if db.session.query(EmployeeTable).count() == 0:
                return True
            else:
                return False

    def add_dummy_user(self):
        hashed_password = generate_password_hash("123456")

        with self.flask_instance.app_context():
            db.session.add(
                EmployeeTable(
                    emp_id=100,
                    username="admin",
                    password=hashed_password,
                    role="admin",
                    first_name="admin",
                    last_name="",
                )
            )
            db.session.commit()
