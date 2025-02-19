# Zyphor - Example 2

## Web Demo

This example is a simple web-based demo that visualizes a chat interaction between two simulated users. While it features a clean UI and engaging animations, it is not a real chat application—messages are sent to the server unencrypted. This project serves as a demonstration rather than a production-ready communication tool.

---

## Features

-   **Simulated Chat Interaction:** A basic conversation between two users is displayed.
-   **Modern UI & Animations:** Smooth animations and a clean, user-friendly interface.
-   **Frontend & Backend Integration:** Messages are sent to a backend server (without encryption).
-   **Minimalistic & Lightweight:** The project is designed for demonstration purposes with a simple file structure.

---

## File Structure

```
/backend
    certs/          # Placeholder for potential certificates (not used in this demo. Needed when hosting on domain)
    kyber_py/       # Contains cryptographic-related Python scripts
    server.py       # Backend server handling messages
/frontend
    index.html      # Main HTML structure of the web interface
    styles.css      # CSS styles for the frontend
    script.js       # JavaScript logic for UI and message interactions
```

---

## How It Works

1. The frontend (HTML, CSS, JS) provides a chat interface where messages appear as if exchanged between two users.
2. When a message is sent, it is transmitted to the backend server (server.py) **without encryption**.
3. The server makes real encryption handeling with the message and shows it nicely. The response on the client side is just simulated though.
4. Various UI animations enhance the visual experience, making the chat feel interactive.

---

## Limitations

-   🚨 **Not Secure:** Messages are sent to the backend unencrypted.
-   🛠️ **No Real User Authentication:** Users are simulated; no real login or authentication process is in place.
-   ⚠️ **Not for Production Use:** This is purely a visualization demo and should not be used as a real chat application.

---

## Setup & Running the Demo

### Prerequisites

-   Python 3.x installed
-   PIP installed

### Steps to Run

1. Clone this repository:
    ```sh
    git clone https://github.com/protdos/zyphor.git
    cd zyphor/examples/example2
    ```
2. Navigate to the backend folder:
    ```sh
    cd backend
    ```
3. Install requirements
    ```sh
    pip install -r requirements.txt
    ```
4. Run the server:
    ```sh
    python3 server.py
    ```
5. Open `frontend/index.html` in a browser to see the frontend in action.

---

Enjoy experimenting with Zyphor! 🚀
