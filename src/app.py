from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
import re
from datetime import datetime
from src.config import app, db
from src import database
from src.models.user import User, user_schema, users_schema
from src.models.experience import Experience, experience_schema, experiences_schema


user_params = ['first_name', 'last_name', 'city_state', 'phone_number',
               'email_address', 'password']
experience_params = ['company_name', 'position_title', 'start_date',
                     'end_date', 'description']


@app.cli.command('init_db')
def init_db():
    database.init_db()


@app.cli.command('seed_db')
def seed_db():
    database.seed_db()


@app.cli.command('drop_db')
def drop_db():
    database.drop_db()


@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(users=result)


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id: int):
    user = User.query.filter(User.id == user_id).first()
    if user:
        result = user_schema.dump(user)
        return jsonify(user=result)
    else:
        return jsonify(message=f"No User Found"), 404


@app.route('/api/user/search', methods=['GET'])
def get_user_by_email():
    user_email = request.args.get("email")
    if user_email:
        user = User.query.filter(User.email_address == user_email).first()
        if user:
            result = user_schema.dump(user)
            return jsonify(user=result)
        else:
            return jsonify(message=f"No User Found"), 404
    else:
        return jsonify(message="No Email Provided"), 400


@app.route('/api/user/<int:user_id>/experiences', methods=['GET'])
def get_user_experiences(user_id: int):
    user = User.query.filter(User.id == user_id).first()
    if user:
        experience_ids = [experience.id for experience in user.experiences]
        experiences = Experience.query.filter(
            Experience.id.in_(experience_ids)).all()
        if experiences:
            result = experiences_schema.dump(experiences)
            return jsonify(experiences=result)
        else:
            return jsonify(experiences=[])
    else:
        return jsonify(message="User Does Not Exist"), 404


@app.route('/api/user/create', methods=['POST'])
def create_user():
    if request.json:
        if valid_user_params(request.json):
            if parameters_in_request_json(request.json, user_params):
                first_name = request.json['first_name']
                last_name = request.json['last_name']
                city_state = request.json['city_state']
                phone_number = request.json['phone_number']
                email = request.json['email_address']
                password = request.json['password']
                user = User(first_name=first_name, last_name=last_name,
                            city_state=city_state, phone_number=phone_number,
                            email_address=email, password=password)
                db.session.add(user)
                db.session.commit()
                return jsonify(id=f"{request.host_url}api/user/{user.id}")
            else:
                return jsonify(message="One Or More Parameters Are Missing",
                               required_parameters=user_params), 400
        else:
            return jsonify(message="Invalid Data",
                           reasons=["Email Must Be Valid, Password Must Be "
                                    "Alphanumeric and 4-8 Characters Long"]
                           ), 400
    else:
        return jsonify(message="Request Parameters Must Be Submitted In JSON"
                       ), 400


@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id: int):
    if request.json:
        user = User.query.filter(User.id == user_id).first()
        if user:
            if valid_user_params(request.json):
                for request_parameter in user_params:
                    if request_parameter in request.json:
                        setattr(user, request_parameter,
                                request.json[request_parameter])

                        try:
                            experience_ids = request.json['experiences']
                            if not isinstance(experience_ids, list):
                                return jsonify(message="Experiences Is Not A "
                                                       "List"), 400
                            for experience_id in experience_ids:
                                if not isinstance(experience_id, int):
                                    return jsonify(
                                        message=f"Experience Ids Must Be Int"
                                                f". {experience_id} Is Not An "
                                                f"Int")
                            experiences = Experience.query.filter(
                                Experience.id.in_(experience_ids)).all()
                            user.experiences.append(experiences)
                        except KeyError:
                            pass

                        db.session.add(user)
                        db.session.commit()
                        return jsonify(id=f"{request.host_url}api/user/"
                                          f"{user.id}")
            else:
                jsonify(message="Invalid Data", reasons=["Email Must Be Valid,"
                                                         "Password Must Be"
                                                         "Alphanumeric and 4-"
                                                         "15 Characters Long"]
                        )
        else:
            jsonify(message="User does not exist"), 404
    else:
        return jsonify(message="Request Parameters Must Be Submitted In JSON"
                       ), 400


