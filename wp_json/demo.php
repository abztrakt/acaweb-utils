<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Testing</title>
    <style>
     input[type="text"] {
       margin:5px;
     }
    </style>
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

    // Using apache authorization information
    $args = array(
        'headers' => array(
            'Authorization' => 'Basic ' . base64_encode($_SERVER['PHP_AUTH_USER'] 
                                                        . ':' . $_SERVER['PHP_AUTH_PW']), 
        ),
    );

    // Check submit form
    if (isset($_POST['submit_input'])) {
        $request_url = $_POST['url_input'];
        $wp_http = new WP_Http;

        $result = $wp_http->request ($request_url, $args);
        echo "You requested: <b>$request_url</b> <br>";
        echo "Go to <a href='http://json.parser.online.fr' target='_blank'> JSON Parser Online</a> to simply format the JSON";
        put_json($result['body']);

        // unset because we are done
        unset($_POST['submit_input']);
    }
}

function get_form() {
?>
  <form name="input_form" id="input-form" action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">
    <input type="text" placeholder="Your base url. E.g. http://wonka.cac.washington.edu/itconnect/wp-json" name="url_base" id="url-base" size="80"><br>
    <!--input type="text" placeholder="Enter a url here" name="url_input" id="url-input" size="100"-->
    <input type="radio" name="type" value="post" checked>post<input type="text" placeholder="post id" name="post_id" style="display:none" id="post-id" size="20"><br>
    <input type="radio" name="type" value="page">page<input type="text" placeholder="page id" name="page_id" style="display:none" id="page-id" size="20"><br>
    <input type="radio" name="type" value="custom">custom<input type="text" placeholder="custom type id" name="custom_id" style="display:none" id="custom-id" size="20"><br>
    <input type=text" placeholder="custom type" name="custom_type" style="display:none" id="custom-type" size="40">
    <p id="url-to-request">You are about to request <b></b></p>
    <input type="submit" value="Submit" id="submit-input" name="submit_input" class="submit-btn">
  </form>
<?php
}

function put_json($str) {
?>
  <div class="json-area" style="width:960px; background-color:grey; color:#FFF">
    <pre style="word-wrap: break-word; white-space: pre-wrap;">
      <?php echo $str ?>
    </pre>
  </div>
<?php
}

?>