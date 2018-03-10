#!/usr/bin/env python
from flask import Flask, abort, jsonify, make_response, request
import json
import os
import subprocess
import tempfile

from ingredient_phrase_tagger.training import utils

app = Flask(__name__)


def tag(ingredients_string):
    _, tmpFile = tempfile.mkstemp()

    with open(tmpFile, 'w') as outfile:
        outfile.write(utils.export_data(ingredients_string.splitlines()))

    modelFilename = "/ingredient-phrase-tagger/tmp/model_file"
    result = subprocess.check_output("crf_test -v 1 -m %s %s" % (modelFilename, tmpFile), shell=True)
    os.system("rm %s" % tmpFile)
    return json.dumps(utils.import_data(result.splitlines()), indent=4)


@app.route('/ingredients-phrase-tagger/api/v1.0/ingredients', methods=['POST'])
def tag_ingredients():
    if not request.json or not 'ingredients_list' in request.json:
        abort(400)
    return tag(request.json['ingredients_list']), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)