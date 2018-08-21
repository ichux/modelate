from flask import jsonify, request

from modelate.controllers.apiv1 import apiv1


@apiv1.route('', methods=["POST"])
def index():
    """
    Password authentication is done here.

    Note: there's no trailing slash in this route. It is to avoid FormDataRoutingRedirect error being thrown
    :return: json
    """
    # curl -k -X POST https://127.0.0.1:43210/api/v1.0 -H 'content-type: application/json' -d '{"data": "exhaust"}'
    return jsonify({'meta': {'success': True, 'code': 200}, 'result': {"message": request.get_json()}}), 200
