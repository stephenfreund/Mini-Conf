/**
@param {object} user - The user being created
@param {string} user.id - user id
@param {string} user.tenant - Auth0 tenant name
@param {string} user.username - user name
@param {string} user.email - email
@param {boolean} user.emailVerified - is e-mail verified?
@param {string} user.phoneNumber - phone number
@param {boolean} user.phoneNumberVerified - is phone number verified?
@param {object} user.user_metadata - user metadata
@param {object} user.app_metadata - application metadata
@param {object} context - Auth0 connection and other context info
@param {string} context.requestLanguage - language of the client agent
@param {object} context.connection - information about the Auth0 connection
@param {object} context.connection.id - connection id
@param {object} context.connection.name - connection name
@param {object} context.connection.tenant - connection tenant
@param {object} context.webtask - webtask context
@param {function} cb - function (error, response)
*/

/*
 * We require an email list to be present at Gather already. 
 * If the list is not there, we do *not* create one.
 *
 * THIS IS A FEATURE.  It prevents Auth0 from creating a new
 * partial list if we delete the Gather list on purpose.
 * 
 * NOTE:
 * apiKey/spaceId need to match our happy virtual home.
 * 
 * This will fail silently if it doesn't work, with no 
 * messages apparing in any log.  I don't see any 
 * way to log this, barring send a second message to another server.
 * That doesn't seem worth it.
 */

module.exports = function (user, context, cb) {
  const request = require('request');

  request.post(
  {
      url: 'https://gather.town/api/setEmailGuestlist',
      json: {
          "overwrite": false,  // list must exist already.
          "apiKey": "...",
          "spaceId": "aaaaaaaaaaaa\\pldi21",
          "guestlist": {
           // If we provide the name, then users cant' change it to add
           // affiliation, etc.  So, provide empty map without the name.
           // This seems to work, but watch for issues...
           //     [user.email] : { name: user.user_metadata.nname }
           [user.email] : { }
        }
      }
  },
  (err, response, body) => {
    console.log(body);
  });

  cb();
};

