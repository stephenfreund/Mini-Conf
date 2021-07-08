# Auth0 Config

## Hooks

Setup these hooks at <https://manage.auth0.com/dashboard/us/dev-tdha92d1/hooks>

* Pre-Registration:
    * Version 1:
        * Consult RegMaster via the endpoint provided by Mike Moshell:
        * [../admin/auth0-hooks/pre-user-registration-hook-regmaster.js](../admin/auth0-hooks/pre-user-registration-hook-regmaster.js)
    * Version 2:
        * Consult a CSV file in Steve's DropBox folder
        * [../admin/auth0-hooks/pre-user-registration-hook-dropbox.js](../admin/auth0-hooks/pre-user-registration-hook-dropbox.js)
    * Version 3: 
        * Do #1 and then #2
        * [../admin/auth0-hooks/pre-user-registration-hook-combined.js](../admin/auth0-hooks/pre-user-registration-hook-combined.js)


* Post-Registration:
    * Add new users to the Gather email whitelist.
    * [../admin/auth0-hooks/post-registration-hook-gather.js](../admin/auth0-hooks/post-registration-hook-gather.js)
    * NOTE: This will not *create* a list if it isn't there already to avoid the hook from setting one up if
    we ever intentionally remove the list from Gather.


## Welcome Email

* Edit the HTML Here: <https://manage.auth0.com/dashboard/us/dev-tdha92d1/templates>
* Default version in [../admin/auth0-emails/auth0-welcome-email.html](../admin/auth0-emails/auth0-welcome-email.html)

## Slack SSO

* To Be Written when we get there...



