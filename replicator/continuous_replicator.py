#!/usr/bin/python

#Copyright 2009 Meebo, Inc.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# install me to /var/lib/lounge/replication_notifier.py

LOG_PATH = '/var/log/lounge/replicator/replication_notifier.log'

import logging
import os
import sys
import simplejson
import socket
socket.setdefaulttimeout(900)
from stat import *
import time
import urllib
import urllib2

import lounge

# TODO some other time use couch.ini for the port
me = 'http://' + socket.getfqdn() + ':5984/'

shard_map = None

def i_dont_host(node):
	return not node.startswith(me)

def do_continuous_replication(source, target):
	try:
		target_host, target_db = target.rsplit('/', 1)
		target_db = urllib.unquote(target_db)
		post_data = simplejson.dumps({"source": source, "target": target_db, "continuous": True})
		urllib2.urlopen(urllib2.Request(
			target_host + "/_replicate", post_data,
			{"Content-Type" : "application/json"}))
	except:
		# don't panic!  keep going to the next record in the queue.
		pass

def replicate(shard):
	# first do full replication
	source = urllib.quote(shard, '')
	local = me + source
	nodes = shard_map.nodes(source)
	if local not in nodes:
		return

	for target in nodes:
		# for full replication, we don't want to replicate to our self.	how silly
		if i_dont_host(target):
			do_continuous_replication(local, target)
	
	# TODO: design doc replication

def load_config(fname):
	global shard_map
	old = shard_map

	shard_map = lounge.ShardMap()
	try:
		pass
	except:
		# config invalid; use old conf
		shard_map = old

def read_config_if_changed(last_read):
	fname = "/etc/lounge/shards.conf"
	mtime = os.stat(fname)[ST_MTIME]
	if last_read is None or mtime > last_read:
		load_config(fname)
		last_read = mtime
	return last_read

def main():
	try:
		logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG)
	except IOError:
		logging.warn("Cannot write to " + LOG_PATH)
		logging.warn("Log messages will be written to stderr instead")
	read_conf_at = None

	logging.info("Starting up")

	while True:
		# wait for a line from the database
		stuff = sys.stdin.readline()
		if not stuff:
			return
		
		try:
			# format: {"type": "updated", "db": "nameofdb"}
			notification = simplejson.loads(stuff) 
		
			# check for updated config
			read_conf_at = read_config_if_changed(read_conf_at) 
		
			# extract the database name
			if notification['type']=='updated':
				db = notification['db'] 
				replicate(db)
		except KeyboardInterrupt:
			sys.exit(1)
		except:
			logging.exception("exception :( --")
			time.sleep(1)
	
if __name__=='__main__':
	main()

# vi: noexpandtab ts=2 sw=2
