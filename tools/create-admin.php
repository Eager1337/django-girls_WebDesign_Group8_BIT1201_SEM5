<?php
if(PHP_SAPI!=='cli'){http_response_code(403);exit;}
require dirname(__DIR__).'/config.php';
echo "Recovery admin name: ";$n=trim(fgets(STDIN));echo "Email: ";$e=strtolower(trim(fgets(STDIN)));echo "Password (visible, 10–72 chars, letters + number): ";$p=trim(fgets(STDIN));
if(!$n||strlen($n)>100||!filter_var($e,FILTER_VALIDATE_EMAIL)||strlen($p)<10||strlen($p)>72||!preg_match('/[A-Za-z]/',$p)||!preg_match('/[0-9]/',$p)){fwrite(STDERR,"Invalid details.\n");exit(1);}
query("INSERT INTO users(name,email,password,role) VALUES(?,?,?,'admin')",[$n,$e,password_hash($p,PASSWORD_DEFAULT)]);echo "Administrator created.\n";
