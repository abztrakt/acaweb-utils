<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Testing</title>
    <style>
     input[type="text"] {
       margin:5px;
       font-size:17px;
       height:22px;
       border:1px solid black;
     }

     input[type="submit"] {
       padding:5px;
       font-size:17px;
       background-color:#DDE;
     }

     #real-url {
       font-weight:700;
     }

     .json-area {
       width:1000px; 
       background-color:#FFFFCC; 
       color:#000;
       font-size:13px;
     }

     .radio-area {
       width:450px;
       margin:15px;
       background-color:#EEEEFE
     }
    </style>
    <script src="https://code.jquery.com/jquery-1.11.3.min.js"></script>
  </head>
  <body>
  </body>
</html>
<?php 
/*
  This is an example of how to get json data from the json api
 */

require_once( '/var/www/itconnect/wp-load.php' ); // this is how you can be in WordPress environment
defined( 'ABSPATH' ) || define( 'ABSPATH', '/var/www/itconnect/' ); // sort of unnecessary
require_once( ABSPATH . 'wp-settings.php' );

// Basic Authentication Required
$username = null;
$password = null;

if (isset($_SERVER['PHP_AUTH_USER'])) {
    $username = $_SERVER['PHP_AUTH_USER'];
    $password = $_SERVER['PHP_AUTH_PW'];

} elseif (isset($_SERVER['HTTP_AUTHORIZATION'])) {
    // most other servers
    if (strpos(strtolower($_SERVER['HTTP_AUTHORIZATION']),'basic')===0)
        list($username,$password) = explode(':',base64_decode(substr($_SERVER['HTTP_AUTHORIZATION'], 6)));
 
}
 
if (is_null($username)) {
 
    header('WWW-Authenticate: Basic realm="My Realm"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Text to send if user hits Cancel button';
 
    die();
 
} else {
    echo "<p>How do you do, {$username}.</p>";
    echo "<p>You entered SOME_PASSWORD as your password.</p>";
    echo "<p>Welcome to WP API demo. Remember to put <b>'http://' or 'https://'</b> in front of your URL.</p>";
    
    get_form(); // show the form
    description();

    // Using apache authorization information
    $args = array(
        'headers' => array(
            'Authorization' => 'Basic ' . base64_encode($username . ':' . $password)
        ),
    );

    // Check submit form
    if (isset($_POST['submit_input'])) {
        $request_url = $_POST['url_request'];
        $wp_http = new WP_Http;

        $result = $wp_http->request ($request_url, $args);
        echo "<hr>";
        echo "You requested: <b>$request_url</b> <br>";
        echo "Go to <a href='http://json.parser.online.fr' target='_blank'> JSON Parser Online</a> to simply format the JSON";
        put_json($result['body']);

        // unset because we are done
        unset($_POST['submit_input']);
    }
}

function get_form() {
?>
  <form name="input_form" id="input-form" action="<?php echo $_SERVER['PHP_SELF']; ?>" method="POST">
    <p id="url-to-request">You are about to <u>GET</u><input type="hidden" name="method" id="request-method-hidden"></u> <input type="text" name="url_request" value="" size="100" id="real-url"></p>
    <input type="submit" value="Submit" id="submit-input" name="submit_input" class="submit-btn">
  </form>
<?php
}

function description() {
?>
  <div class="text-description">
    <ul>
      <li>Enter an url above. e.g. http://wonka.cac.washington.edu/itconnect/wp-json/posts</li>
      <li>FYI:</li>
      <ul>
        <li>posts/id/meta</li>
        <li>How you should get custom post type</li>
        <ul>
          <li>example: posts/id?type[]=service</li>
          <li>example: posts/id/meta?type[]=service</li>
        </ul>
        <li>pages/id/meta</li>
        <li>users/id/meta</li>
      </ul>
    </ul>
  </div>
<?php
}

function put_json($str) {
?>
  <div class="json-area" style="">
    <xmp style="word-wrap: break-word; white-space: pre-wrap;">
      <?php echo $str ?>
    </xmp>
  </div>
<?php
}

?>