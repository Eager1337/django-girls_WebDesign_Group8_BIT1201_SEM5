<?php
require 'config.php';$u=require_login();
$completed=(int)one('SELECT COUNT(*) n FROM progress WHERE user_id=?',[$u['id']])['n'];$total=(int)one('SELECT COUNT(*) n FROM resources')['n'];
$registered=(int)one('SELECT COUNT(*) n FROM registrations WHERE user_id=?',[$u['id']])['n'];$posts=(int)one('SELECT COUNT(*) n FROM topics WHERE user_id=?',[$u['id']])['n'];$pct=$total?round($completed/$total*100):0;
page_start('Overview',$u);
?>
<section class="dashboard-user-hero">
  <div class="dashboard-user-hero-left">
    <div class="dashboard-user-hero-avatar">
      <?=user_avatar($u, 68)?>
    </div>
    <div class="dashboard-user-hero-info">
      <span class="eyebrow">YOUR LEARNING JOURNEY</span>
      <h1>Hello, <?=e(first_name($u['name']))?>! <span class="badge"><?=e(ucfirst($u['role']))?></span></h1>
      <p class="lede">Focus: <strong><?=e($u['interests'])?></strong> · A little progress every day. A community behind every step.</p>
    </div>
  </div>
  <div class="dashboard-user-hero-action">
    <a href="profile.php" class="button light">Edit profile ✎</a>
  </div>
</section>
<section class="dashboard-hero"><div><span class="pill">MAKE ROOM FOR YOUR POTENTIAL</span><h2>Small steps.<br>Extraordinary futures.</h2><p>Your focus: <?=e($u['interests'])?>. Find your next lesson and keep the momentum going.</p><a class="button light" href="resources.php">Continue learning →</a></div><div class="code-art"><span>&lt;/&gt;</span><small>LEARN. BUILD. BELONG.</small></div></section>
<div class="stats"><?php foreach([[$completed,'Resources completed'],[$registered,'Events joined'],[$posts,'Conversations started'],[$pct.'%','Learning progress']] as [$v,$l])echo '<div><strong>'.e($v).'</strong><span>'.e($l).'</span></div>';?></div>
<div class="two-col"><section class="card"><div class="section-title"><h2>Coming up next</h2><a href="events.php">All events →</a></div><?php $events=rows('SELECT e.*, (SELECT COUNT(*) FROM registrations r WHERE r.event_id=e.id) joined FROM events e WHERE starts_at>=NOW() ORDER BY starts_at LIMIT 3');foreach($events as $ev):?><a class="event-row" href="events.php"><div class="date-box"><strong><?=date('d',strtotime($ev['starts_at']))?></strong><?=strtoupper(date('M',strtotime($ev['starts_at'])))?></div><div><h3><?=e($ev['title'])?></h3><p><?=e($ev['location'])?> · <?=date('H:i',strtotime($ev['starts_at']))?></p></div><span>↗</span></a><?php endforeach;if(!$events)echo '<p>No upcoming events yet. Check back when organisers publish one.</p>';?></section><section class="card"><p class="eyebrow">YOUR NEXT CHAPTER</p><h2>Learning, at your pace.</h2><p><?=$completed?> of <?=$total?> resources completed</p><progress value="<?=$completed?>" max="<?=max(1,$total)?>"><?=$pct?>%</progress><?php $recommend=rows('SELECT * FROM resources WHERE id NOT IN (SELECT resource_id FROM progress WHERE user_id=?) ORDER BY (category LIKE ?) DESC,id LIMIT 2',[$u['id'],'%'.$u['interests'].'%']);foreach($recommend as $r)echo '<a class="learning-row" href="resources.php"><small>'.e($r['category']).'</small><h3>'.e($r['title']).' →</h3></a>';if(!$recommend)echo '<p>You are up to date. Well done!</p>';?></section></div>
<section class="card"><div class="section-title"><h2>From the community</h2><a href="community.php">Join the conversation →</a></div><?php foreach(rows('SELECT t.*,u.name,u.photo FROM topics t JOIN users u ON u.id=t.user_id ORDER BY t.id DESC LIMIT 3') as $t)echo '<a class="discussion-row" href="community.php?topic='.$t['id'].'">'.user_avatar($t, 34).'<div><h3>'.e($t['title']).'</h3><small>'.e($t['name']).' · '.date('d M Y',strtotime($t['created_at'])).'</small></div><span>→</span></a>';?></section>
<?php page_end(); ?>
