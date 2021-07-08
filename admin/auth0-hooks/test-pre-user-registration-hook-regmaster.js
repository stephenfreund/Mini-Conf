
const hook = require('./pre-user-registration-hook-regmaster');

const cb = function(error, response) {
    console.log("")
    console.log(`   error: ${JSON.stringify(error)}`)
    console.log(`response: ${JSON.stringify(response, null, 2)}`)
    console.log("")
}

const validUser = {
    "id": "abc123",
    "tenant": "my-tenant",
    "email": "...",
    "name": "Full Name",
    "user_metadata": {
    },
    "app_metadata": {
    }
};

const unpaidUser = {
    "id": "abc123",
    "tenant": "my-tenant",
    "email": "...",
    "name": "Full Name",
    "user_metadata": {
    },
    "app_metadata": {
    }
};

const noUser = {
    "id": "abc123",
    "tenant": "my-tenant",
    "email": "...",
    "name": "Full Name",
    "user_metadata": {
    },
    "app_metadata": {
    }
};



const context = {
    "request": {
        "language": "en-us",
        "ip": "127.0.0.1"
    },
    "connection": {
        "id": "con_xxxxxxxxxxxxxxxx",
        "name": "Username-Password-Authentication",
        "tenant": "my-tenant"
    }
};

hook(validUser, context, cb)
hook(unpaidUser, context, cb)
hook(noUser, context, cb)
