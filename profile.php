<?php require 'config.php';$u=require_login();page_start('My profile',$u);heading('THIS IS YOUR SPACE','Tell your story.','Share what you are learning and help your community get to know you.'); ?>
<div class="two-col">
  <section class="card">
    <div style="margin-bottom:16px;">
      <?=user_avatar($u, 110, 'profile-photo')?>
    </div>
    <h2><?=e($u['name'])?></h2>
    <span class="badge"><?=e(ucfirst($u['role']))?></span>
    <p><?=e($u['email'])?></p>
    <p class="body-text"><?=e($u['bio']?:'Your story is just getting started.')?></p>
    <p class="meta">Joined <?=date('d M Y',strtotime($u['created_at']))?><br>Interests: <?=e($u['interests'])?></p>
  </section>
  <form class="card" method="post" action="action.php" enctype="multipart/form-data">
    <?php csrf();?>
    <input type="hidden" name="action" value="profile">
    <h2>Edit your profile</h2>
    <?php input('Full name','name','text',$u['name']);input('Learning interests','interests','text',$u['interests']);?>
    <label>Biography<textarea name="bio" rows="4" maxlength="5000"><?=e($u['bio'])?></textarea></label>
    <label>Profile photo (JPG, PNG or WebP, max 2 MB)
      <input type="file" name="photo" accept="image/jpeg,image/png,image/webp">
      <small style="display:block;margin-top:4px;color:var(--muted);">Your photo will appear on your dashboard, top navigation, community posts and member cards.</small>
    </label>
    <details>
      <summary>Change password (optional)</summary>
      <?php input('Current password','current_password','password','',false);input('New password (10–72 characters, letters + number)','new_password','password','',false);?>
    </details>
    <button class="button">Save profile →</button>
  </form>
</div>
<?php page_end(); ?>
