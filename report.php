<?php
require 'config.php';require_admin();
$type=($_GET['type']??'members')==='events'?'events':'members';
if($type==='events')$data=rows('SELECT e.title,e.starts_at,e.capacity,COUNT(r.user_id) registrations,COALESCE(SUM(r.attended),0) attended FROM events e LEFT JOIN registrations r ON r.event_id=e.id GROUP BY e.id,e.title,e.starts_at,e.capacity ORDER BY e.starts_at');
else $data=rows('SELECT u.name,u.email,u.role,u.active,u.created_at,(SELECT COUNT(*) FROM registrations r WHERE r.user_id=u.id) events_joined,(SELECT COUNT(*) FROM registrations r WHERE r.user_id=u.id AND attended=1) events_attended,(SELECT COUNT(*) FROM progress p WHERE p.user_id=u.id) lessons_completed,(SELECT COUNT(*) FROM topics t WHERE t.user_id=u.id) topics_started,(SELECT COUNT(*) FROM replies r WHERE r.user_id=u.id) replies FROM users u ORDER BY u.id');
header('Content-Type: text/csv; charset=UTF-8');header('Content-Disposition: attachment; filename="django-girls-'.$type.'.csv"');$f=fopen('php://output','w');
if($data){fputcsv($f,array_keys($data[0]),',','"','');foreach($data as $row){$row=array_map(function($v){$s=(string)$v;return preg_match('/^[=+@\-\t\r]/',$s)?"'".$s:$s;},array_values($row));fputcsv($f,$row,',','"','');}}fclose($f);
