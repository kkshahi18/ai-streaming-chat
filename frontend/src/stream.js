export async function readChatStream(body, onChunk, signal) {
  const reader = body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let finished = false;
  const abort = () => { void reader.cancel().catch(() => {}); };
  signal?.addEventListener("abort", abort, { once: true });
  function checkAbort() {
    if (signal?.aborted) throw new DOMException("Generation stopped", "AbortError");
  }
  function processEvents() {
    // Match line endings without normalizing a trailing partial CRLF.
    let boundary;
    while (!finished && (boundary = /\r?\n\r?\n/.exec(buffer))) {
      const event = buffer.slice(0, boundary.index);
      buffer = buffer.slice(boundary.index + boundary[0].length);
      const lines = event.split(/\r?\n/).filter(line => line.startsWith("data:"));
      if (!lines.length) continue;
      const data = JSON.parse(lines.map(line => line.slice(5).replace(/^ /, "")).join("\n"));
      checkAbort();
      if (data.type === "chunk" && typeof data.text === "string") onChunk(data.text);
      else if (data.type === "error") throw new Error(data.message || "AI generation failed");
      else if (data.type === "done") finished = true;
      else throw new Error("Invalid streaming event");
    }
  }
  try {
    checkAbort();
    while (!finished) {
      const { value, done } = await reader.read();
      checkAbort();
      buffer += done ? decoder.decode() : decoder.decode(value, { stream: true });
      processEvents();
      if (done) {
        if (!finished) throw new Error("Response ended unexpectedly. Please try again.");
        break;
      }
    }
  } finally {
    signal?.removeEventListener("abort", abort);
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}
