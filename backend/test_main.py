import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import main

class StreamingTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {'GEMINI_API_KEY': 'test-secret'})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.client = TestClient(main.app)

    def events(self, response):
        return [json.loads(x[6:]) for x in response.text.strip().split('\n\n')]

    def test_health(self):
        self.assertEqual(self.client.get('/health').json(), {'status':'ok'})

    def test_empty(self):
        for message in ('', '   '):
            self.assertEqual(self.client.post('/chat/stream', json={'message':message}).status_code, 422)

    def test_missing_key(self):
        with patch.dict(os.environ, {'GEMINI_API_KEY':''}):
            self.assertEqual(self.client.post('/chat/stream', json={'message':'hello'}).status_code, 500)

    @patch('main.genai.Client')
    def test_stream(self, factory):
        client = factory.return_value.__enter__.return_value
        client.models.generate_content_stream.return_value = [SimpleNamespace(text='Hello\n'), SimpleNamespace(text='world')]
        result = self.client.post('/chat/stream', json={'message':'hello'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('text/event-stream', result.headers['content-type'])
        self.assertEqual(self.events(result), [{'type':'chunk','text':'Hello\n'}, {'type':'chunk','text':'world'}, {'type':'done'}])
        factory.return_value.__exit__.assert_called_once()

    @patch('main.genai.Client')
    def test_provider_failure(self, factory):
        exc = RuntimeError('test-secret Authorization: private-header')
        exc.code = 401
        def broken(**kwargs):
            yield SimpleNamespace(text='partial')
            raise exc
        factory.return_value.__enter__.return_value.models.generate_content_stream.side_effect = broken
        with self.assertLogs('uvicorn.error', level='ERROR') as logs:
            result = self.client.post('/chat/stream', json={'message':'hello'})
        events = self.events(result)
        self.assertEqual([e['type'] for e in events], ['chunk','error'])
        self.assertEqual(events[-1]['code'], 401)
        output = result.text + ''.join(logs.output)
        self.assertNotIn('test-secret', output)
        self.assertNotIn('private-header', output)
        self.assertIn('Traceback', output)

    @patch('main.genai.Client')
    def test_empty_generation_fails(self, factory):
        factory.return_value.__enter__.return_value.models.generate_content_stream.return_value = []
        with self.assertLogs('uvicorn.error'):
            events = self.events(self.client.post('/chat/stream', json={'message':'hello'}))
        self.assertEqual(events[0]['type'], 'error')

if __name__ == '__main__':
    unittest.main()
