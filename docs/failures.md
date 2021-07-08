# Panic Time!

## If Gather Email Verification Begins to Fail

* Delete email list from Gather server.
* Auth0 will stop adding names to it, so no further action is needed.
* To restart, use one of the `gather_add_all_...` scripts.

## If Slack SSO Begins to Fail

* Disable SSO from inside Slack.
* Create a shared invite link.
    * (You cannot do this first.)
    * Add to [Auth0's welcome message](https://github.com/pldi21/PLDI-Mini-Conf/blob/master/docs/auth0.md#welcome-email) to include the link
    * Send out to student volunteers so they know how to respond to requests.
* When you do this, all users may (check this) get an email asking them to set up a password.

## If Auth0 Begins to Fail

* Cry.
* Comment out this line in `sitedata/config.yml`:

    use_auth0: true
    
* `make deploy`
* Follow steps for Slack SSO above.


## If Website goes down

* Amazon...  What do we do?

 
