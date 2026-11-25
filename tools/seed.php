<?php
if(PHP_SAPI!=='cli'){http_response_code(403);exit;}
if(!function_exists('db'))require dirname(__DIR__).'/config.php';
if(!one('SELECT id FROM resources LIMIT 1')){
 foreach([
 ['Your first website','Web development','https://developer.mozilla.org/en-US/docs/Learn_web_development','Start with semantic HTML, CSS and browser fundamentals.'],
 ['Django Girls tutorial','Python','https://tutorial.djangogirls.org/en/','A welcoming guide to building a web application with Python and Django.'],
 ['PHP: the first steps','PHP','https://www.php.net/manual/en/tutorial.php','Learn variables, forms and server-side programming from the PHP manual.'],
 ['Design for everyone','Accessibility','https://www.w3.org/WAI/tutorials/','Build accessible navigation, forms and page structures.'],
 ['Version control essentials','Git','https://git-scm.com/book/en/v2','Understand commits, branches and collaborative workflows.'],
 ['Query your first database','SQL','https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/','Understand relational data and SQL through the official MySQL tutorial.']
 ] as $r)query('INSERT INTO resources(title,category,url,description) VALUES(?,?,?,?)',$r);
}
if(!one('SELECT id FROM events LIMIT 1'))foreach([
 ['Build your first web page','Bring your curiosity. Leave with a working HTML and CSS page.','+7 days','Freetown community lab',30],
 ['PHP & MySQL practical lab','Connect your forms to a database and learn safe queries.','+14 days','Limkokwing learning studio',25],
 ['Community project showcase','Share your work, ask questions and celebrate what you have built.','+21 days','Freetown community lab',60]
] as [$t,$d,$when,$loc,$cap])query('INSERT INTO events(title,description,starts_at,location,capacity) VALUES(?,?,?,?,?)',[$t,$d,date('Y-m-d 10:00:00',strtotime($when)),$loc,$cap]);
$admin=one("SELECT id FROM users WHERE role='admin' ORDER BY id LIMIT 1");if($admin&&!one('SELECT id FROM topics LIMIT 1'))query('INSERT INTO topics(user_id,title,body) VALUES(?,?,?)',[$admin['id'],'Welcome to our learning community','Introduce yourself! What are you learning, and what would you love to build? This is a supportive space. Please keep posts respectful and do not share private passwords or personal data.']);
