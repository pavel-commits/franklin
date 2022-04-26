import datetime

from flask_restful import Resource, request
from flask import jsonify

from models import db_session
from models.categories import Categories
from models.courses import Courses
from models.tests import Tests
from models.sides import Sides

from models.results import Results
from get_results import _get_result

with open("static/txt/apikey.txt") as f:
    APIKEY = f.read().strip()


class CoursesResource(Resource):
    def get(self):
        args = request.args

        apikey = args.get("apikey")

        if not apikey or apikey != APIKEY:
            return jsonify(
                {
                    "error": "Apikey is not stated or incorrect. Reg in https://127.0.0.1:8080/register to receive an apikey"}
            )

        side_id = args.get('side_id')
        category_id = args.get('category_id')
        course_id = args.get('course_id')

        db_sess = db_session.create_session()

        if course_id:
            if not course_id.isdigit():
                return {"error": "course_id has to be integer"}
            course = db_sess.query(Courses).get(int(course_id))
            if not course:
                return {"error": "not found"}
            return jsonify(
                {
                    "response": {
                        "courses": [
                            {"course": course.to_dict(only=('id',
                                                            'name',
                                                            'description',
                                                            'price',
                                                            'url',
                                                            'image',
                                                            'brand',
                                                            'workability',
                                                            'long')),
                             "course_categories": [
                                 category.to_dict(only=('id', 'name', 'side_id')) for category in course.categories
                             ]}
                        ]
                    },
                    "datetime": datetime.datetime.now()
                }
            )
        else:
            if category_id:
                if not category_id.isdigit():
                    return {"error": "category_id has to be integer"}
                category = db_sess.query(Categories).get(category_id)
                if not category:
                    return {"error": "not found"}
                return jsonify(
                    {
                        "response": {
                            "categories": [
                                {
                                    "category": category.to_dict(only=('id',
                                                                       'name',
                                                                       'side_id'
                                                                       )),
                                    "category_courses": [
                                        {
                                            "course": course.to_dict(only=('id',
                                                                           'name',
                                                                           'description',
                                                                           'price',
                                                                           'url',
                                                                           'image',
                                                                           'brand',
                                                                           'workability',
                                                                           'long')),
                                            "course_categories": [
                                                category.to_dict(only=('id', 'name', 'side_id')) for category in
                                                course.categories
                                            ]
                                        } for course in category.courses
                                    ]
                                }
                            ]
                        },
                        "datetime": datetime.datetime.now()
                    }
                )
            else:
                if side_id:
                    if not side_id.isdigit():
                        return {"error": "side_id has to be integer"}
                    side = db_sess.query(Sides).get(side_id)
                    if not side:
                        return {"error": "not found"}

                    return jsonify(
                        {
                            "response": {
                                "sides": [
                                    {
                                        "side": side.to_dict(only=('id',
                                                                   'name',
                                                                   'image',
                                                                   'description',
                                                                   'json_number'
                                                                   )),
                                        "side_categories": [
                                            {
                                                "category": category.to_dict(only=('id',
                                                                                   'name',
                                                                                   'side_id'
                                                                                   )),
                                                "category_courses": [
                                                    {
                                                        "course": course.to_dict(only=('id',
                                                                                       'name',
                                                                                       'description',
                                                                                       'price',
                                                                                       'url',
                                                                                       'image',
                                                                                       'brand',
                                                                                       'workability',
                                                                                       'long')),
                                                        "course_categories": [
                                                            category.to_dict(only=('id', 'name', 'side_id')) for
                                                            category in
                                                            course.categories
                                                        ]
                                                    } for course in category.courses
                                                ]
                                            } for category in side.categories
                                        ]
                                    }
                                ]
                            },
                            "datetime": datetime.datetime.now()
                        }
                    )
                else:
                    sides = db_sess.query(Sides).all()
                    if not sides:
                        return {"error": "not found"}
                    return jsonify(
                        {
                            "response": {
                                "sides": [
                                    {
                                        "side": side.to_dict(only=('id',
                                                                   'name',
                                                                   'image',
                                                                   'description',
                                                                   'json_number'
                                                                   )),
                                        "side_categories": [
                                            {
                                                "category": category.to_dict(only=('id',
                                                                                   'name',
                                                                                   'side_id'
                                                                                   )),
                                                "category_courses": [
                                                    {
                                                        "course": course.to_dict(only=('id',
                                                                                       'name',
                                                                                       'description',
                                                                                       'price',
                                                                                       'url',
                                                                                       'image',
                                                                                       'brand',
                                                                                       'workability',
                                                                                       'long')),
                                                        "course_categories": [
                                                            category.to_dict(only=('id', 'name', 'side_id')) for
                                                            category in
                                                            course.categories
                                                        ]
                                                    } for course in category.courses
                                                ]
                                            } for category in side.categories
                                        ]
                                    } for side in sides
                                ]
                            },
                            "datetime": datetime.datetime.now()
                        }
                    )


class ResultsResource(Resource):
    def get(self):
        args = request.args

        apikey = args.get("apikey")

        if not apikey or apikey != APIKEY:
            return jsonify(
                {
                    "error": "Apikey is not stated or incorrect. Reg in https://127.0.0.1:8080/register to receive an apikey"}
            )

        test_id = args.get('test_id')
        result_id = args.get('result_id')

        db_sess = db_session.create_session()
        sides = db_sess.query(Sides).all()

        if result_id:
            if not result_id.isdigit():
                return {"error": "result_id has to be integer"}
            result = db_sess.query(Results).get(result_id)
            if not result:
                return {"error": "not found"}
            return jsonify(
                {
                    "response": {
                        "sides": [side.to_dict(only=('name', 'id')) for side in sides],
                        "results": [
                            {
                                "result": result.to_dict(only=('id',
                                                               'result',
                                                               'date')),
                                "result_test": result.test.to_dict(only=('id', 'name', 'description')),
                                "result_meaning": _get_result(result.result)
                            }
                        ]
                    },
                    "datetime": datetime.datetime.now()
                }
            )
        else:
            if test_id:
                if not test_id.isdigit():
                    return {"error": "result_id has to be integer"}
                test = db_sess.query(Tests).get(test_id)
                if not test:
                    return {"error": "not found"}
                return jsonify(
                    {
                        "response": {
                            "sides": [side.to_dict(only=('name', 'id')) for side in sides],
                            "tests": [
                                {
                                    "test": test.to_dict(only=('id', 'name', 'description')),
                                    "test_results": [
                                        {
                                            "result": result.to_dict(only=('id',
                                                                           'result',
                                                                           'date')),
                                            "result_test": result.test.to_dict(only=('id', 'name', 'description')),
                                            "result_meaning": _get_result(result.result)
                                        } for result in test.results
                                    ]
                                }
                            ]
                        },
                        "datetime": datetime.datetime.now()
                    }
                )

            else:
                tests = db_sess.query(Tests).all()
                if not tests:
                    return {"error": "not found"}
                return jsonify(
                    {
                        "response": {
                            "sides": [side.to_dict(only=('name', 'id')) for side in sides],
                            "tests": [
                                {
                                    "test": test.to_dict(only=('id', 'name', 'description')),
                                    "test_results": [
                                        {
                                            "result": result.to_dict(only=('id',
                                                                           'result',
                                                                           'date')),
                                            "result_test": result.test.to_dict(only=('id', 'name', 'description')),
                                            "result_meaning": _get_result(result.result)
                                        } for result in test.results
                                    ]
                                } for test in tests
                            ]
                        },
                        "datetime": datetime.datetime.now()
                    }
                )
