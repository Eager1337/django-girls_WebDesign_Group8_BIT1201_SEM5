<?php
// CLI only, disposable installation. Temporary state is rolled back.
if(PHP_SAPI!=='cli'){http_response_code(403);exit;}
require dirname(__DIR__).'/config.php';require_innovations();
$checks=0;
function verify_test(string $name,bool $condition):void{global $checks;if(!$condition)throw new RuntimeException('FAIL '.$name);$checks++;echo 'PASS '.$name."\n";}
try{
 db()->beginTransaction();
 query("INSERT INTO users(name,email,password,role) VALUES('Helper Test',?,'unused','member')",['helper-'.bin2hex(random_bytes(8)).'@example.test']);$uid=(int)db()->lastInsertId();
 verify_test('No activity has no streak',learning_streak($uid)===['current'=>0,'best'=>0,'days'=>0]);
 foreach([0,1,2,5,6] as $days)query('INSERT INTO activity_days(user_id,activity_date) VALUES(?,?)',[$uid,date('Y-m-d',strtotime('-'.$days.' days'))]);
 verify_test('Current and best streak include gaps',learning_streak($uid)===['current'=>3,'best'=>3,'days'=>5]);
 record_learning_day($uid);record_learning_day($uid);
 verify_test('Same-day meaningful actions idempotent',learning_streak($uid)['days']===5);
 query('DELETE FROM activity_days WHERE user_id=? AND activity_date=?',[$uid,date('Y-m-d')]);
 verify_test('Yesterday maintains current streak',learning_streak($uid)['current']===2);
 query('DELETE FROM activity_days WHERE user_id=? AND activity_date=?',[$uid,date('Y-m-d',strtotime('-1 day'))]);
 verify_test('Missing yesterday breaks current',learning_streak($uid)['current']===0);
 verify_test('Historical best remains',learning_streak($uid)['best']===2);
 notify_member($uid,'Reminder','events.php','test');notify_member($uid,'Reminder','events.php','test');
 verify_test('Notifications deduplicate',(int)one('SELECT COUNT(*) n FROM notifications WHERE user_id=?',[$uid])['n']===1);
 verify_test('Daily challenge deterministic',daily_challenge('2026-11-21')['id']===daily_challenge('2026-11-21')['id']);
 db()->rollBack();echo "$checks helper checks passed; temporary data rolled back.\n";
}catch(Throwable $e){if(db()->inTransaction())db()->rollBack();fwrite(STDERR,$e->getMessage()."\n");exit(1);}