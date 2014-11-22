import sys
import json
import requests
from collections import defaultdict
from jsonschema import validate as schema_validate
from jsonschema import ValidationError
from jsonschema import SchemaError

class RequestHTTP:

	def __init__(self, base):

		self.sessions = defaultdict(dict)
		self.base = base
		self.requests = []

	def __call__(self, method, url='', payload=None, headers={}, session_key=None, **kwargs):

		full_url = self.base + url

		#set headers for session key
		if session_key is not None:
			self.sessions[session_key].update(headers)

		session = self.sessions.get(session_key)
		if session is not None:
			headers = session

		r = requests.request(method, full_url, data=json.dumps(payload), headers=headers, **kwargs)

		self.requests.append(r)

		return self

	def expect(self, status):
		'''
		validate the expected return code
		'''
		request = self.last()
		assert status == request.status_code
		return self

	def _json_data(self, key=None):
		request = self.last()
		data = request.json()

		if key is not None:
			return data.get(key)
		return data


	def json(self, schema, key=None, cls=None, *args, **kwargs):
		'''
		will validate the returned json using jsonschema 
		'''
		data = self._json_data(key)

		if data is None:
			print('No data :-(')
			sys.exit()

		try:
			schema_validate(schema, data, *args, **kwargs)
		except ValidationError:

			print('\n >> Validation Error <<')
			print(data)
			print('\n Goodbye :-)')
			sys.exit()
		
		except SchemaError as e:

			print('\n ## You provided a bad schema :-( ##\n')
			print(schema,'\n')
			
			print(e)
			print('\n Goodbye :-)')
			sys.exit()

		return self

	def headers(self, headers):
		'''
		will validate the returned headers using jsonschema
		'''
		print('not implemented.')
		return self

	def out(self, what='text', key=None):
		'''
		print out a component of what is returned.
		'''
		request = self.last()
		thing = getattr(request, what)

		if callable(thing):
			thing = thing()

		if key is not None and isinstance(thing, dict):
			print(thing[key])
		else:
			print(thing) #todo: pretty print?

		return self

	def last(self):
		return self.requests[-1]

