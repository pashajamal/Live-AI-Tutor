# AI Tutor with Tavus

Two small Flask apps that pair an LLM tutor with [Tavus](https://www.tavus.io/) AI video/avatar generation. Ask a question (or start a live session) and get back a talking-head tutor instead of plain text.

## Apps

### `simple.py` — Ask the Tutor → Video
A question/answer flow:
1. You type a question.
2. OpenAI (`gpt-4o`) generates a tutoring script.
3. The script is sent to Tavus to render as a video with your replica.
4. The app polls Tavus until the video is ready, then embeds it.

Runs on **port 5001**.

### `live.py` — Live AI Tutor (embedded)
A real-time conversational flow:
1. You provide optional context (e.g. "we're covering quadratic equations").
2. The app creates a live Tavus conversation using a persona + replica.
3. The returned `conversation_url` is embedded in an iframe so you can talk to the tutor live via camera/mic.

Runs on **port 5002**.

## Requirements

- Python 3.9+
- A [Tavus](https://www.tavus.io/) account with an API key, a replica ID, and (for the live app) a persona ID
- An [OpenAI](https://platform.openai.com/) API key (for `simple.py` only)

## Setup

1. Clone the repo and install dependencies:

   ```bash
   pip install flask requests python-dotenv openai
   ```

2. Create a `.env` file in the project root:

   ```env
   TAVUS_API_KEY=your_tavus_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Replace the placeholder IDs in each script:

   - `simple.py`: set `REPLICA_ID` to your Tavus replica ID.
   - `live.py`: set `PERSONA_ID` and `REPLICA_ID` to your Tavus persona/replica IDs.

## Usage

Run whichever app you want:

```bash
python simple.py   # http://localhost:5001
python live.py      # http://localhost:5002
```

### `simple.py` flow
- Enter a question in the input box.
- The app generates a script, kicks off video rendering, and polls for completion (up to ~2.5 minutes).
- Once ready, the rendered video is shown inline.

### `live.py` flow
- Optionally describe the session context.
- Click **Start Live Call** to spin up a live Tavus conversation.
- Use the embedded iframe (or the shared link) to talk to the tutor via camera/mic.

## Notes & Next Steps

- Both apps run with Flask's `debug=True`, which is fine for local development but should be turned off (and secrets kept out of version control) before any deployment.
- `.env` is expected to hold API keys — make sure it's included in `.gitignore` and never committed.
- The video polling loop in `simple.py` is a simple fixed retry/backoff (30 attempts, 5s apart); consider a webhook-based approach for production use.
- No error handling is shown in the UI if the Tavus or OpenAI calls fail — you may want to add friendlier error states.

## License

Add a license of your choice here (e.g. MIT).