<?php
if(PHP_SAPI!=='cli'){http_response_code(403);exit;}
require dirname(__DIR__).'/config.php';
$file=$argv[1]??'';if(!$file||!is_file($file)){fwrite(STDERR,"Usage: php tools/migrate-assignment1.php path/to/users.json\n");exit(1);}
$users=json_decode(file_get_contents($file),true,512,JSON_THROW_ON_ERROR);$count=0;db()->beginTransaction();
try{foreach($users as $u){$email=strtolower($u['email']??'');$hash=$u['password']??$u['password_hash']??'';$name=$u['name']??$u['full_name']??'Member';if(!filter_var($email,FILTER_VALIDATE_EMAIL)||!password_get_info($hash)['algo'])throw new RuntimeException('Invalid account data. Nothing imported.');if(one('SELECT id FROM users WHERE email=?',[$email]))continue;query('INSERT INTO users(name,email,password) VALUES(?,?,?)',[$name,$email,$hash]);$count++;}db()->commit();echo "Imported $count members. Original password hashes preserved.\n";}catch(Throwable $e){db()->rollBack();fwrite(STDERR,$e->getMessage());exit(1);}
