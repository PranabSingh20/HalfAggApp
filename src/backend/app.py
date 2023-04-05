import json, os, hashlib, shutil
from flask import Flask, request, jsonify
from keygen import keypairs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Steps:
# 1. Student writes id, pdf file and clicks sign
# 2. Hit /sign?id=<id> where id and files are captured and dumped into a global folder
# 3. It generates a single keypair (dump into json) run(keypair -n 1) (dump keys in global json too only pk)
# 4. Take the file hash  and run(sign -m {file_hash}) change str to bytes in sign and no hashing (dump sign in global json)


@app.route('/sign', methods=['POST'])
def sign():
    upload_dir = os.path.join('content')
    if not (os.path.exists('content')):
        os.makedirs(upload_dir)
    studentId = int(request.args.get('studentId'))  # get the 'studentId' parameter from the request URL
    file = request.files['file']
    # print(studentId)

    f = open('submittedfiles.json')
    files = json.load(f)
    f.close()

    can = True
    for user in files:
        if(user['studentId'] == studentId and user['filename'] == file.filename):
            can = False
    if(can == False):
        return jsonify("The user has already submitted this file")
    
    newFilename = str(studentId) + '_' + file.filename

    file.save(os.path.join(upload_dir, newFilename))
    files.append({"studentId": studentId, "filename":file.filename})

    # print(files)

    json_object = json.dumps(files, indent=4)

    with open("submittedfiles.json", "w") as f:
        f.write(json_object)

    # create keypair dump public keys into json 

    sk = keypairs()

    # hash message and use it for signature

    file_hash = hashlib.sha256()
    file_path = os.path.join('content', newFilename)
    with open(file_path, 'rb') as f: 
        fb = f.read() 
        file_hash.update(fb) 

    os.system('python sign.py -m '+ str(file_hash.hexdigest()) + ' -sk '+ str(sk))

    print("sign",str(file_hash.hexdigest()))
    f = open('messages.json')
    messages = json.load(f)
    f.close()
    messages.append(str(file_hash.hexdigest()))
    json_object = json.dumps(messages, indent=4)

    with open("messages.json", "w") as f:
        f.write(json_object)

    return jsonify("Successfully signed")


@app.route('/aggregate-sign')
def aggregate_sign():

    os.system('python aggSign.py')
    f = open('aggregatesign.json')
    aggsign = json.load(f)
    f.close()

    return jsonify(aggsign)

@app.route('/aggregate-verify')
def aggregate_verify():

    os.system('python aggVerify.py')
    f = open('result.json')
    result = json.load(f)
    f.close()

    return jsonify(result)

@app.route('/individual-verify')
def individual_verify():

    messages = []
    f = open('submittedfiles.json')
    files = json.load(f)
    f.close()
    info = []
    for file in files:
        info.append([file['studentId'], file['filename']])
        newfileName = str(file['studentId']) + '_' + file['filename']
        file_path = os.path.join('content', newfileName)

        # Check if file is a regular file
        if os.path.isfile(file_path):
            file_hash = hashlib.sha256()
            # print(file_path)
            with open(file_path, 'rb') as f: 
                fb = f.read() 
                file_hash.update(fb) 
            messages.append(str(file_hash.hexdigest()))

    f = open('publickeys.json')
    publickeys = json.load(f)
    # print("Public keys : ", publickeys)
    f.close()

    f = open('signatures.json')
    signatures = json.load(f)
    # print("signatures : ", signatures)
    f.close()

    results = []
    for i in range(len(signatures)):
        os.system('python verify.py -m '+ str(messages[i]) + ' -p '+ str(publickeys[i]) + ' -s ' + str(signatures[i]))
        f = open('individualVerify.json')
        result = json.load(f)
        f.close()
        results.append([info[i][0], info[i][1], result])

    print("info ", info)
    print("results ", results)
    return jsonify(results)

@app.route('/reset')
def reset():

    os.system('python reset.py')
    return jsonify("Successfully reset")
