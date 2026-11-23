import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readChatStream } from './stream.js';
const encoder = new TextEncoder();
function body(parts) {
  return new ReadableStream({ start(c) { for (const part of parts) c.enqueue(part); c.close(); } });
}
const event = data => `data:${JSON.stringify(data)}\r\n\r\n`;
test('UTF8, CRLF and JSON split at every byte; no duplicate chunks or post-done text', async () => {
  const bytes = encoder.encode(event({type:'chunk',text:'Hello 🌍'}) + event({type:'done'}) + event({type:'chunk',text:'BAD'}));
  let text = '';
  await readChatStream(body(Array.from(bytes, b => Uint8Array.of(b))), s => { text += s; });
  assert.equal(text, 'Hello 🌍');
});
test('provider error fails and cancels reader', async () => {
  await assert.rejects(readChatStream(body([encoder.encode(event({type:'error',message:'Denied'}))]), () => {}), /Denied/);
});
test('truncated stream fails', async () => {
  await assert.rejects(readChatStream(body([encoder.encode('data: {')]), () => {}), /unexpectedly/);
});
test('Stop cancels a pending read and prevents late updates', async () => {
  const controller = new AbortController();
  let cancelled = false;
  const stream = new ReadableStream({ cancel() { cancelled = true; } });
  const result = readChatStream(stream, () => assert.fail('late update'), controller.signal);
  controller.abort();
  await assert.rejects(result, {name:'AbortError'});
  assert.equal(cancelled, true);
});
test('network disconnect propagates', async () => {
  const stream = new ReadableStream({ start(c) { c.error(new Error('Disconnected')); } });
  await assert.rejects(readChatStream(stream, () => {}), /Disconnected/);
});
