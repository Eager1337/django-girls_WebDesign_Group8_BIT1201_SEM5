<?php
declare(strict_types=1);
// Assignment 1 helpers retained and upgraded from JSON storage to PDO/MySQL.
session_set_cookie_params(['httponly'=>true,'samesite'=>'Lax','secure'=>!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS']!=='off']);
session_start();
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header("Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'self'; form-action 'self'");
header('Referrer-Policy: strict-origin-when-cross-origin');
header('Cache-Control: no-store');
date_default_timezone_set('Africa/Freetown');
require_once __DIR__.'/includes/innovations.php';
function db(): PDO {
 static $pdo;
 if (!$pdo) {
  $c = file_exists(__DIR__.'/config.local.php') ? require __DIR__.'/config.local.php' : [];
  $pdo = new PDO('mysql:host='.($c['host']??'127.0.0.1').';port='.($c['port']??3306).';dbname='.($c['database']??'django_girls').';charset=utf8mb4',$c['user']??'root',$c['password']??'',[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC,PDO::ATTR_EMULATE_PREPARES=>false]);
 }
 return $pdo;
}
function query(string $sql,array $args=[]): PDOStatement { $s=db()->prepare($sql);$s->execute($args);return $s; }
function rows(string $sql,array $args=[]): array {return query($sql,$args)->fetchAll();}
function one(string $sql,array $args=[]): ?array {return query($sql,$args)->fetch() ?: null;}
function e($v): string {return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function csrf_token(): string {return $_SESSION['csrf']??=bin2hex(random_bytes(32));}
function verify_csrf(?string $t): bool {return is_string($t)&&hash_equals(csrf_token(),$t);}
function csrf(): void {echo '<input type="hidden" name="csrf" value="'.e(csrf_token()).'">';}
function go(string $path): never {header('Location: '.$path);exit;}
function flash(string $key,?string $message=null): ?string {if($message!==null){$_SESSION['flash'][$key]=$message;return null;}$v=$_SESSION['flash'][$key]??null;unset($_SESSION['flash'][$key]);return $v;}
function current_user(): ?array {return empty($_SESSION['user_id'])?null:one('SELECT * FROM users WHERE id=? AND active=1',[$_SESSION['user_id']]);}
function require_login(): array {$u=current_user();if(!$u)go('index.php');return $u;}
function require_admin(): array {$u=require_login();if($u['role']!=='admin'){http_response_code(403);exit('Administrator access required.');}return $u;}
function first_name(string $n): string {return explode(' ',trim($n))[0];}
function user_avatar(?array $u, int $size = 32, string $extraClass = ''): string {
    if (!$u) {
        return '<span class="avatar ' . e($extraClass) . '" style="width:' . $size . 'px;height:' . $size . 'px;font-size:' . round($size * 0.42) . 'px;">?</span>';
    }
    $photo = trim((string)($u['photo'] ?? ''));
    $name = (string)($u['name'] ?? 'Member');
    $initial = mb_substr($name, 0, 1) ?: 'U';
    if ($photo !== '' && file_exists(__DIR__ . '/uploads/' . $photo)) {
        return '<img class="avatar-img ' . e($extraClass) . '" src="uploads/' . e($photo) . '" alt="' . e($name) . '" style="width:' . $size . 'px;height:' . $size . 'px;min-width:' . $size . 'px;min-height:' . $size . 'px;border-radius:50%;object-fit:cover;vertical-align:middle;display:inline-block;border:1.5px solid #75d5ff;flex-shrink:0;">';
    }
    return '<span class="avatar ' . e($extraClass) . '" style="width:' . $size . 'px;height:' . $size . 'px;line-height:' . $size . 'px;font-size:' . round($size * 0.42) . 'px;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;flex-shrink:0;">' . e($initial) . '</span>';
}
function audit(int $id,string $action): void {query('INSERT INTO audit_log(user_id,action) VALUES(?,?)',[$id,$action]);}
function text(string $key,int $max=5000): string {$v=trim((string)($_POST[$key]??''));if($v===''||mb_strlen($v)>$max)throw new RuntimeException('Please fill in '.$key.' (maximum '.$max.' characters).');return $v;}
function safe_url(string $s): string {if(!filter_var($s,FILTER_VALIDATE_URL)||!in_array(parse_url($s,PHP_URL_SCHEME),['https','http'],true))throw new RuntimeException('Use a valid http or https URL.');return $s;}
function page_start(string $title,?array $u=null): void {
 if($u)event_reminders((int)$u['id']);
 echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#090a0d"><title>'.e($title).' · Django Girls</title><link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png"><link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-192.png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png"><link rel="shortcut icon" href="favicon.ico"><link rel="stylesheet" href="assets/style.css?v=prism1"><link rel="stylesheet" href="assets/prism.css?v=1"><link rel="stylesheet" href="assets/innovations.css?v=1"><script src="assets/app.js?v=innovations1" defer></script></head><body data-page="'.e(basename($_SERVER['SCRIPT_NAME'],'.php')).'" class="'.($u?'private-view':'public-view').'"><a class="skip" href="#main">Skip to content</a>';
 if($u){echo '<aside class="sidebar"><a class="brand" href="dashboard.php"><span class="brandmark">dg.</span><span>Django Girls<small>FREETOWN COMMUNITY</small></span></a><p class="nav-label">YOUR WORKSPACE</p><nav>';foreach(['dashboard'=>'Overview','events'=>'Events & workshops','resources'=>'Learning library','community'=>'Community','mentorship'=>'Mentorship','members'=>'Members','profile'=>'My profile'] as $p=>$label)echo '<a class="'.(basename($_SERVER['SCRIPT_NAME'])===$p.'.php'?'active':'').'" href="'.$p.'.php">'.e($label).'</a>';if($u['role']==='admin')echo '<a href="admin.php">Administration</a>';echo '</nav><div class="side-bottom"><div class="side-user-row">'.user_avatar($u,36).'<div class="side-user-meta"><strong>'.e($u['name']).'</strong><small>'.e(ucfirst($u['role'])).'</small></div></div><form method="post" action="logout.php">';csrf();echo '<button class="ghost">Sign out</button></form></div></aside><div class="workspace"><header class="topbar"><span>Community / '.e($title).'</span><div class="top-actions"><a class="user-chip" href="profile.php" title="Edit profile">'.user_avatar($u,28).' <span>'.e(first_name($u['name'])).'</span></a><form class="mobile-logout" method="post" action="logout.php">';csrf();echo '<button class="ghost">Sign out</button></form></div></header><main id="main">';}
 else echo '<header class="public-header"><a class="brand" href="index.php"><span class="brandmark">dg.</span>Django Girls</a><nav><a href="index.php">Home & login</a><a class="button" href="signup.php">Join the community</a></nav></header><main id="main" class="public-main">';
 if($u){
  echo '<nav class="innovation-nav" aria-label="Explore innovations">';
  foreach(['hub'=>'Discover','challenges'=>'Daily challenge','showcase'=>'Project lab','calendar'=>'Calendar','search'=>'Search','achievements'=>'Milestones','notifications'=>'Inbox'] as $route=>$label){
   $count=$route==='notifications'&&innovations_ready()?(int)one('SELECT COUNT(*) n FROM notifications WHERE user_id=? AND is_read=0',[$u['id']])['n']:0;
   echo '<a href="'.$route.'.php" '.(basename($_SERVER['SCRIPT_NAME'])===$route.'.php'?'aria-current="page"':'').'>'.e($label).($count?' <span class="unread-count">'.$count.'</span>':'').'</a>';
  }
  echo '</nav>';
  if(!innovations_ready())echo '<div class="notice error">Innovation upgrade needed: back up your database, then run <code>C:\\xampp\\php\\php.exe tools\\upgrade.php</code>. Do not reinstall.</div>';
 }
 foreach(['success','error'] as $key)if($m=flash($key))echo '<div role="alert" class="notice '.$key.'">'.e($m).'</div>';
}
function page_end(bool $private=true): void {echo '</main><footer>© 2026 Django Girls Freetown · Academic community project, not an official Django Girls service.</footer>'.($private?'</div>':'').'</body></html>';}
function heading(string $eyebrow,string $title,string $desc): void {echo '<div class="page-heading"><p class="eyebrow">'.e($eyebrow).'</p><h1>'.e($title).'</h1><p>'.e($desc).'</p></div>';}
function input(string $label,string $name,string $type='text',$value='',bool $required=true): void {echo '<label>'.e($label).'<input type="'.e($type).'" name="'.e($name).'" value="'.e($value).'" '.($required?'required':'').' maxlength="'.($name==='url'?500:190).'"></label>';}
function textarea(string $label,string $name,$value=''): void {echo '<label>'.e($label).'<textarea name="'.e($name).'" required maxlength="5000" rows="4">'.e($value).'</textarea></label>';}