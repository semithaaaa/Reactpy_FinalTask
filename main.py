# Import necessary modules
from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, event, html, use_state
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Create a FastAPI app instance
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your MongoDB URI with username and password
uri = "mongodb+srv://admin:admin@123@cluster0.2n0dmlw.mongodb.net/"

# Escape the username and password
parsed_uri = urllib.parse.urlparse(uri)
escaped_username = urllib.parse.quote_plus(parsed_uri.username)
escaped_password = urllib.parse.quote_plus(parsed_uri.password)
escaped_uri = uri.replace(parsed_uri.username, escaped_username).replace(parsed_uri.password, escaped_password)

# Create a new client and connect to the server
client = MongoClient(escaped_uri, server_api=ServerApi("1"))
db = client["ReactPy_Projects"]
collection = db["Test"]

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
def login(login_data: dict):
    username = login_data["name"]
    password = login_data["password"]

    # Create a document to insert into the collection
    document = {"name": username, "password": password}

    # Insert the document into the collection
    post_id = collection.insert_one(document).inserted_id
    print(post_id)

    return {"message": "Login successful"}


@component
def MyCrud():
    # Creating the state
    alltodo = use_state([])
    name, set_name = use_state("")
    password, set_password = use_state("")

    def mysubmit(event):
        newtodo = {"name": name, "password": password}  # Remove .value here
        alltodo.set_value(alltodo.value + [newtodo])
        login(newtodo)

    list = [
        html.li(
            {},
            f"{b} => {i['name']} ; {i['password']} ",
        )
        for b, i in enumerate(alltodo.value)
    ]

    def handle_event(event):
        print(event)

    return html.div(
        {
            "style": {
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "padding": "20px",
                "background-color": "#f0f0f0",
                "border-radius": "10px",
                "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.2)",
            }
        },
        html.form(
            {"on_submit": mysubmit},
            html.h1("Login Form"),
            html.h2("ReactPy & MongoDB"),
            html.input(
                {
                    "type": "text",  # Corrected "test" to "text"
                    "placeholder": "Name",
                    "on_change": lambda event: set_name(event["target"]["value"]),
                }
            ),
            html.div(
                html.input(
                    {
                        "type": "password",
                        "placeholder": "Enter Password",
                        "on_change": lambda event: set_password(event["target"]["value"]),
                    }
                )
            ),
            html.button(
                {
                    "type": "submit",
                    "on_click": event(
                        lambda event: mysubmit(event), prevent_default=True
                    ),
                },
                "Submit",
            ),
        ),
        html.ul(list),
    )

# Configure the FastAPI app with ReactPy component
configure(app, MyCrud)

# Define host and port
host = "127.0.0.1"
port = 8001

# Run the app using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=port)
