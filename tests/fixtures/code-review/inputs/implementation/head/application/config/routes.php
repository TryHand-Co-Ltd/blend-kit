<?php
$route['scores/show/(:num)']['GET'] = 'Score/show/$1'; // Show an authorized score
$route['scores/raw/(:num)']['GET'] = 'Score/rawExport/$1'; // Export a score
