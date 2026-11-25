<?php
if(PHP_SAPI!=='cli'){http_response_code(403);exit('Terminal only.');}
require_once dirname(__DIR__).'/config.php';
try {
 if(!one("SHOW TABLES LIKE 'users'"))throw new RuntimeException('Install the base application first.');
 db()->exec(file_get_contents(dirname(__DIR__).'/database/innovations.sql'));
 if(!one('SELECT id FROM challenges LIMIT 1')){
  foreach([
   ['An accessible welcome','Write semantic HTML for a welcome panel containing a heading, a short introduction and a clearly labelled join link. Explain one accessibility decision.'],
   ['A responsive card','Write HTML and CSS for a workshop card that fits both mobile and desktop. Explain how you avoid horizontal overflow.'],
   ['Safe PHP output','Show PHP that safely displays a user-provided biography. Explain why escaping matters. Do not include credentials or private data.'],
   ['A thoughtful query','Write a parameterised PDO query to find resources by category. Explain how placeholders protect the query.'],
   ['A tiny interaction','Write JavaScript for a button that toggles a details panel and updates aria-expanded. Describe the keyboard behaviour.'],
   ['Model your idea','Describe the tables and relationships for a beginner study group. Include primary keys and one foreign key.'],
   ['Build for everyone','Review a form you have built. Suggest three improvements for keyboard users and screen readers, with an example snippet.']
  ] as [$title,$prompt])query('INSERT INTO challenges(title,prompt) VALUES(?,?)',[$title,$prompt]);
 }
 query("INSERT IGNORE INTO app_migrations(version) VALUES('innovations-v1')");
 echo "Innovation upgrade complete. Existing users, photos and content were retained.\n";
}catch(Throwable $ex){fwrite(STDERR,$ex->getMessage()."\n");exit(1);}