@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id: int):
    user = User.query.filter(User.id == user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return '', 204
    else:
        return jsonify(message="No User Found"), 404


@app.route('/api/experiences', methods=['GET'])
def get_all_experiences():
    experiences = Experience.query.all()
    result = experiences_schema.dump(experiences)
    return jsonify(experiences=result)


@app.route('/api/experience/<int:experience_id>', methods=['GET'])
def get_experience_by_id(experience_id: int):
    experience = Experience.query.filter(Experience.id == experience_id).first()
    if experience:
        result = experience_schema.dump(experience)
        return jsonify(experience=result)
    else:
        return jsonify(message="No Experience Found"), 404


@app.route('/api/experience/create', methods=['POST'])
def create_experience():
    if request.json:
        if validate_experience_params(request.json):
            if parameters_in_request_json(request.json, experience_params):
                company_name = request.json['company_name']
                position_title = request.json['position_title']
                start_date = datetime.strptime(request.json['start_date'],
                                               "%m-%d-%Y")
                end_date = datetime.strptime(request.json['end_date'],
                                             "%m-%d-%Y")
                description = request.json['description']
                experience = Experience(company_name=company_name,
                                        position_title=position_title,
                                        start_date=start_date,
                                        end_date=end_date,
                                        description=description)
                db.session.add(experience)
                db.session.commit()
                return jsonify(id=f"{request.host_url}api/experience/"
                                  f"{experience.id}")
            else:
                return jsonify(message="One Or More Parameters Are Missing",
                               required_parameters=user_params), 400
        else:
            return jsonify(message="Invalid Data",
                           reasons=["Date Must Be Formatted MM-DD-YYYY"]), 400
    else:
        return jsonify(message="Request Parameters Must Be Submitted In JSON"
                       ), 400


@app.route('/api/experience/<int:experience_id>', methods=['PUT'])
def update_experience_by_id(experience_id: int):
    if request.json:
        experience = Experience.query.filter(Experience.id == experience_id).first()
        if experience:
            if validate_experience_params(request.json):
                if request.json.get('company_name'):
                    experience.company_name = request.json['company_name']
                if request.json.get('position_title'):
                    experience.position_title = request.json['position_title']
                if request.json.get('start_date'):
                    experience.start_date = datetime.strptime(request.json[
                                                                  'start_date'],
                                                              "%m-%d-%Y")
                if request.json.get('end_date'):
                    experience.end_date = datetime.strptime(request.json[
                                                                'end_date'],
                                                            "%m-%d-%Y")
                if request.json.get('description'):
                    experience.description = request.json['description']
                db.session.add(experience)
                db.session.commit()
                result = experience_schema.dump(experience)
                return jsonify(experience=result)
            else:
                return jsonify(message="Invalid Data",
                               reasons=["Date Must Be Formatted MM-DD-YYYY"]), 400
        else:
            return jsonify(message="No Experience Found"), 404
    else:
        return jsonify(message="Request Parameters Must Be Submitted In JSON"
                       ), 400


@app.route('/api/experience/<int:experience_id>', methods=['DELETE'])
def delete_experience_by_id(experience_id: int):
    experience = Experience.query.filter(Experience.id == experience_id).first()
    if experience:
        db.session.delete(experience)
        db.session.commit()
        return '', 204
    else:
        return jsonify(message="No Experience Found"), 404


def parameters_in_request_json(request_json, parameter_list):
    for parameter in parameter_list:
        if parameter not in request_json:
            return False
    return True


def valid_user_params(request_json):
    email_regex = re.compile('[^@]+@[^@]+\\.[^@]+')
    password_regex = re.compile('^(?=.*\\d).{4,15}$')
    if 'email_address' in request_json:
        if not email_regex.match(request_json['email_address']):
            return False
    if 'password' in request_json:
        if not password_regex.match(request_json['password']):
            return False
    return True


def validate_experience_params(request_json):
    if 'start_date' in request_json:
        try:
            datetime.strptime(request_json['start_date'], "%m-%d-%Y")
        except ValueError:
            return False
    if 'end_date' in request_json:
        try:
            datetime.strptime(request_json['end_date'], "%m-%d-%Y")
        except ValueError:
            return False
    return True


if __name__ == '__main__':
    app.run()
