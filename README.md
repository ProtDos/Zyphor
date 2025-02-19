

# Zyphor: Quantum-Safe Anonymous Chat Protocol

Zyphor is a new cutting-edge, open-source chat protocol designed to provide **end-to-end encryption**, **metadata protection**, and **quantum-safe security** for all types of communication. It focuses on maintaining **full anonymity** for users while ensuring that all transmitted data remains secure, private, and protected against future computational threats. 

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [License](#license)
4. [Getting Started](#getting-started)
5. [Installation](#installation)
6. [Technical Details](#technical-details)
7. [Implementation](#implementation)
8. [Threat Model](#thread-model)
9. [License](#license)
10. [Roadmap](#roadmap)
11. [FAQ](#faq)
12. [Contact](#contact)

---

## Overview

Zyphor provides a robust soluiton for secure, anonymous communication in an era of increasing surveillance and digital threats. By using **quantum-safe encryption algorithms**, Zyphor ensures that your communications remain protected from both current and future cryptographic vulnerabilities.

The protocol is designed for users who prioritize **security**, **privacy**, and **metadata protection** while chatting. Zyphor’s **zero-trust architecture** ensures that no one—except the sender and recipient—can access the contents or metadata of the conversation. Zyphor is centralized, which means it needs a central server to forward messages to the intendent recipient. Below is an overview what the server owner or intruders could theoretically see.

I have developed this protocol so that users still have a fixed username over which they communicate. Other apps like [SimpleX Chat](https://simplex.chat/) don't use such identifiers at all, as even a [session id can be linked to users profiles](https://simplex.chat/#why-ids-bad-for-privacy). But I have decided to still use usernames for two reasons:
1. Ease of use: Users can simply start a chat with a person. Users can post their username and receive messages easily, like with a _normal_ chat app.
2. Design of protocol: Even though my protocol has usernames, my state-of-the-art sealing system makes tracking the amounts of messages a user sent for example impossible.

---


## Key Features

-   **Quantum-Resistant Encryption**: Utilizes the Kyber algorithm, a post-quantum cryptographic method, to ensure that messages remain secure against future quantum computing attacks.
    
-   **Perfect Forward Secrecy (PFS)**: Ensures that past communications remain secure even if long-term keys are compromised.

-   **Sealed Messaging**: Protects sender anonymity by encrypting metadata, making it difficult for third parties to determine who is communicating with whom.
    
-   **Zero-Knowledge Proofs (ZKPs)**: Minimizes metadata exposure by allowing verification of information without revealing the information itself.
    
-   **Onion Routing**: Uses the Tor network to anonymize IP addresses, further protecting user identities.
    
-   **Message Padding**: Adds random data to messages to obscure their length and content, making traffic analysis more difficult.
    
-   **Plausible Deniability**: Implements mechanisms that allow users to deny having sent or received specific messages, even if evidence suggests otherwise.



---

## Getting Started

To start using Zyphor in your own projects, you can use the python example below or create an implementation based off the protocol scheme itself. A practical version of the protocol itself doesn't exist yet.

---

## Installation

Follow the steps below to install the Zyphor Python example in your environment:

### Requirements

- **Operating System**: Linux, macOS, or Windows
- **Dependencies**:
    - Python 3.8+ (or specify your environment’s requirements)
    - Pip
  
### Step 1: Clone the Repository

```bash
git clone https://github.com/ProtDos/zyphor.git
cd zyphor/example
```

### Step 2: Install Dependencies

Use your preferred package manager to install dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Protocol

You will see an example dialog between Alice and Bob and logging during their simulated conversation.
```bash
python3 main.py
```

---


## Technical Details

### Encryption Algorithms

-   **Kyber-1024**: A lattice-based cryptographic algorithm selected by NIST for post-quantum cryptography. Kyber is used for key encapsulation, ensuring secure key exchange.
    
-   **AES-256**: The Advanced Encryption Standard with a 256-bit key is used for symmetric encryption of message content. AES-256 is considered quantum-resistant due to its high security margin against Grover's algorithm.
    

### Security Mechanisms

-   **Perfect Forward Secrecy (PFS)**: Each session uses a unique, temporary key, ensuring that past communications cannot be decrypted even if future keys are compromised. Keys are rotated every few messages or every message. **IMPORTANT:** When rotating every few messages, make this value random, as otherwise after some time the server owner could analyze the traffic and find the communication partners. Kyber allows for a blazingly fast key encapsulation, so using temporary keys for every message is possible. 
    
-   **Sealed Sender**: Encrypts sender information, making it impossible for third parties to determine who sent a message without access to the recipient's private key. Below I explain the newly invented and further developed variant of this, which my protocoll also uses: Sealed Messaging
    
-   **Blind Signatures**: Used in the mailbox system to verify and limit the number of anonymous mailboxes a user can create without revealing their identity. Functions as DDoS protection against malicious actors. This system will be discusses further later on.
    
-   **Ephemeral MACs**: Message Authentication Codes that are periodically regenerated to ensure message integrity and authenticity while maintaining plausible deniability.

As this protocol is designed to be as secure as possible, using an old encryption key (e.g. as a fallback if a message fails) is not possible, as it would open a large security concern. If that happens, it is best to restart the key exchange from ground up.
    

### Metadata Minimization

-   **Onion Routing**: Routes messages through multiple Tor relays to anonymize IP addresses. The Tor-Network as of itself isn't perfect but it's another layer of security.
    
-   **Message Padding**: Adds random data to messages to obscure their true length and content.
    
-   **Zero-Knowledge Proofs (ZKPs)**: Allows verification of information without revealing the information itself, minimizing metadata exposure.
    


## Implementation

### Chat Protocol

<details>
  <summary>Show protocoll</summary>
  ![image](https://github.com/user-attachments/assets/417d2e54-6354-4502-865a-ec4a2e3e2d56)

 </details>
    

### Sealed Messaging System

Zyphor implements a novel mailbox system that allows users to send and receive messages anonymously. [https://zyphor-sealed.netlify.app/](https://zyphor-sealed.netlify.app/) demonstrates the way this system works. Key features include:

-   **Anonymous Mailboxes**: Users can create and manage mailboxes without revealing their identity.
    
-   **Blind Signatures**: Used to verify and limit the number of mailboxes a user can create.
    
-   **Rotating Mailboxes**: Mailbox addresses can be changed periodically to enhance privacy.

All mailboxes are unique and not bound to a user itself. There is also no way to check if a mailbox is registered to a user. Mailboxes can change at any given time. 

<details>
  <summary>Show protocoll</summary>
  ![image](https://github.com/user-attachments/assets/852d36fd-1fca-4f9a-ba28-ffaf3a1b5c55)

 </details>

---

## Comparison with Other Messaging Apps

Zyphor has been designed to surpass the security and privacy features of existing messaging apps. A detailed comparison can be found  [here](https://jufo-2025.netlify.app/compare/).

---

## Challenges and Future Work

While Zyphor represents a significant advancement in secure messaging, there are still challenges to address:

-   **Scalability**: The protocol currently requires a high number of server requests, which can lead to exponential load in large-scale scenarios.
    
-   **Practical Validation**: The protocol has not yet been tested in a real-world environment, and further validation is needed to identify and address potential vulnerabilities.
    
-   **Quantum Resistance**: While Zyphor uses quantum-resistant algorithms, the field of post-quantum cryptography is still evolving, and ongoing research is necessary to ensure long-term security.

---

## Contributing

We welcome contributions! If you'd like to help make Zyphor better, here's how you can get involved:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new pull request.

Before contributing, please review the [Contributing Guide](CONTRIBUTING.md) for detailed instructions on submitting issues, feature requests, and code changes.

---

## Thread Model

### Intended Audience

Zyphor is designed for individuals and organizations that prioritize secure, anonymous communication. The protocol is ideal for:
- Privacy-conscious users who want to protect their conversations from surveillance.
- Whistleblowers, journalists, and activists who need strong anonymity.
- Developers and researchers working on secure messaging systems.
- Any user concerned about post-quantum security and metadata protection.
- Companies wanting to secure their traffic
- Schools or other institutions

### Possible Threat Actors

Zyphor is built to defend against a range of potential attackers, including:
- **Network Adversaries (ISPs, Governments, and Mass Surveillance Programs)**: Attempt to monitor or intercept communication by analyzing network traffic.
- **Malicious Server Operators**: The centralized nature of Zyphor means server operators have some visibility, but protections are in place to limit metadata leakage.
- **Man-in-the-Middle (MitM) Attackers**: Attempt to intercept or modify messages between sender and recipient.
- **Malicious Users**: Individuals attempting to spam, impersonate, or deanonymize other users.
- **Quantum Adversaries**: Attackers with access to future quantum computing resources capable of breaking traditional encryption.

### What an Attacker Can See

- **That a message was sent**: While the contents remain encrypted, an attacker could observe that communication is occurring.
- **Username-based Identifiers**: A malicious server owner could see every registered username and last request this user has done authenticated. This does not include messages sent, but rather just blinding the key or initiating a conversation, as the sealed messaging systems hides those identifiers.

#### Trusting the central server
Users can trust the server as all data linked to it is anonymized and no personal data is stored whatsoever. Like stated above even a compromised server wouldn't compromise a user in any way.


### What an Attacker Cannot See

- **Message Contents**: All communications are end-to-end encrypted using Kyber-1024 and AES-256, making decryption infeasible. Attackers also can't assign a message sent to a user.
- **Sender and Receiver Identities**: The Sealed Messaging System ensures that the actual sender and recipient are unknown to any external observer.
- **Conversation Links**: Due to metadata obfuscation and padding, it's impossible to determine who is communicating with whom based on message flow.
- **Long-term Message Correlation**: Perfect Forward Secrecy (PFS) ensures that even if one session key is compromised, past messages remain secure.
- **IP-Addresses**: The usage of the Tor-network ensures the anonymity of users by hiding their IP-address over multiple layers.



---

## License

Zyphor is licensed under the [**GNU General Public License v3.0 (GPL-3.0)**](LICENSE). You are free to modify, share, and contribute to the project, but you cannot use it for commercial purposes unless you release the modified code under the same license. Please [contact me](mailto:elku001@yahoo.com) if you are interested in using the protocoll in your business.

---

## Roadmap

- **v0.0.1**: Initial alpha protocoll demonstration, no release whatsoever

---

## FAQ

**Q: Is Zyphor compatible with other messaging protocols?**

A: Zyphor is designed to be a standalone, secure chat protocol. However, we are exploring options for inter-protocol communication in future releases.


**Q: How do I ensure my messages are completely anonymous?**

A: Zyphor uses advanced techniques like **Tor routing** and **zero-knowledge proofs** to ensure that no metadata or IP information is exposed during transmission.

---

## Contact

For more information, suggestions, or issues, please contact us at:

- Email: elku001@yahoo.com
- GitHub: [github.com/ProtDos/zyphor](https://github.com/ProtDos/zyphor)
