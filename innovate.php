<?php
require 'config.php';$u=require_login();require_innovations();
if($_SERVER['REQUEST_METHOD']!=='POST'||!verify_csrf($_POST['csrf']??null)){http_response_code(403);exit('Invalid form token.');}
$a=(string)($_POST['action']??'');$id=filter_var($_POST['id']??0,FILTER_VALIDATE_INT)?:0;
$routes=['submit_challenge'=>'challenges.php','review_challenge'=>'challenges.php','save_challenge'=>'challenges.php','project'=>'showcase.php','feedback'=>'showcase.php','project_delete'=>'showcase.php','feedback_delete'=>'showcase.php','reaction'=>'hub.php','read_notification'=>'notifications.php','read_all'=>'notifications.php'];$dest=$routes[$a]??'hub.php';
try{
 if($a==='submit_challenge'){
  $challenge=daily_challenge();if(!$challenge||$id!=$challenge['id'])throw new RuntimeException('The daily challenge changed. Refresh and try again.');
  $solution=text('solution',12000);$date=date('Y-m-d');
  db()->beginTransaction();
  one('SELECT id FROM users WHERE id=? FOR UPDATE',[$u['id']]);
  $old=one('SELECT * FROM challenge_submissions WHERE user_id=? AND challenge_date=?',[$u['id'],$date]);
  if($old&&$old['status']==='approved')throw new RuntimeException('An approved submission cannot be changed. Try the next daily challenge.');
  query("INSERT INTO challenge_submissions(user_id,challenge_id,challenge_date,solution) VALUES(?,?,?,?) ON DUPLICATE KEY UPDATE solution=VALUES(solution),status='submitted',review=NULL",[$u['id'],$id,$date,$solution]);
  record_learning_day((int)$u['id']);
  db()->commit();
 }elseif($a==='review_challenge'){
  require_admin();$s=one('SELECT * FROM challenge_submissions WHERE id=?',[$id]);if(!$s)throw new RuntimeException('Submission not found.');
  db()->beginTransaction();one('SELECT id FROM users WHERE id=? FOR UPDATE',[$s['user_id']]);
  $status=$_POST['status']??'';if(!in_array($status,['approved','needs_work']))throw new RuntimeException('Choose a review decision.');
  $review=text('review',1000);query('UPDATE challenge_submissions SET status=?,review=? WHERE id=?',[$status,$review,$id]);
  notify_member((int)$s['user_id'],'Your coding challenge has new feedback.','challenges.php','review-'.$id.'-'.hash('sha256',$review.$status));
  if($status==='approved'&&!one("SELECT id FROM activity_feed WHERE kind='challenge' AND source_id=?",[$id]))feed_publish((int)$s['user_id'],'challenge','Earned a challenge approval','achievements.php',$id);
  db()->commit();
 }elseif($a==='save_challenge'){
  require_admin();$title=text('title',150);$prompt=text('prompt',5000);$difficulty=$_POST['difficulty']??'';if(!in_array($difficulty,['Beginner','Intermediate']))throw new RuntimeException('Invalid difficulty.');
  query('INSERT INTO challenges(title,prompt,difficulty) VALUES(?,?,?)',[$title,$prompt,$difficulty]);
 }elseif($a==='project'){
  $title=text('title',150);$desc=text('description',5000);$url=trim((string)($_POST['url']??''));if(strlen($url)>500)throw new RuntimeException('URL too long.');if($url!=='')$url=safe_url($url);
  query('INSERT INTO projects(user_id,title,description,url) VALUES(?,?,?,?)',[$u['id'],$title,$desc,$url?:null]);$pid=(int)db()->lastInsertId();
  feed_publish((int)$u['id'],'project','Published '.$title,'showcase.php?project='.$pid,$pid);record_learning_day((int)$u['id']);$dest='showcase.php?project='.$pid;
 }elseif($a==='feedback'){
  $project=one('SELECT * FROM projects WHERE id=?',[$id]);if(!$project)throw new RuntimeException('Project not found.');
  query('INSERT INTO project_feedback(project_id,user_id,body) VALUES(?,?,?)',[$id,$u['id'],text('body',3000)]);$fid=(int)db()->lastInsertId();
  if($project['user_id']!=$u['id'])notify_member((int)$project['user_id'],$u['name'].' left feedback on your project.','showcase.php?project='.$id,'feedback-'.$fid);
  record_learning_day((int)$u['id']);$dest='showcase.php?project='.$id;
 }elseif($a==='project_delete'){
  $project=one('SELECT * FROM projects WHERE id=?',[$id]);if(!$project||($project['user_id']!=$u['id']&&$u['role']!=='admin'))throw new RuntimeException('You cannot remove this project.');
  db()->beginTransaction();query("DELETE FROM activity_feed WHERE kind='project' AND source_id=?",[$id]);query('DELETE FROM projects WHERE id=?',[$id]);db()->commit();
 }elseif($a==='feedback_delete'){
  require_admin();query('DELETE FROM project_feedback WHERE id=?',[$id]);
 }elseif($a==='reaction'){
  if(!one('SELECT f.id FROM activity_feed f JOIN users u ON u.id=f.user_id WHERE f.id=? AND u.active=1',[$id]))throw new RuntimeException('Activity not found.');
  $mode=$_POST['mode']??'';if($mode==='remove')query('DELETE FROM feed_reactions WHERE feed_id=? AND user_id=?',[$id,$u['id']]);elseif($mode==='add')query('INSERT IGNORE INTO feed_reactions(feed_id,user_id) VALUES(?,?)',[$id,$u['id']]);else throw new RuntimeException('Invalid reaction.');
 }elseif($a==='read_notification'){
  query('UPDATE notifications SET is_read=1 WHERE id=? AND user_id=?',[$id,$u['id']]);
 }elseif($a==='read_all'){
  query('UPDATE notifications SET is_read=1 WHERE user_id=?',[$u['id']]);
 }else throw new RuntimeException('Unknown action.');
 audit((int)$u['id'],$a.' #'.$id);flash('success','Saved successfully.');
}catch(Throwable $ex){if(db()->inTransaction())db()->rollBack();flash('error',$ex instanceof PDOException?'Could not save this change. Please try again.':$ex->getMessage());}
go($dest);