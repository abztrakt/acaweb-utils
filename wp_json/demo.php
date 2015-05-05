<?php 
/*
  This is an example of how to get json data from the json api
 */

require_once( '/var/www/itconnect/wp-load.php' ); // this is how you can be in WordPress environment
defined( 'ABSPATH' ) || define( 'ABSPATH', '/var/www/itconnect/' ); // sort of unnecessary
require_once( ABSPATH . 'wp-settings.php' );

$username = null;
$password = null;

if (isset($_SERVER['PHP_AUTH_USER'])) {
    $username = $_SERVER['PHP_AUTH_USER'];
    $password = $_SERVER['PHP_AUTH_PW'];

// most other servers
} elseif (isset($_SERVER['HTTP_AUTHORIZATION'])) {
 
    if (strpos(strtolower($_SERVER['HTTP_AUTHORIZATION']),'basic')===0)
        list($username,$password) = explode(':',base64_decode(substr($_SERVER['HTTP_AUTHORIZATION'], 6)));
 
}
 
if (is_null($username)) {
 
    header('WWW-Authenticate: Basic realm="My Realm"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Text to send if user hits Cancel button';
 
    die();
 
} else {
    echo "<p>Hello {$username}.</p>";
    echo "<p>You entered SOME_PASSWORD as your password.</p>";

    // Using apache authorization information
    $args = array(
        'headers' => array(
            'Authorization' => 'Basic ' . base64_encode($_SERVER['PHP_AUTH_USER'] 
                                                        . ':' . $_SERVER['PHP_AUTH_PW']), 
        ),
    );

    $wp_http = new WP_Http;
    $request_url = "http://wonka.cac.washington.edu/itconnect/wp-json/posts/26556";
    $result = $wp_http->request ($request_url, $args);
    echo "You requested: $request_url <br>";
    echo $result['body'];
}

?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Testing</title>
  </head>
  <body>
    <form >
      
    </form>
  </body>
</html>