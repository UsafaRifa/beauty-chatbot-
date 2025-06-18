from flask import Flask, request, jsonify, render_template_string
import openai

openai.api_key = "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"

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Beauty Chatbot 💄</title>
  <style>
    body {
      background: linear-gradient(135deg, #fce4ec, #f8bbd0);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      padding: 40px 20px;
      color: #5a2a5c;
      max-width: 600px;
      margin: auto;
    }
    h1 {
      font-weight: 700;
      font-size: 2.5rem;
      margin-bottom: 20px;
      text-align: center;
      text-shadow: 1px 1px 3px #e91e63aa;
    }
    #chatbox {
      background: white;
      border-radius: 12px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.1);
      padding: 20px;
      min-height: 300px;
      overflow-y: auto;
      margin-bottom: 20px;
      line-height: 1.5;
      font-size: 1.1rem;
      color: #333;
    }
    .user-msg {
      color: #e91e63;
      font-weight: 700;
      margin-top: 15px;
    }
    .bot-msg {
      color: #6a1b9a;
      font-weight: 600;
      margin-top: 8px;
      margin-left: 20px;
      white-space: pre-wrap; /* Preserve new lines */
    }
    form {
      display: flex;
      gap: 10px;
    }
    input[type="text"] {
      flex-grow: 1;
      padding: 12px;
      font-size: 1.1rem;
      border-radius: 8px;
      border: 1px solid #ddd;
      outline: none;
    }
    button {
      padding: 0 20px;
      background: #e91e63;
      color: white;
      border: none;
      border-radius: 8px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.3s;
    }
    button:hover {
      background: #c2185b;
    }
  </style>
</head>
<body>
  <h1>Beauty Chatbot 💄</h1>
  <div id="chatbox"></div>

  <form id="chat-form">
    <input type="text" id="user-input" placeholder="Ask your beauty question..." autocomplete="off" required />
    <button type="submit">Send</button>
  </form>

<script>
  const chatbox = document.getElementById('chatbox');
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');

  function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = sender === 'user' ? 'user-msg' : 'bot-msg';
    msgDiv.textContent = text;
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;  // Scroll to bottom
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userText = input.value.trim();
    if (!userText) return;

    addMessage("You: " + userText, 'user');
    input.value = '';
    input.disabled = true;

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: userText})
      });

      const data = await response.json();
      let botReply = data.reply || "Sorry, no response.";

      // Show full answer without truncation
      addMessage("Bot: " + botReply, 'bot');
    } catch (err) {
      addMessage("Bot: Error connecting to server.", 'bot');
    } finally {
      input.disabled = false;
      input.focus();
    }
  });
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly beauty expert."},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=500
        )
        reply = response.choices[0].message.content.strip() if response.choices[0].message.content else ""
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
