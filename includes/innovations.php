<?php
// Additive feature helpers. No network services and no submitted-code execution.
function innovations_ready(): bool {
 static $ready;
 if($ready===null){try{$ready=(bool)one("SHOW TABLES LIKE 'app_migrations'") && (bool)one("SELECT version FROM app_migrations WHERE version='innovations-v1'");}catch(PDOException $ex){$ready=false;}}
 return $ready;
}
function require_innovations(): void {if(!innovations_ready()){http_response_code(503);exit('Run PHP tools/upgrade.php in your terminal to enable innovations. Existing data will be retained.');}}
function record_learning_day(int $uid): void {if(innovations_ready())query('INSERT IGNORE INTO activity_days(user_id,activity_date) VALUES(?,?)',[$uid,date('Y-m-d')]);}
function learning_streak(int $uid): array {
 $dates=array_column(rows('SELECT activity_date FROM activity_days WHERE user_id=? ORDER BY activity_date DESC',[$uid]),'activity_date');
 $set=array_fill_keys($dates,true);$cursor=new DateTimeImmutable('today');
 if(!isset($set[$cursor->format('Y-m-d')]))$cursor=$cursor->modify('-1 day');
 $current=0;while(isset($set[$cursor->format('Y-m-d')])){$current++;$cursor=$cursor->modify('-1 day');}
 $best=0;$run=0;$previous=null;foreach(array_reverse($dates) as $date){$dt=new DateTimeImmutable($date);$run=($previous && $previous->modify('+1 day')->format('Y-m-d')===$date)?$run+1:1;$best=max($best,$run);$previous=$dt;}
 return ['current'=>$current,'best'=>$best,'days'=>count($dates)];
}
function daily_challenge(?string $day=null): ?array {
 $day??=date('Y-m-d');$all=rows('SELECT * FROM challenges WHERE active=1 ORDER BY id');
 if(!$all)return null;$index=(int)floor((new DateTimeImmutable($day))->getTimestamp()/86400)%count($all);return $all[$index];
}
function notify_member(int $uid,string $message,string $url,string $key): void {
 if(innovations_ready())query('INSERT IGNORE INTO notifications(user_id,message,url,dedupe_key) SELECT id,?,?,? FROM users WHERE id=? AND active=1',[$message,$url,$key,$uid]);
}
function feed_publish(int $uid,string $kind,string $title,string $url,int $source=0): void {
 if(innovations_ready())query('INSERT INTO activity_feed(user_id,kind,title,url,source_id) VALUES(?,?,?,?,?)',[$uid,$kind,$title,$url,$source]);
}
function event_reminders(int $uid): void {
 if(!innovations_ready())return;
 foreach(rows('SELECT e.id,e.title FROM registrations r JOIN events e ON e.id=r.event_id WHERE r.user_id=? AND e.starts_at BETWEEN NOW() AND DATE_ADD(NOW(),INTERVAL 48 HOUR)',[$uid]) as $event)notify_member($uid,'Coming up: '.$event['title'],'events.php','reminder-'.$event['id']);
}
function innovation_hidden(string $action,int $id=0): void {csrf();echo '<input type="hidden" name="action" value="'.e($action).'"><input type="hidden" name="id" value="'.$id.'">';}
function after_standard_action(array $u,string $action,int $id,int $createdId=0,bool $meaningful=true): void {
 if(!innovations_ready())return;
 if($meaningful&&in_array($action,['complete','topic','reply']))record_learning_day((int)$u['id']);
 if($action==='complete'){
  $r=one('SELECT title FROM resources WHERE id=?',[$id]);
  if($r&&!one("SELECT id FROM activity_feed WHERE user_id=? AND kind='learning' AND source_id=?",[$u['id'],$id]))feed_publish((int)$u['id'],'learning','Completed '.$r['title'],'resources.php',$id);
 }
 if($action==='topic'){$t=one('SELECT id,title FROM topics WHERE id=? AND user_id=?',[$createdId,$u['id']]);if($t)feed_publish((int)$u['id'],'topic',$t['title'],'community.php?topic='.$t['id'],(int)$t['id']);}
 if($action==='reply'){
  $t=one('SELECT user_id,title FROM topics WHERE id=?',[$id]);$r=one('SELECT id FROM replies WHERE id=? AND topic_id=? AND user_id=?',[$createdId,$id,$u['id']]);
  if($t&&$r&&$t['user_id']!=$u['id'])notify_member((int)$t['user_id'],$u['name'].' replied to your discussion.','community.php?topic='.$id,'reply-'.$r['id']);
 }
 if($action==='mentor_request'){$r=one('SELECT id FROM mentorships WHERE member_id=? AND mentor_id=?',[$u['id'],$id]);if($r)notify_member($id,$u['name'].' requested mentorship.','mentorship.php','request-'.$r['id']);}
 if($action==='mentor_response'){$r=one('SELECT member_id,status FROM mentorships WHERE id=?',[$id]);if($r)notify_member((int)$r['member_id'],'Your mentorship request was '.$r['status'].'.','mentorship.php','response-'.$id);}
 if($action==='event_save'&&$id===0){$ev=one('SELECT id,title FROM events WHERE id=?',[$createdId]);if($ev)foreach(rows('SELECT id FROM users WHERE active=1 AND id<>?',[$u['id']]) as $member)notify_member((int)$member['id'],'New workshop: '.$ev['title'],'events.php','new-event-'.$ev['id']);}
 if(in_array($action,['topic_delete','resource_delete']))query('DELETE FROM activity_feed WHERE kind=? AND source_id=?',[$action==='topic_delete'?'topic':'learning',$id]);
}