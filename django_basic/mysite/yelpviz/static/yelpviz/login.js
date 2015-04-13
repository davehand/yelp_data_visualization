/***************************************************************
/**
 * Handles UI response to login/logout events
 */
function login_event(is_loggedin, type) {
  if (!is_loggedin) {
      /* shut off profile picture */
      document.getElementById('profile-pic').setAttribute('style', 'display: none');
      document.getElementById('profile-pic').setAttribute('src', '');

      /* all FB stuff, except profile attributes, can be shown */
      document.getElementById('fb-login-details').setAttribute('style', 'display: block');
      document.getElementById('fb-logged-in-gui').setAttribute('style', 'display: none');
  } else if (type == "facebook") {
      /* shut off google UI, turn on FB profile stuff */
      document.getElementById('fb-logged-in-gui').setAttribute('style', 'display: block');

      FB.api("/me/picture?width=50&height=50",  function(response) {
        document.getElementById('profile-pic').setAttribute('style', 'display: block');
        document.getElementById('profile-pic').setAttribute('src', response.data.url);
        console.log('Retrieved Facebook profile picture');
      });  
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

  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
};

// Load the SDK asynchronously
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
