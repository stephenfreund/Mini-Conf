# Basic Operations

You should be in `~/PLDI-Mini-Conf/admin` for all of this

## Check whether email is valid for each service.


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

Or:

```console
$ ./regmaster_validate_email.py ...
{ ... }
$ ./auth0_validate_email.py ...
[
  {
    "created_at": "2021-02-01T10:13:15.362Z",
    "email": "...",
    "email_verified": true,
    "identities": [ ... ]
    "name": "Stephen Freund (sfreund)",
    ...
  }
]
$ ./gather_validate_email.py ...
{'name': 'Stephen Freund (sfreund)'}
```

Should return a valid record in each case.


## Get all registered users for each service

```console
$ ./regmaster_all_registered.py
email,name
...,Stephen Freund
...,Adam Eveman
...,Mike Moshell
...
$ ./auth0_all_users.py
email,name
...,...
...,Dan Iorga
...,Daniel Barowy
...
$ ./gather_all_users.py
email,name
...,...
...,Dan Iorga
...,Daniel Barowy
...
```

## Add unregistered user to our services

1. Add the email / username to this file: <https://www.dropbox.com/s/aw7sux8yq6i9qqc/email-addresses.csv?dl=0>

2. Then Do either:

    * These on the command line:

    ```console
    ./auth0_add_user.py email first last
    ./gather_add_user.py email
    ```

    * Add the user through the Auth0 UI, and then run the `gather_add_user.py` script for good measure...


**Note:** The user must be regsitered and paid, or in Steve's CSV file.

**Note:** Disable the pre-registration hook if you have problems:
<https://manage.auth0.com/dashboard/us/dev-tdha92d1/hooks>.  And **re-enable**
the hook afterwards.


## Add user to gather

```console
./gather_add_user.py email first last
```

## Block an email address

1. Add email address to `blacklist.yml`
2. Auth0
    * Go to <https://manage.auth0.com/dashboard/us/dev-tdha92d1/users>
    * Find user entry in list
    * Click the "..." button and select block.
3. Slack
    * Go to <https://pldi21.slack.com/admin>
    * Find user entry in list
    * Click the "..." button and select deactivate.
    * [Check this -- is it possible with SSO turned on?]
4. Gather
    * run `./gather_purge_blacklisted.py`

## UnBlock User

1. Remove email address from `blacklist.yml`
2. Auth0
    * Go to <https://manage.auth0.com/dashboard/us/dev-tdha92d1/users>
    * Find user entry in list
    * Click the "..." button and unblock.
3. Slack
    * Go to <https://pldi21.slack.com/admin>
    * Find user entry in list
    * Click the "..." button and select reactivate.
    * [Check this -- is it possible with SSO turned on?]
4. Gather
    * run `./gather_add_user.py email first last`

