// JUST FOR TESTING -- DON'T INCLUDE IN AUTH0.
class PreUserRegistrationError {
  constructor(logMessage, userMessage) {
      this.logMessage = logMessage;
      this.userMessage = userMessage;
  }
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

  // Load a csv file from Steve's DropBox account.
  // This is a CSV file with a header line, where the rows are:
  //   email,full name
  request.get(
  {
    url: 'https://www.dropbox.com/s/aw7sux8yq6i9qqc/email-addresses.csv?dl=1'
  },
  (err, response, body) => {
    const whitelist = body.split('\n');
    whitelist.shift(); // skip header
    
    var denyRegistration = !user.email || !whitelist.some(function (row) {
      
      if (row.length == 0) return false;  // skip blank lines

      const cols = row.split(",")
      const email = cols[0]
      return email.toLowerCase() === user.email.toLowerCase();

    });

    if (denyRegistration) {    
      // If user.app_metadata.special exists, override a negative regmaster response.
      // This gives us a way to add users who are not registered via a script.
      if (!(user.app_metadata && user.app_metadata.special)) {
        
        // This message is not used w/ classic login, but will include here anyway...
        const localizedMessage = 'You are not allowed to sign up.';
        return cb(new PreUserRegistrationError(`Denied sign up for ${user.email} -- you must complete registration for PLDI first.`, localizedMessage));
      }
    }
  
    var ok = {};

    // No errors, good to go!
    // We need to pass along any new metadata -- it's all empty for us, but ...
    // we include a note that we verified via the csv file.
    ok.user = {
      user_metadata: { approval: "spreadsheet check" },
      app_metadata: {  }
    };
    cb(null, ok);
  });
}
