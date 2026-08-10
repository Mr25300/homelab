<?php

$CONFIG = array(
  'filelocking.enabled' => true,
  'memcache.local' => '\OC\Memcache\APCu',
  'memcache.distributed' => '\OC\Memcache\Redis',
  'memcache.locking' => '\OC\Memcache\Redis',
  'redis' => array(
    'host' => 'valkey',
    'port' => 6379,
    'dbindex' => 0,
    'timeout' => 0.0,
  ),
);
