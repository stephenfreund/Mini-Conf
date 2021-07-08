// JUST FOR TESTING -- DON'T INCLUDE IN AUTH0.
class PreUserRegistrationError {
  constructor(logMessage, userMessage) {
    this.logMessage = logMessage;
    this.userMessage = userMessage;
  }
}



/*
* Build empty metadata for user, but add
* whatever we want as the reason the user
* is valid.  Useful for debugging later...
*/
function metaDataForUser(payload) {
  return {
    user: {
      user_metadata: { nname: payload },
      app_metadata:  {  }
    }
  };
}

/**
@param {object} user - The user being created
@param {string} user.tenant - Auth0 tenant name
@param {string} user.username - user name
@param {string} user.password - user's password
@param {string} user.email - email
@param {boolean} user.emailVerified - is e-mail verified?
@param {string} user.phoneNumber - phone number
@param {boolean} user.phoneNumberVerified - is phone number verified?
@param {object} context - Auth0 connection and other context info
@param {string} context.renderlanguage - language used by signup flow
@param {string} context.request.ip - ip address
@param {string} context.request.language - language of the client agent
@param {object} context.connection - information about the Auth0 connection
@param {object} context.connection.id - connection id
@param {object} context.connection.name - connection name
@param {object} context.connection.tenant - connection tenant
@param {object} context.webtask - webtask context
@param {function} cb - function (error, response)
*/

/*
* Build empty metadata for user, but add
* whatever we want as the reason the user
* is valid.  Useful for debugging later...
*/
function metaDataForUser(payload) {
  return {
    user: {
      user_metadata: { nname: payload },
      app_metadata:  {  }
    }
  };
}

/**
@param {object} user - The user being created
@param {string} user.tenant - Auth0 tenant name
@param {string} user.username - user name
@param {string} user.password - user's password
@param {string} user.email - email
@param {boolean} user.emailVerified - is e-mail verified?
@param {string} user.phoneNumber - phone number
@param {boolean} user.phoneNumberVerified - is phone number verified?
@param {object} context - Auth0 connection and other context info
@param {string} context.renderlanguage - language used by signup flow
@param {string} context.request.ip - ip address
@param {string} context.request.language - language of the client agent
@param {object} context.connection - information about the Auth0 connection
@param {object} context.connection.id - connection id
@param {object} context.connection.name - connection name
@param {object} context.connection.tenant - connection tenant
@param {object} context.webtask - webtask context
@param {function} cb - function (error, response)
*/
module.exports = function (user, context, cb) {
  
  const request = require('request');
  var reason = null;
  
  request.post({
    url: 'https://regmaster.com/aaaaaaaaaaaa?action=validate&password=aaaaaaaaaaaa&email=' + encodeURIComponent(user.email)
  },
  (err, response, body) => {
    
    // BUG FIX:
    // There is a JSON encoded error from RegMaster.  It sends D'Antoni as D\'Antoni -- that should be \\'
    // So: do NOT parse their response as JSON.  Treat as text and match the first part of the string
    // to see if we get an error or not.

    /* response formats:
    {"attendeeNumber":"21000","firstname":"Mike","lastname":"Moshell"} - registered and paid
    {"error":"balance due"} - registered and not paid
    {"error":"not found"} - email is not registered.
    {"error":"access denied"}  - bad password
    */
    // regmaster doesn't respond or regmaster returns an error
    if (err || body.startsWith('{"error"')) {
      request.get({
        url: 'https://www.dropbox.com/s/aaaaaaaaaaaa/email-addresses.csv?dl=1'
      },
      (err2, response2, body2) => {
        /* body is a CSV file with a header line, where the rows are:
        email,full name 
        */
        if (user.email.toLowerCase().endsWith("slideslive.com")) { 
          return cb(null, metaDataForUser("slideslive")); 
        } 
        
        const whitelist = body2.split('\n');
        whitelist.shift(); // skip header
        
        if (user.email){
          const entry = whitelist.find(function (row) {
            if (row.length === 0) return false;  // skip blank lines
            const cols = row.split(",")
            const email = cols[0]
            return email.toLowerCase() === user.email.toLowerCase();
          });
          
          if (entry) { 
            return cb(null, metaDataForUser("sheet")); 
          } 
        }

        // const slack = require('slack-notify')('https://hooks.slack.com/services/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');

        // const message = `Failed Reg: ${user.email}`;
        // const channel = '#auth0';

        // slack.success({
        //   text: message,
        //   channel: channel
        // });

        return cb(new PreUserRegistrationError(`Denied sign up for ${user.email} -- you must complete registration for PLDI first.`));      
      });
    } else {
      return cb(null, metaDataForUser("regmaster")); 
    }
  });
}

