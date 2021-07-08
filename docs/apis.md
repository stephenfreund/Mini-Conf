# Local Level API Functions

## Data Files

- `config.yml`: all the secrets - do not add to repo
- `blacklist.yml`: banned email addresses

## All

* **`regmaster_validate_email.py <email>`**: verifies whether `email` is present in each service.  

    ```console
    $ ./validate_email.py ...
    RegMaster
    ---------
    Not Registered: not found

    Auth0
    ---------
    [
        {
            ...
            "email": "...",
            "identities": [ ... ],
            "name": "Stephen Freund (sfreund)",
            ...
        },
    ]

    Gather
    ---------
    {'name': 'Stephen Freund (sfreund)'}
    ```

## RegMaster

* **`regmaster_validate_email.py <email>`**: verifies whether `email` is registered and paid.  

    ```console
    $ ./regmaster_validate_email.py ...
    Registered: {
      "attendeeNumber": "21000",
      "firstname": "Mike",
      "lastname": "Moshell"
    }
    $ ./regmaster_validate_email.py ...
    Not Registered: not found
    $ ./regmaster_validate_email.py ...
    Not Registered: balance due
    ```


* **`regmaster_all_registered.py`**: returns a CSV of all paid registrants.  NOTE: commas in names
    are removed because RegMaster isn't handling them properly in the CSV they send us...

    ```console
    $ ./regmaster_all_registered.py
    email,name
    ...,Stephen Freund
    ...,Adam Eveman
    ...,Mike Moshell
    ...,Stephen COmma Freund COmma
    ```

* **`regmaster_all_registered_with_unpaid.py`**: returns a CSV of all paid and unpaid registrants.  

    ```console
    $ ./regmaster_all_registered_with_unpaid.py
    email,name
    ...,Stephen Freund
    ...
    ```


## Auth0

* **`auth0_validate_email.py <email>`**: verifies whether `email` is in Auth0 database.

    ```console
    $ ./auth0_validate_email.py ...
    Email address is not in Database.
    $ ./auth0_validate_email.py ...
    [
        {
            "created_at": "2021-02-01T10:13:15.362Z",
            "email": "...",
            "email_verified": true,
            "identities": [
            {
                "user_id": "6017d43b441fd6007082c3cb",
                "provider": "auth0",
                "connection": "Username-Password-Authentication",
                "isSocial": false
            }
            ],
            "name": "Stephen Freund (sfreund)",
            ...
        }
    ]
    ```

* **`auth0_all_users.py`**: lists all users in our database on Auth0

    ```console
    $ ./auth0_all_users.py 
    email,name
    ...,...
    ...,Dan Iorga
    ...,Daniel Barowy
    ...
    ```

* **`auth0_add_user.py <email> <first> <last>`**: add user to Auth0 DB.  
    - This sets up a new user with a default password.
    - Do only if necessary, and not designed for bulk additions.
    - Note email must be in either RegMaster as registered and paid, or
      in Steve's CSV file on DropBox.

    ```console
    $ ./auth0_add_user.py ... Steve Freund
    ```

## Gather

* **`gather_validate_email.py <email>`**: verifies whether `email` is in gather's email list

    ```console
    $ ./gather_validate_email.py ...
    Email not found.
    $ ./gather_validate_email.py ...
    {'name': 'Stephen Freund'}
    $ 
    ```

* **`gather_all_users.py`**: lists all users in Gather's email list

    ```console
    $ ./gather_all_users.py 
    email,name
    ...,...
    ...,Dan Iorga
    ...,Daniel Barowy
    ...
    ```

* **`gather_add_user.py <email> <first> <last>`**: add user to gather.  
    - This isn't connected to RegMaster or Auth0.
    - So the change won't be persistent if you blow away the gather email list and upload a new one.

    ```console
    $ ./gather_add_user.py ... Steve Freund
    ```

* **`gather_add_all_auth0_users.py`**: adds everyone from Auth0 to the Gather email list.  
    - This only adds to the list, it doesn't not remove anyone.

    ```console
    $ ./gather_add_all_auth0_users.py
    ```

* **`gather_add_all_regmaster_users.py`**: adds everyone from RegMaster to the Gather email list.  
    - This only adds to the list, it doesn't not remove anyone.

    ```console
    $ ./gather_add_all_regmaster_users.py
    ```

* **`gather_purge_blacklisted.py`**: removed blacklisted emails from Gather email list.
    - Warning: This is not an atomic operation!  We may lose concurrent additions to the list.
    - Use only if necessary.

    ```console
    $ ./gather_purge_blacklisted.py
    ```

## Slack  [TBD]

* **`slack_validate_email.py <email>`**: verifies whether `email` is in Slack workspace

    ```console
    TBD
    ```

* **`slack_all_users.py`**: lists all users in Slack workspace

    ```console
    TBD
    ```




## AWS

* **`pinpoint_email_csv_to_segment.py <email.csv>`**: create a csv file that can be loaded as a Segment in AWS.

    ```console
    $ cat test.csv
    email,name
    ...,Stephen Freund
    ...,Adam Eveman
    ...,Mike Moshell
    ...,Stephen COmma Freund COmma
    $ ./pinpoint_email_csv_to_segment.py test.csv 
    ChannelType,Address
    EMAIL,...
    EMAIL,...
    EMAIL,...
    EMAIL,...
    ```
