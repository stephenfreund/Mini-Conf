// Original version from mini-conf repo.
//
// Note:
//   - Do not use private browsing tabs.
//   - Do not use Safari unless you have subdomains set up for Auth0.
//
// Both of those cases lead to infinite refresh loops.
// The big question: Are there others?
//

window.onload = async () => {
  const auth0 = await createAuth0Client({
    domain: auth0_domain,
    client_id: auth0_client_id,
    cacheLocation: "localstorage",
  });
  try {
    const token = await auth0.getTokenSilently();
  } catch (error) {
    if (error.error !== "login_required") {
      throw error;
    }
    if (
      window.location.href.includes("index.html") &&
      !window.location.href.includes("static/pldi21")
    ) {
      await auth0.loginWithRedirect({
        redirect_uri: window.location.href,
      });
    } else {
      window.location.href = "../../../index.html";
    }
  }

  // NEW - check for the code and state parameters
  const query = window.location.search;
  if (query.includes("code=") && query.includes("state=")) {
    // Process the login state
    await auth0.handleRedirectCallback();

    // Use replaceState to redirect the user away and remove the querystring parameters
    window.history.replaceState({}, document.title, "/home.html");
  }
};
