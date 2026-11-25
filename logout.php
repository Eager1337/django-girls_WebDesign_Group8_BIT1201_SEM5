<?php
require 'config.php';
if($_SERVER['REQUEST_METHOD']!=='POST'||!verify_csrf($_POST['csrf']??null)){http_response_code(403);exit('Invalid logout request.');}
$_SESSION=[];$p=session_get_cookie_params();setcookie(session_name(),'',time()-42000,$p['path'],$p['domain'],$p['secure'],$p['httponly']);session_destroy();go('index.php');
