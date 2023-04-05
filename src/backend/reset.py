import json, os, shutil

def reset():
    json_object1 = json.dumps([], indent=4)
    with open("publickeys.json", "w") as f:
        f.write(json_object1)

    with open("signatures.json", "w") as f:
        f.write(json_object1)

    with open("aggregatesign.json", "w") as f:
        f.write(json_object1)

    with open("submittedfiles.json", "w") as f:
        f.write(json_object1)
    
    with open("individualVerify.json", "w") as f:
        f.write(json_object1)

    if (os.path.exists('content')):
        shutil.rmtree('content')
        os.mkdir('content')

reset()
