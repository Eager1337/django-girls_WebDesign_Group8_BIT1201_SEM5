<?php
// CLI only: no publicly accessible installation endpoint.
if(PHP_SAPI!=='cli'){http_response_code(403);exit('Run this script from a terminal.');}
require dirname(__DIR__).'/config.php';
try{
 if(one("SHOW TABLES LIKE 'users'")){echo "Tables already exist. Installer does not overwrite data.\n";exit(1);}
 $sql=file_get_contents(dirname(__DIR__).'/database/schema.sql');db()->exec($sql);
 echo "Database tables created.\nAdmin name: ";$name=trim(fgets(STDIN));echo "Admin email: ";$email=strtolower(trim(fgets(STDIN)));echo "Admin password (visible in terminal; 10–72 characters, letters and a number): ";$pw=trim(fgets(STDIN));
 if(!$name||strlen($name)>100||!filter_var($email,FILTER_VALIDATE_EMAIL)||strlen($pw)<10||strlen($pw)>72||!preg_match('/[A-Za-z]/',$pw)||!preg_match('/[0-9]/',$pw))throw new RuntimeException('Invalid admin details. Tables were created; use tools/create-admin.php to finish.');
 query("INSERT INTO users(name,email,password,role,bio,interests) VALUES(?,?,?,'admin',?,?)",[$name,$email,password_hash($pw,PASSWORD_DEFAULT),'Community organiser and lifelong learner.','Web development']);
 require __DIR__.'/seed.php';require __DIR__.'/upgrade.php';echo "Installation complete. Open http://localhost/django-girls/ and sign in.\n";
}catch(Throwable $e){fwrite(STDERR,$e->getMessage()."\nCheck config.local.php and ensure MySQL is running.\n");exit(1);}
