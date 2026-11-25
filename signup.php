<?php
require 'config.php';$error='';
if($_SERVER['REQUEST_METHOD']==='POST')try{
 if(!verify_csrf($_POST['csrf']??null))throw new RuntimeException('Your form expired. Please try again.');
 $name=text('name',100);$email=strtolower(text('email',190));$password=(string)($_POST['password']??'');
 if(!filter_var($email,FILTER_VALIDATE_EMAIL))throw new RuntimeException('Enter a valid email address.');
 if(strlen($password)<10||strlen($password)>72||!preg_match('/[A-Za-z]/',$password)||!preg_match('/[0-9]/',$password))throw new RuntimeException('Use 10–72 characters with letters and a number.');
 if($password!==($_POST['confirm']??''))throw new RuntimeException('Passwords do not match.');
 if(one('SELECT id FROM users WHERE email=?',[$email]))throw new RuntimeException('This email is already registered.');
 query('INSERT INTO users(name,email,password,interests) VALUES(?,?,?,?)',[$name,$email,password_hash($password,PASSWORD_DEFAULT),text('interests',190)]);
 flash('success','Account created. Sign in to begin your learning journey.');go('index.php');
}catch(PDOException $ex){$error='Could not create account. Check database setup or try a different email.';}catch(RuntimeException $ex){$error=$ex->getMessage();}
page_start('Join us'); ?>
<section class="signup-layout"><div><p class="eyebrow">YOUR FIRST STEP</p><h1>Big ideas.<br>Brave beginnings.</h1><p class="lede">You do not need to be an expert. You just need to be curious.</p><div class="quote">“The best part of learning to code?<br>Not doing it alone.”<small>THE DJANGO GIRLS COMMUNITY</small></div></div><div class="card auth"><h2>Make yourself at home.</h2><p>Create your free community account.</p><?php if($error)echo '<div class="notice error" role="alert">'.e($error).'</div>';?><form method="post"><?php csrf();input('Full name','name','text',$_POST['name']??'');input('Email address','email','email',$_POST['email']??'');?><label>What do you want to learn?
<input list="interest-options" name="interests" value="<?=e($_POST['interests']??'Web development')?>" required maxlength="190" placeholder="Choose a program or type your own…">
<datalist id="interest-options">
  <option value="Web development">
  <option value="Python & Django">
  <option value="HTML, CSS & JavaScript">
  <option value="PHP & MySQL Databases">
  <option value="Backend APIs & Architecture">
  <option value="Data Science & Analytics">
  <option value="UI/UX & Frontend Design">
</datalist></label><?php input('Password (10–72 characters, letters + number)','password','password');input('Confirm password','confirm','password');?><button type="button" class="password-toggle ghost">Show passwords</button><button class="button full">Create my account →</button></form><p>Already a member? <a href="index.php">Sign in</a></p></div></section>
<?php page_end(false); ?>