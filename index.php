<?php
require 'config.php';
$error='';
try {
 if($_SERVER['REQUEST_METHOD']==='POST'){
  if(!verify_csrf($_POST['csrf']??null))throw new RuntimeException('Your form expired. Please try again.');
  $email=strtolower(text('email',190)); $attempt=one('SELECT * FROM login_attempts WHERE email=?',[$email]);
  if($attempt && $attempt['attempts']>=5 && strtotime($attempt['last_attempt'])>time()-900)throw new RuntimeException('Too many attempts. Try again in 15 minutes.');
  $u=one('SELECT * FROM users WHERE email=? AND active=1',[$email]);
  if(!$u || !password_verify((string)($_POST['password']??''),$u['password'])){
   query('INSERT INTO login_attempts(email,attempts,last_attempt) VALUES(?,1,NOW()) ON DUPLICATE KEY UPDATE attempts=IF(last_attempt<DATE_SUB(NOW(),INTERVAL 15 MINUTE),1,attempts+1),last_attempt=NOW()',[$email]);
   throw new RuntimeException('Email or password is incorrect.');
  }
  query('DELETE FROM login_attempts WHERE email=?',[$email]);session_regenerate_id(true);$_SESSION['user_id']=$u['id'];unset($_SESSION['csrf']);audit($u['id'],'Logged in');go('dashboard.php');
 }
 if(current_user())go('dashboard.php');
} catch(PDOException $ex){$error='Database not ready. Follow README.md and run the installer.';}catch(RuntimeException $ex){$error=$ex->getMessage();}
page_start('Welcome');
?>
<section class="landing"><div><p class="eyebrow">A LITTLE COURAGE. A WORLD OF POSSIBILITY.</p><h1>Your next chapter<br>starts with <em>code.</em></h1><p class="lede">A welcoming space for women to learn, build and belong. Meet your people. Find your confidence. Create something that matters.</p><div class="hero-links"><a class="button" href="signup.php">Become a member →</a><a href="#login">Already a member? Sign in</a></div><div class="terminal"><div class="terminal-bar">● ● ● <span>your_future.py</span></div><code><span># Start wherever you are.</span><br>community = "Django Girls"<br>you.learn()<br>you.build()<br><b>possibilities = unlimited</b></code></div><div class="values"><span>01 / Learn together</span><span>02 / Build boldly</span><span>03 / Lift others</span></div></div>
<section class="card auth" id="login"><p class="eyebrow">GOOD TO HAVE YOU HERE</p><h2>Welcome back.</h2><p>Your community is waiting.</p><?php if($error)echo '<div role="alert" class="notice error">'.e($error).'</div>';?><form method="post"><?php csrf();input('Email address','email','email');input('Password','password','password');?><button type="button" class="password-toggle ghost">Show password</button><button class="button full">Sign in →</button></form><p>New here? <a href="signup.php">Create your account</a></p><small>Secure sessions. Real connections.<br>No third-party tracking or plugins.</small></section></section>
<section class="mission"><p class="eyebrow">OUR MISSION</p><h2>Technology is for everyone.<br>So is a seat at this table.</h2><p>Our Freetown learning community connects beginners with practical workshops, open learning resources and supportive mentors. This student-built platform extends the Assignment 1 Django Girls authentication project.</p><img class="original-logo" src="assets/django-girls-logo.svg" alt="Django Girls original project logo"></section>
<?php page_end(false); ?>
