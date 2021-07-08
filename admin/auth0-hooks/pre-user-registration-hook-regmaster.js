// JUST FOR TESTING -- DON'T INCLUDE IN AUTH0.
class PreUserRegistrationError {
  constructor(logMessage, userMessage) {
      this.logMessage = logMessage;
      this.userMessage = userMessage;
  }
}


  /*
  Access should only be granted to verified users.
  RegMaster returns one of the following for validation requests:
  {"attendeeNumber":"21000","firstname":"Mike","lastname":"Moshell"} - registered and paid
  {"error":"balance due"} - registered and not paid
  {"error":"not found"} - email is not registered.
  {"error":"access denied"}  - bad password
  */


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
  
  request.post({
    url: 'https://regmaster.com/2021conf/PLDI21/PLDIgetName.php?action=validate&password=UZHgcjZdzsGg&email=' + encodeURIComponent(user.email)
  },
  (err, response, body) => {
    if (err) {
      return cb(new PreUserRegistrationError(`Denied sign up for ${user.email} -- you must complete registration for PLDI first.`, "RegMaster failed to return response."));
    }
    const res = JSON.parse(body)
    if (res.error) {
     
      // If user.app_metadata.special exists, override a negative regmaster response.
      // This gives us a way to add users who are not registered via a script.
      if (!(user.app_metadata && user.app_metadata.special)) {
        
        // This message is not used w/ classic login, but will include here anyway...
        const localizedMessage = 'You are not allowed to sign up.';
        return cb(new PreUserRegistrationError(`Denied sign up for ${user.email} -- you must complete registration for PLDI first.`, localizedMessage));
      }
    }
    
    // No errors, good to go!
    // We need to pass along any new metadata -- it's all empty for us, but ...
    // we include the regmaster result so we have a log of it somewhere.
    const ok = {
      user: {
        user_metadata: { regmaster: res },
        app_metadata:  {  }
      }
    };
    return cb(null, ok);
  });
}

