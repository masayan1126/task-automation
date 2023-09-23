
python3 -m venv content_share/venv
source content_share/venv/bin/activate

deactivate

pip install -r content_share/requirements.txt
pip freeze > content_share/requirements.txt

python -m pip install functions-framework
functions-framework --source content_share/main.py --target hello_http --port=8080 --debug
[localhost:8080](http://localhost:8080)

VSCODE

python.autoComplete.extraPaths




```
certifi==2022.6.15
charset-normalizer==3.2.0
distlib==0.3.5
filelock==3.7.1
idna==3.4
oauthlib==3.2.2
pipenv==2022.7.4
platformdirs==2.5.2
python-dotenv==1.0.0
requests==2.31.0
requests-oauthlib==1.3.1
six==1.16.0
tweepy==4.14.0
urllib3==2.0.5
virtualenv==20.15.1
virtualenv-clone==0.5.7

```
