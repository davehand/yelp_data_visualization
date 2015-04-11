/***************************************************************
 * Generic Login code & user account handling
 */
 var last_login = null;
/**
 * Handles UI response to login/logout events
 */
function login_event(is_loggedin, type) {

  if (is_loggedin) {
    last_login = type;
  }

  /* probably some async call we dont care about */
  if (!is_loggedin && last_login == null)
    return;

  if (!is_loggedin) {
      last_login = null;
      /* shut off profile picture */
      document.getElementById('profile-pic').setAttribute('style', 'display: none');
      document.getElementById('profile-pic').setAttribute('src', '');

      /* all google login stuff can be shown except logout button */
      document.getElementById('google-login-details').setAttribute('style', 'display: block');
      document.getElementById('google-login-button').setAttribute('style', 'display: block');
      document.getElementById('google-logout-button').setAttribute('style', 'display: none');

      /* all FB stuff, except profile attributes, can be shown */
      document.getElementById('fb-login-details').setAttribute('style', 'display: block');
      document.getElementById('fb-logged-in-gui').setAttribute('style', 'display: none');
  } else if (type == "facebook") {
      /* shut off google UI, turn on FB profile stuff */
      document.getElementById('google-login-details').setAttribute('style', 'display: none');
      document.getElementById('fb-logged-in-gui').setAttribute('style', 'display: block');

      FB.api("/me/picture?width=50&height=50",  function(response) {
        document.getElementById('profile-pic').setAttribute('style', 'display: block');
        document.getElementById('profile-pic').setAttribute('src', response.data.url);
        console.log('Retrieved Facebook profile picture');
      });  
  } else if (type == "google") {
      document.getElementById('google-login-details').setAttribute('style', 'display: block');
      document.getElementById('google-logout-button').setAttribute('style', 'display: block');
      document.getElementById('google-login-button').setAttribute('style', 'display: none');
      document.getElementById('fb-login-details').setAttribute('style', 'display: none');
      

      /* load user profile & get URL to profile picture */
      gapi.client.load('plus','v1', function() {
      var request = gapi.client.plus.people.get({
          'userId': 'me'
        });
        request.execute(function(resp) {
          if (last_login == 'google') {
            document.getElementById('profile-pic').setAttribute('style', 'display: block');
            document.getElementById('profile-pic').setAttribute('src', resp.image.url);
          }
          console.log('Retrieved Google+ profile picture');
        });
      });
  }
}
 
/***************************************************************
 *
 * GOOGLE LOGIN BELOW
 */
var clientId = '9623654849-crp8t34rpcaeukbsbri3spv8v7qvsbjo.apps.googleusercontent.com';
var apiKey = 'AIzaSyBUo1pyUUbezj2JjvmX21RrCDPIIxW6GaY';
var scopes = 'https://www.googleapis.com/auth/plus.me';
function handleClientLoad() {
  gapi.client.setApiKey(apiKey);
  window.setTimeout(checkAuth,1);
}

function checkAuth() {
  gapi.auth.authorize({
    client_id: clientId, 
    scope: scopes, 
    immediate: true}, handleAuthResult);
}

function signinCallback(authResult) {
  console.log(authResult)
  if (authResult['status']['signed_in']) {
    // Update the app to reflect a signed in user
    // Hide the sign-in button now that the user is authorized, for example:
    login_event(true, "google");
  } else {
    // Update the app to reflect a signed out user
    // Possible error values:
    //   "user_signed_out" - User is signed-out
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatically log in the user
    console.log('Sign-in state: ' + authResult['error']);
    login_event(false, "google");
  }
}

function handleAuthClick(event) {
  gapi.auth.authorize({client_id: clientId, scope: scopes, immediate: false}, handleAuthResult);
  return false;
}

function googleLogin() {
  var additionalParams = {
   'callback': signinCallback
  };
  gapi.auth.signIn(additionalParams);
}

function googleLogout() {
  gapi.auth.signOut();
}

/**
 * Called when Google+ API loads */
function render() {
  var additionalParams = {
    'theme' : 'dark',
    'callback' : 'signinCallback',
  };
  gapi.signin.render('google-login-button', additionalParams);
  if (last_login != null) {
    document.getElementById('google-login-button').setAttribute('style', 'display: none');
  }
}

/***************************************************************
 *
 * FACEBOOK LOGIN BELOW
 */
// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
  console.log('statusChangeCallback');
  console.log(response);
  if (response.status === 'connected') {
    login_event(true, "facebook");
  } else {
    login_event(false, "facebook");
  }
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
}

window.fbAsyncInit = function() {
  FB.init({
    appId      : '780541118709132',
    cookie     : true,
    xfbml      : true,
    version    : 'v2.2'
  });

  // FB.getLoginStatus(function(response) {
  //   statusChangeCallback(response);
  // });
};

// Load the SDK asynchronously
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
