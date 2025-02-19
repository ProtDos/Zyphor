# Zyphor - Example 1

## Description

Zyphor - Example 1 demonstrates a simulated communication between Alice and Bob. Users can enter messages directed to either Bob or Alice, and the logs display everything happening in real-time. Unlike the chat visualization in Example 2, this simulation accurately represents how the server handles message exchange.

Additionally, the system simulates a server environment, showing how messages are processed and transmitted.

---

## Features

-   **Simulated Message Exchange:** Enter messages for Alice and Bob, and observe how they are processed.
-   **Real-Time Logging:** Logs display all message transactions and server interactions.
-   **Server Simulation:** The backend emulates real server behavior instead of merely visualizing the chat.
-   **Lightweight and Minimal:** Simple structure, easy to understand and modify.

---

## Example Output

<details>
  <summary>Click to show (long):</summary>

```text
2025-02-19 18:22:44,117 - INFO - Alice: Generating Kyber keypair
2025-02-19 18:22:44,125 - INFO - Alice: Kyber keypair generated. Rotation count: 1
2025-02-19 18:22:44,125 - INFO - Bob: Generating Kyber keypair
2025-02-19 18:22:44,132 - INFO - Bob: Kyber keypair generated. Rotation count: 1
2025-02-19 18:22:44,132 - INFO - Alice: Generating new mailbox ID
2025-02-19 18:22:44,132 - INFO - Alice: New mailbox ID generated: eaf8539dfd7a3723dee5001878d35870
2025-02-19 18:22:44,132 - INFO - Server: Mailbox eaf8539dfd7a3723dee5001878d35870 opened for Alice
2025-02-19 18:22:44,132 - INFO - Bob: Generating new mailbox ID
2025-02-19 18:22:44,132 - INFO - Bob: New mailbox ID generated: 110de1936cffb33a19a8d069c8feea72
2025-02-19 18:22:44,132 - INFO - Server: Mailbox 110de1936cffb33a19a8d069c8feea72 opened for Bob
2025-02-19 18:22:44,142 - INFO - Alice: Shared key: 9ee7a9908b05a0432a48c4bf1a46f197eb0543c0e3578b3624bb8b9a80b2246b generated with b'\xc7\x05\x1e\xb1\xa9\xbc\xa3\xac$\x19'...
2025-02-19 18:22:44,142 - INFO - Alice: MAC key: 4330d2a861058b20194e1476b02446fdbddbda6767600cf36b8d903d5371f475
2025-02-19 18:22:44,153 - INFO - Bob: Shared key derived: 9ee7a9908b05a0432a48c4bf1a46f197eb0543c0e3578b3624bb8b9a80b2246b
2025-02-19 18:22:44,153 - INFO - Bob: MAC key: 4330d2a861058b20194e1476b02446fdbddbda6767600cf36b8d903d5371f475
2025-02-19 18:22:44,161 - INFO - Bob: Shared key: b3977cb911203a0a8126b5a8934db224bacbe543d470ee2c585cd34b55307b88 generated with b'{!&\\\xbb \x89\xd9\xbe|'...
2025-02-19 18:22:44,161 - INFO - Bob: MAC key: 79cd24a868b522b8002a98bb505ec1c32b8a98edf791f8c066512b60d378ac02
2025-02-19 18:22:44,172 - INFO - Alice: Shared key derived: b3977cb911203a0a8126b5a8934db224bacbe543d470ee2c585cd34b55307b88
2025-02-19 18:22:44,172 - INFO - Alice: MAC key: 79cd24a868b522b8002a98bb505ec1c32b8a98edf791f8c066512b60d378ac02
Enter a message for Alice to send to Bob: Test
--------------------
Bob received: Test
2025-02-19 18:22:48,511 - INFO - Alice: Sending message to Bob
2025-02-19 18:22:48,512 - INFO - Alice: Message content: Test
2025-02-19 18:22:48,512 - INFO - Alice: Padded message: 546573740c0c0c0c0c0c0c0c0c0c0c0c
2025-02-19 18:22:48,512 - INFO - Alice: Nonce: 2fa43e5c8f19975958e3f98dac9f87c9
2025-02-19 18:22:48,512 - INFO - Alice: MAC: 0346fdccbde2f935c10d7db474d4e94585213517cfa98ccb22c735c1fdb7dc8d
2025-02-19 18:22:48,512 - INFO - Alice: Ciphertext: d120fee1c13ff567794eef059668c607
2025-02-19 18:22:48,512 - INFO - Server: Forwarding message from Alice to Bob's mailbox
2025-02-19 18:22:48,512 - INFO - Server: Message forwarded to Bob's mailbox 110de1936cffb33a19a8d069c8feea72
2025-02-19 18:22:48,512 - INFO - Alice: Message sent to Bob
2025-02-19 18:22:48,512 - INFO - Server: Retrieving messages for Bob
2025-02-19 18:22:48,512 - INFO - Server: Messages retrieved for Bob
2025-02-19 18:22:48,512 - INFO - Bob: Receiving message from Alice
2025-02-19 18:22:48,512 - INFO - Bob: Received ciphertext: d120fee1c13ff567794eef059668c607
2025-02-19 18:22:48,512 - INFO - Bob: Received nonce: 2fa43e5c8f19975958e3f98dac9f87c9
2025-02-19 18:22:48,512 - INFO - Bob: Received MAC: 0346fdccbde2f935c10d7db474d4e94585213517cfa98ccb22c735c1fdb7dc8d
2025-02-19 18:22:48,513 - INFO - Bob: Verifying MAC
2025-02-19 18:22:48,513 - INFO - Bob: MAC verified
2025-02-19 18:22:48,513 - INFO - Bob: Decrypting message with AES-GCM
2025-02-19 18:22:48,513 - INFO - Bob: Message decrypted
2025-02-19 18:22:48,513 - INFO - Bob: Message received and processed.
2025-02-19 18:22:48,513 - INFO - Bob: Rotating mailbox
2025-02-19 18:22:48,513 - INFO - Bob: Generating new mailbox ID
2025-02-19 18:22:48,513 - INFO - Bob: New mailbox ID generated: 91e387d03aae4c3db4d7179b2fd67fce
2025-02-19 18:22:48,513 - INFO - Bob: Signing mailbox ID
2025-02-19 18:22:48,513 - INFO - Bob: Mailbox ID signed
2025-02-19 18:22:48,513 - INFO - Server: Mailbox 91e387d03aae4c3db4d7179b2fd67fce opened for Bob
2025-02-19 18:22:48,513 - INFO - Bob: Sealing message with Kyber
2025-02-19 18:22:48,522 - INFO - Bob: Message sealed
2025-02-19 18:22:48,522 - INFO - Server: Forwarding notification from Bob to Alice
2025-02-19 18:22:48,523 - INFO - Server: Notification forwarded to Alice's mailbox eaf8539dfd7a3723dee5001878d35870
2025-02-19 18:22:48,523 - INFO - Bob: Mailbox rotated. Rotation count: 1
2025-02-19 18:22:48,523 - INFO - Server: Retrieving messages for Alice
2025-02-19 18:22:48,523 - INFO - Server: Messages retrieved for Alice
2025-02-19 18:22:48,523 - INFO - Alice: Unsealing message with Kyber
Alice updated Bob's mailbox to: 91e387d03aae4c3db4d7179b2fd67fce
2025-02-19 18:22:48,534 - INFO - Alice: Decrypting message with AES-GCM
2025-02-19 18:22:48,534 - INFO - Alice: Message decrypted
2025-02-19 18:22:48,535 - INFO - Alice: Message unsealed
2025-02-19 18:22:48,535 - INFO - Alice: Verifying mailbox ID signature
2025-02-19 18:22:48,535 - INFO - Alice: Mailbox ID signature verified
Enter a message for Bob to send to Alice: Test back
Alice received: Test back
2025-02-19 18:22:54,762 - INFO - Bob: Sending message to Alice
2025-02-19 18:22:54,762 - INFO - Bob: Message content: Test back
2025-02-19 18:22:54,762 - INFO - Bob: Padded message: 54657374206261636b07070707070707
2025-02-19 18:22:54,762 - INFO - Bob: Nonce: 81e2f5b3587d2fd0c9f3b335c79a0c31
2025-02-19 18:22:54,762 - INFO - Bob: MAC: 4fc1985257b6cde13ad3360ebd9b2f79c052b80b859c7d80d2e91fad646a444e
2025-02-19 18:22:54,762 - INFO - Bob: Ciphertext: b36ada9267dc6bad61c51173cf03c9be
2025-02-19 18:22:54,763 - INFO - Server: Forwarding message from Bob to Alice's mailbox
2025-02-19 18:22:54,763 - INFO - Server: Message forwarded to Alice's mailbox eaf8539dfd7a3723dee5001878d35870
2025-02-19 18:22:54,763 - INFO - Bob: Message sent to Alice
2025-02-19 18:22:54,763 - INFO - Server: Retrieving messages for Alice
2025-02-19 18:22:54,763 - INFO - Server: Messages retrieved for Alice
2025-02-19 18:22:54,763 - INFO - Alice: Receiving message from Bob
2025-02-19 18:22:54,763 - INFO - Alice: Received ciphertext: b36ada9267dc6bad61c51173cf03c9be
2025-02-19 18:22:54,763 - INFO - Alice: Received nonce: 81e2f5b3587d2fd0c9f3b335c79a0c31
2025-02-19 18:22:54,763 - INFO - Alice: Received MAC: 4fc1985257b6cde13ad3360ebd9b2f79c052b80b859c7d80d2e91fad646a444e
2025-02-19 18:22:54,763 - INFO - Alice: Verifying MAC
2025-02-19 18:22:54,763 - INFO - Alice: MAC verified
2025-02-19 18:22:54,763 - INFO - Alice: Decrypting message with AES-GCM
2025-02-19 18:22:54,763 - INFO - Alice: Message decrypted
2025-02-19 18:22:54,763 - INFO - Alice: Message received and processed.
```

 </details>

---

## Installation

### Prerequisites

-   Python 3.x installed

### Steps to Install

1. Clone the repository:
    ```sh
    git clone https://github.com/protdos/zyphor.git
    ```
2. Navigate to the project directory:
    ```sh
    cd examples/example1
    ```
3. Install requirements
    ```sh
    pip install -r requirements.txt
    ```

---

## Running the Simulation

To start the simulation, run:

```sh
python3 main.py
```

---

## File Structure

```
kyber_py/    # Contains cryptographic-related Python scripts
main.py      # Main script handling message transactions and logging
```

---

## Disclaimer

Messages are processed in plaintext, and the server does not implement encryption or authentication. This is a simulation, not a secure messaging system.

---

Enjoy exploring Zyphor - Example 1! 🚀
