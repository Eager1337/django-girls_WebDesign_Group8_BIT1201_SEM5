<?php
if(PHP_SAPI!=='cli'){http_response_code(403);exit;}
require dirname(__DIR__).'/config.php';
echo "Optional fictional demo accounts only. Random passwords are not retained.\n";
foreach([['Amie (demo mentor)','mentor','PHP, Web development','I help beginners turn ideas into their first working website.'],['Mariama (demo mentor)','mentor','Python, Git','Start small, ask questions and celebrate every step forward.'],['Fatmata (demo learner)','member','Web development','Learning HTML and CSS, one project at a time.']] as [$n,$role,$i,$b]){
 $e=strtolower(explode(' ',$n)[0]).'@demo.example.test';if(!one('SELECT id FROM users WHERE email=?',[$e]))query('INSERT INTO users(name,email,password,role,interests,bio) VALUES(?,?,?,?,?,?)',[$n,$e,password_hash(bin2hex(random_bytes(24)),PASSWORD_DEFAULT),$role,$i,$b]);
}
$a=one("SELECT id FROM users WHERE role='admin' ORDER BY id LIMIT 1");if($a){query('INSERT IGNORE INTO registrations(user_id,event_id) SELECT ?,id FROM events ORDER BY id LIMIT 1',[$a['id']]);query('INSERT IGNORE INTO progress(user_id,resource_id) SELECT ?,id FROM resources ORDER BY id LIMIT 2',[$a['id']]);}
echo "Demo members added. Disable them in administration when no longer needed.\n";
