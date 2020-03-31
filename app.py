from flask import Flask, jsonify, request
from flask.views import MethodView
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/trainingtset'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
swag = Swagger(app)


class UserModel(db.Model):
    """
    Creating the User Model

    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))


class UserModelSchema(ma.Schema):
    """
        Using marshmallow for serialization and deserialization operations

    """
    class Meta:
        fields = ('id', 'name', 'email', 'password')


class PostAPIView(MethodView):

    def get(self, user_id):
        """
        Getting the user based on id
        ---
        tags:
          - users
        parameters:
          - name: user_id
            in: path
            description: ID of User (type any number)
            required: true
            type: integer
        definitions:
          User:
            type: object
            properties:
              name:
                type: string
              email:
                type: string
              password:
                type: string
        responses:
          200:
            description: Returns the user based on id
            schema:
              id: Users
              type: object
              properties:
                users:
                  type: array
                  items:
                    $ref: '#/definitions/User'
        """
        print(user_id)
        data = UserModel.query.get(user_id)
        return jsonify(UserModelSchema().dump(data))

    def delete(self, user_id):
        """
        Deleting the user based on id
        ---
        tags:
          - users
        parameters:
          - name: user_id
            in: path
            description: ID of User (type any number)
            required: true
            type: integer
        definitions:
          User:
            type: object
            properties:
              name:
                type: string
              email:
                type: string
              password:
                type: string
        responses:
          200:
            description: Returns the user based on id
            schema:
              id: Users
              type: object
              properties:
                users:
                  type: array
                  items:
                    $ref: '#/definitions/User'
                """
        data = UserModel.query.get(user_id)
        db.session.delete(data)
        db.session.commit()
        return jsonify(UserModelSchema().dump(data))

    def put(self, user_id):
        """
        Updating the user
        ---
        tags:
          - users
        parameters:
          - name: user_id
            in: path
            description: ID of User (type any number)
            required: true
            type: integer
          - in: body
            name: body
            schema:
              id: User
              required:
                - email
                - name
                - password
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
                password:
                  type: string
                  description: password for user
        responses:
          201:
            description: User Updated
        """
        data = UserModel.query.get(user_id)
        data.name = request.json['name']
        data.email = request.json['email']
        data.password = request.json['password']
        db.session.commit()

        return 'User Updated Successfully'


app.add_url_rule(
    '/user/<user_id>',
    view_func=PostAPIView.as_view('user'),
    methods=['GET', 'DELETE', 'PUT']
)


class GetPostView(MethodView):

    def get(self):
        """
        Getting  all the users
        ---
        tags:
          - users
        definitions:
          User:
            type: object
            properties:
              name:
                type: string
              email:
                type: string
              password:
                type: string
        responses:
          200:
            description: Returns the user based on id
            schema:
              id: Users
              type: object
              properties:
                users:
                  type: array
                  items:
                    $ref: '#/definitions/User'
        """
        data = UserModel.query.all()
        return jsonify(UserModelSchema().dump(data, many=True))

    def post(self):
        """
        Creating the user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - email
                - name
                - password
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
                password:
                  type: string
                  description: password for user
        responses:
          200:
            description: User Created
        """
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        print(name, password)
        data = UserModel(name=name, email=email, password=password)
        db.session.add(data)
        db.session.commit()

        return 'User Created Successfully'


app.add_url_rule(
    '/users',
    view_func=GetPostView.as_view('users'),
    methods=['GET', 'POST']
)

if __name__ == "__main__":
    app.run(debug=True)
