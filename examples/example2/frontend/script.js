function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: false,
    });
  }
  
  async function sendMessage(sender, content) {
    await fetch("https://api.getveilo.com:4566/send_message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender, content }),
    });
  }
  
  function addMessage(sender, content, container) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(
      "message",
      sender === "Alice" ? "sent" : "received"
    );
    messageDiv.textContent = content;
  
    const timestampDiv = document.createElement("div");
    timestampDiv.classList.add("timestamp");
    timestampDiv.textContent = formatTime();
  
    container.appendChild(messageDiv);
    container.appendChild(timestampDiv);
    container.scrollTop = container.scrollHeight;
  }
  
  const aliceInput = document.getElementById("alice-input");
  const bobInput = document.getElementById("bob-input");
  const aliceMessages = document.getElementById("alice-messages");
  const bobMessages = document.getElementById("bob-messages");
  
  aliceInput.addEventListener("keypress", async (e) => {
    if (e.key === "Enter" && aliceInput.value.trim()) {
      const message = aliceInput.value;
      await sendMessage("Alice", message);
      addMessage("Alice", message, aliceMessages);
      addMessage("Bob", message, bobMessages);
      aliceInput.value = "";
    }
  });
  
  bobInput.addEventListener("keypress", async (e) => {
    if (e.key === "Enter" && bobInput.value.trim()) {
      const message = bobInput.value;
      await sendMessage("Bob", message);
      addMessage("Alice", message, bobMessages);
      addMessage("Bob", message, aliceMessages);
      bobInput.value = "";
    }
  });
  