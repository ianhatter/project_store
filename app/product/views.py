from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view

from flask import Blueprint, jsonify, abort, request
from .models import Product, User, db

from flask import Blueprint, jsonify, abort, request
import hashlib
import secrets


def index(request):
    print("Products Are Here")
    queryset = Tutorial.objects.all()
    return render(request, "products/index.html", {'products': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/index.html'

    def get(self, request):
        queryset = Tutorial.objects.all()
        return Response({'products': queryset})


class list_all_tutorials(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/products_list.html'

    def get(self, request):
        queryset = Tutorial.objects.all()
        return Response({'products': queryset})
    



bpd = Blueprint("products", __name__, url_prefix="/products")


@bpd.route("", methods=["GET"])  # decorator takes path and list of HTTP verbs
def index():
    products = Product.query.all()  # ORM performs SELECT query
    result = []
    for p in products:
        result.append(p.serialize())  
    return jsonify(result)  # return JSON response


@bpd.route("/<int:id>", methods=["GET"])
def show(id: int):
    p = Product.query.get_or_404(id)
    return jsonify(p.serialize())


@bpd.route("", methods=["POST"])
def create():
    # req body must contain user_id and content
    if "user_id" not in request.json or "content" not in request.json:
        return abort(400)

    # user with id of user_id must exist
    User.query.get_or_404(request.json["user_id"])


    p = Product(user_id=request.json["user_id"], content=request.json["content"])

    db.session.add(p)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(p.serialize())


@bpd.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    p = Product.query.get_or_404(id)
    try:
        db.session.delete(p)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode("utf-8")).hexdigest()


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("", methods=["GET"])
def index():
    users = User.query.all()
    result = []
    for u in users:
        result.append(u.serialize())
    return jsonify(result)


@bp.route("/<int:id>", methods=["GET"])
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())


@bp.route("", methods=["POST"])
def create():
    # req body must contain user_id and content
    if "username" not in request.json or "password" not in request.json:
        return abort(400)

    if len(request.json["username"]) < 3:
        return abort(400)

    if len(request.json["password"]) < 8:
        return abort(400)

    u = User(
        username=request.json["username"], password=scramble(
            request.json["password"])
    )

    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(u.serialize())


@bp.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route("/<int:id>", methods=["PATCH", "PUT"])
def update(id: int):
    u = User.query.get_or_404(id)
    if "username" not in request.json or "password" not in request.json:
        return abort(400)

    if "username" in request.json:
        if len(request.json["username"]) < 3:
            return abort(400)
        if len(request.json["username"]) >= 3:
            u.username = request.json["username"]

    if "password" in request.json:
        if len(request.json["password"]) < 8:
            return abort(400)
        if len(request.json["password"]) >= 8:
            u.password = scramble(request.json["password"])

    try:
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)



