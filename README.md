Create a Python3 Virtual Environment:
    python3 -m venv env

    Activate the Virtual Environment:
    source env/bin/activate

    Deactivate the Virtual Environment:
    deactivate

    To Remove a Virtual Environment:
    sudo em -rf venv

pip3 install flask

Automagically create a requirements.txt file:
    pip3 freeze > requirements.txt

Start the Flask Server:
    flask run

Run the Flask Server in Debug Mode:
    flask --app app.py --debug run