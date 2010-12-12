import re
import cjson

class ShardMap(object):
	def __init__(self, fname=None):
		if fname is None:
			fname = "/etc/lounge/shards.conf"
		self.load_config(fname)
		self.get_db_shard = re.compile(r'^(.*\D)(\d+)$')
	
	def load_config(self, fname):
		self.config = cjson.decode(file(fname).read())
		self.shardmap = self.config["shard_map"]
		self.nodelist = self.config["nodes"]
		self.dupsets = self.config.get("dup_shards", [])
	
	def get_db_from_shard(self, shard):
		"""Strip out the shard index from a shard name.
		Ex: in -- userinfo41
		   out -- userinfo
		"""
		return self.get_db_shard.sub(r'\1', shard)

	def get_index_from_shard(self, shard):
		"""Strip out the db name from a shard name.
		Ex: in -- userinfo41
		   out -- 41 
		"""
		return int(self.get_db_shard.sub(r'\2', shard))
	
	def shards(self, dbname):
		return ["%s%d" % (dbname, i) for i in len(self.shardmap)]

	def unique_shards(self, dbname):
		unique_shards = list(reduce(
			lambda acc, dup: acc.difference(dup[1:]),
			self.dupsets,
			set(range(len(self.shardmap)))))
		unique_shards.sort()
		return ["%s%d" % (dbname, i) for i in unique_shards]
	
	def nodes(self, shard=None):
		"""Return a list of nodes holding a particular shard.
		Ex: in -- userinfo41
		   out -- [http://bfp6:5984/userinfo41, http://bfp7:5984/userinfo41, http://bfp9:5984/userinfo41]

		If shard is not given, return the node list with no db name.
		Ex:
		  out -- [http://bfp6:5984/, http://bfp7:5984/, http://bfp9:5984]
		"""
		if shard is None:
			return [str("http://%s:%d/" % (host, port)) for host, port in self.nodelist]
		else:
			dbname = self.get_db_from_shard(shard)
			shard_index = int(shard.strip(dbname))
			# unicode will mess up stuff like curl, so we convert to plain str
			return [str("http://%s:%d/%s" % (host,port,shard)) for host, port in [self.nodelist[i] for i in self.shardmap[shard_index]]]
	
	def primary_shards(self, dbname, unique=False):
		"""Return the complete URL of each primary shard for a given database.

		Ex: in -- userinfo
		   out -- [http://server1:5984/userinfo1, http://server2:5984/userinfo2, http://server1:5984/userinfo3 ..]
		"""
		shards = unique and self.unique_shards(dbname) or self.shards(dbname)
		return [self.nodes(s)[0] for s in shards]

# vi: noexpandtab ts=2 sw=2
