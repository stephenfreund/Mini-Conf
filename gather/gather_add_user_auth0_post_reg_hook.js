
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
function add(user, context, cb) {

    const request = require('request');
  
    request.post(
    {
        url: 'https://gather.town/api/setEmailGuestlist',
        json: {
            "overwrite": true,
            "apiKey": "...",
            "spaceId": "aaaaaaaaaaaa\\pldi21",
            "guestlist": {
                [user.email] : { "name" : user.name }
            }
        },
    },
    (err, response, body) => {
      console.log(body)
    });
}

data = {
      "id": "abc123",
      "tenant": "my-tenant",
      "name" : "cow",
      "username": "user1",
      "email": "...",
      "emailVerified": true,
      "phoneNumber": "1-000-000-0000",
      "phoneNumberVerified": true,
      "user_metadata": {
        "hobby": "surfing"
      },
      "app_metadata": {
        "plan": "full"
      }
    }


add(data, "", "")


