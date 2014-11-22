

from sat import RequestHTTP

http = RequestHTTP('https://api.github.com/')

# Check Plan
plan_schema = {
	'type': 'object', 
	'properties':{
		'name': {'type': 'string'},
		'space': {'type': 'integer'},
		'private_repos': {'type': 'integer'},
		'collaborators': {'type': 'integer'},
	},
	'required': ['name'],}

http('get', 'user', auth=('user', 'password')).expect(200).out('json', 'plan').json(plan_schema, key='plan')

	