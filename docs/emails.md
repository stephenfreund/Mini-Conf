# Using AWS to Send Bulk Email

## Upload Segment

* Generate the csv file:

    ```console
    $ ./auth0_all_users.py > /tmp/email.csv 
    $ ./pinpoint_email_csv_to_segment.py /tmp/email.csv > /tmp/pinpoint.csv
    $ cat /tmp/pinpoint.csv
    ChannelType,Address
    EMAIL,...
    EMAIL,....uk
    EMAIL,....edu
    ...
    ```

    You can use `regmaster_all_users.py` instead if you want that list instead

* Goto <https://console.aws.amazon.com/pinpoint/home?region=us-east-1#/apps/b466c680934647d889a95ab17ee7df12/segments>
* Click `Create a Segment`.
* Select `Import a Segment`.
* Click `Choose Files`. 
* Select your `pinpoint.csv` file.
* Change the name near the bottom of the page to something descriptive.
* Click `Create Segment`.

## Create a Message Template

* Goto <https://console.aws.amazon.com/pinpoint/home?region=us-east-1#/templates/overview>
* Click `Create Template`.
* Fill in template name, Subject, and Message.
    * Any embedded href should look like `<a ses:no-track href="aws.amazon.com">Amazon Web Services</a>` to avoid stupid tracking.

## Launch a Campaign.

* Goto <https://console.aws.amazon.com/pinpoint/home?region=us-east-1#/apps/b466c680934647d889a95ab17ee7df12/campaigns>
* Click `Create Campaign`.
    * Type is standard, Channel is Email.  Click `Next`.
* Use an existing segment, and choose it.  Click `Next`.
* Choose the template.  Send a test email to specific Email Addresses, eg: you.  Click `Next`.
* Choose "Send Immediately".  Click `Next`.
* Double check all settings.  Click `Launch campaign`.
* Email starts to flow in 15-20 seconds.  The dashboard gets refreshed after that.
