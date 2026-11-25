<?php
require 'config.php';$u=require_login();
$routes=['event_join'=>'events.php','event_leave'=>'events.php','complete'=>'resources.php','uncomplete'=>'resources.php','topic'=>'community.php','reply'=>'community.php','profile'=>'profile.php','mentor_request'=>'mentorship.php','mentor_response'=>'mentorship.php','event_save'=>'admin.php','resource_save'=>'admin.php','user_update'=>'admin.php','event_delete'=>'admin.php','resource_delete'=>'admin.php','topic_delete'=>'admin.php','attendance'=>'admin.php'];
$a=(string)($_POST['action']??'');$dest=$routes[$a]??'dashboard.php';
if($_SERVER['REQUEST_METHOD']!=='POST'||!verify_csrf($_POST['csrf']??null)){http_response_code(403);exit('Invalid form token.');}
try{
 $id=filter_var($_POST['id']??0,FILTER_VALIDATE_INT)?:0;$createdId=0;$meaningful=true;
 if(str_starts_with($a,'event_')&&in_array($a,['event_join','event_leave'])){
  if($a==='event_leave'){query('DELETE FROM registrations WHERE user_id=? AND event_id=?',[$u['id'],$id]);}
  else {db()->beginTransaction();$ev=one('SELECT * FROM events WHERE id=? FOR UPDATE',[$id]);if(!$ev||strtotime($ev['starts_at'])<time())throw new RuntimeException('This event is not open for registration.');
   if(one('SELECT user_id FROM registrations WHERE user_id=? AND event_id=?',[$u['id'],$id]))throw new RuntimeException('You have already registered.');
   if(one('SELECT COUNT(*) n FROM registrations WHERE event_id=?',[$id])['n']>=$ev['capacity'])throw new RuntimeException('This event is full.');query('INSERT INTO registrations(user_id,event_id) VALUES(?,?)',[$u['id'],$id]);db()->commit();}
 }elseif(in_array($a,['complete','uncomplete'])){
  if(!one('SELECT id FROM resources WHERE id=?',[$id]))throw new RuntimeException('Resource not found.');
  if($a==='complete')$meaningful=query('INSERT IGNORE INTO progress(user_id,resource_id) VALUES(?,?)',[$u['id'],$id])->rowCount()>0;else query('DELETE FROM progress WHERE user_id=? AND resource_id=?',[$u['id'],$id]);
 }elseif($a==='topic'){query('INSERT INTO topics(user_id,title,body) VALUES(?,?,?)',[$u['id'],text('title',150),text('body')]);$createdId=(int)db()->lastInsertId();$dest='community.php?topic='.$createdId;
 }elseif($a==='reply'){if(!one('SELECT id FROM topics WHERE id=?',[$id]))throw new RuntimeException('Discussion not found.');query('INSERT INTO replies(topic_id,user_id,body) VALUES(?,?,?)',[$id,$u['id'],text('body')]);$createdId=(int)db()->lastInsertId();$dest='community.php?topic='.$id;
 }elseif($a==='profile'){
  $name=text('name',100);$bio=trim((string)($_POST['bio']??''));if(mb_strlen($bio)>5000)throw new RuntimeException('Biography is too long.');$interests=text('interests',190);$photo=$u['photo'];
  if(isset($_FILES['photo'])&&$_FILES['photo']['error']!==UPLOAD_ERR_NO_FILE){$f=$_FILES['photo'];if($f['error']!==UPLOAD_ERR_OK||$f['size']>2*1024*1024)throw new RuntimeException('Use a photo under 2 MB.');$mime=(new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']);$ext=['image/jpeg'=>'jpg','image/png'=>'png','image/webp'=>'webp'][$mime]??null;$dimensions=@getimagesize($f['tmp_name']);if(!$ext||!$dimensions||$dimensions[0]>6000||$dimensions[1]>6000)throw new RuntimeException('Upload a JPG, PNG or WebP image up to 6000 pixels.');$photo=bin2hex(random_bytes(16)).'.'.$ext;if(!move_uploaded_file($f['tmp_name'],__DIR__.'/uploads/'.$photo))throw new RuntimeException('Upload failed. Check uploads folder permissions.');}
  query('UPDATE users SET name=?,bio=?,interests=?,photo=? WHERE id=?',[$name,$bio,$interests,$photo,$u['id']]);
  $pw=(string)($_POST['new_password']??'');if($pw!==''){if(!password_verify((string)($_POST['current_password']??''),$u['password']))throw new RuntimeException('Current password is incorrect. Profile changes have been saved.');if(strlen($pw)<10||strlen($pw)>72||!preg_match('/[A-Za-z]/',$pw)||!preg_match('/[0-9]/',$pw))throw new RuntimeException('New password needs 10–72 characters, letters and a number.');query('UPDATE users SET password=? WHERE id=?',[password_hash($pw,PASSWORD_DEFAULT),$u['id']]);session_regenerate_id(true);}
 }elseif($a==='mentor_request'){
  $mentor=one("SELECT id FROM users WHERE id=? AND role='mentor' AND active=1",[$id]);if(!$mentor||$id===$u['id'])throw new RuntimeException('Select another active mentor.');if(one('SELECT id FROM mentorships WHERE member_id=? AND mentor_id=?',[$u['id'],$id]))throw new RuntimeException('A request already exists for this mentor.');query('INSERT INTO mentorships(member_id,mentor_id,message) VALUES(?,?,?)',[$u['id'],$id,text('message')]);
 }elseif($a==='mentor_response'){
  $status=$_POST['status']??'';if(!in_array($status,['accepted','declined']))throw new RuntimeException('Invalid response.');$request=one("SELECT * FROM mentorships WHERE id=? AND mentor_id=? AND status='pending'",[$id,$u['id']]);if(!$request||$u['role']!=='mentor')throw new RuntimeException('Request not available.');query('UPDATE mentorships SET status=? WHERE id=?',[$status,$id]);
 }else{
  require_admin();
  if($a==='event_save'){$title=text('title',150);$desc=text('description');$start=text('starts_at',30);$dt=DateTime::createFromFormat('Y-m-d\TH:i',$start);if(!$dt)throw new RuntimeException('Enter a valid date and time.');$cap=filter_var($_POST['capacity']??0,FILTER_VALIDATE_INT);if(!$cap||$cap<1||$cap>10000)throw new RuntimeException('Capacity must be 1–10000.');$loc=text('location',190);if($id)query('UPDATE events SET title=?,description=?,starts_at=?,location=?,capacity=? WHERE id=?',[$title,$desc,$dt->format('Y-m-d H:i:s'),$loc,$cap,$id]);else query('INSERT INTO events(title,description,starts_at,location,capacity) VALUES(?,?,?,?,?)',[$title,$desc,$dt->format('Y-m-d H:i:s'),$loc,$cap]);
  }elseif($a==='resource_save'){$vals=[text('title',150),text('category',80),safe_url(text('url',500)),text('description')];if($id)query('UPDATE resources SET title=?,category=?,url=?,description=? WHERE id=?',[...$vals,$id]);else query('INSERT INTO resources(title,category,url,description) VALUES(?,?,?,?)',$vals);
  }elseif($a==='user_update'){
   $role=$_POST['role']??'';$active=($_POST['active']??'0')==='1'?1:0;if(!in_array($role,['member','mentor','admin']))throw new RuntimeException('Invalid role.');
   db()->beginTransaction();$admins=rows("SELECT id FROM users WHERE role='admin' AND active=1 FOR UPDATE");$target=one('SELECT * FROM users WHERE id=?',[$id]);if(!$target)throw new RuntimeException('Member not found.');if($id===$u['id'])throw new RuntimeException('You cannot change your own role or status.');if($target['role']==='admin'&&$target['active']&&count($admins)<=1&&($role!=='admin'||!$active))throw new RuntimeException('Keep at least one active administrator.');query('UPDATE users SET role=?,active=? WHERE id=?',[$role,$active,$id]);db()->commit();
  }elseif(in_array($a,['event_delete','resource_delete','topic_delete'])){$table=['event_delete'=>'events','resource_delete'=>'resources','topic_delete'=>'topics'][$a];query('DELETE FROM '.$table.' WHERE id=?',[$id]);
  }elseif($a==='attendance'){query('UPDATE registrations SET attended=? WHERE event_id=? AND user_id=?',[($_POST['attended']??'0')==='1'?1:0,$id,(int)($_POST['user_id']??0)]);
  }else throw new RuntimeException('Unknown action.');
 }
 if($a==='event_save'&&$id===0)$createdId=(int)db()->lastInsertId();
 audit($u['id'],$a.' #'.$id);after_standard_action($u,$a,$id,$createdId,$meaningful);flash('success','Saved successfully.');
}catch(Throwable $ex){if(db()->inTransaction())db()->rollBack();flash('error',$ex instanceof PDOException?'Could not save this change. Please check for duplicate entries.':$ex->getMessage());}
go($dest);
