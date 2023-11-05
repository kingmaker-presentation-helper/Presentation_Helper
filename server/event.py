# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import db_fn, https_fn

# The Firebase Admin SDK to access the Firebase Realtime Database.
from firebase_admin import credentials, initialize_app, db

cred = credentials.Certificate("presentation-helper-37f03-firebase-adminsdk-h8b0k-54cd2dfce0.json")

app = initialize_app(cred, {
        'databaseURL': "https://presentation-helper-37f03-default-rtdb.asia-southeast1.firebasedatabase.app/",
        'storageBucket': "presentation-helper-37f03.appspot.com"
                                })


# Instance named "my-app-db-2", at path "/user/{uid}".
# The "my-app-db-2" instance must exist in this region.

@db_fn.on_value_written(
    reference="/user",
    instance="presentation-helper-37f03-default-rtdb",
    region="asia-southeast1",    
)
def on_written_function_instance(event: db_fn.Event ):
    print(event.data)
    # ...



@db_fn.on_value_created(
        reference="/test",
        instance="presentation-helper-37f03-default-rtdb",
        region="asia-southeast1",    
    )
def makeuppercase(event: db_fn.Event):
    """Listens for new messages added to /messages/{pushId}/original and
    creates an uppercase version of the message to /messages/{pushId}/uppercase
    """

    # Grab the value that was written to the Realtime Database.
    original = event.data
    if not isinstance(original, str):
        print(f"Not a string: {event.reference}")
        return

    # Use the Admin SDK to set an "uppercase" sibling.
    print(f"Uppercasing {event.params['pushId']}: {original}")
    upper = original.upper()
    parent = db.reference(event.reference).parent
    if parent is None:
        print("Message can't be root node.")
        return
    parent.child("uppercase").set(upper)

