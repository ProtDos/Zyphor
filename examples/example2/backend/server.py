from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import hmac
import logging
import os
import secrets
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from kyber_py.kyber import Kyber1024
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Configure logging with colorama
class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        message = super().format(record)
        return log_color + message

handler = logging.StreamHandler()
formatter = ColorFormatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[handler])


class User:
    def __init__(self, name):
        self.name = name
        self.mailbox = None
        self.current_kyber_pk = None
        self.current_kyber_sk = None
        self.shared_key = None
        self.mac_key = secrets.token_bytes(32)  # AES key size
        self.last_known_key = None
        self.mailbox_rotation_counter = 0
        self.kyber_rotation_counter = 0
        self.mailbox_id_signature_key = secrets.token_bytes(32)
        self.mailbox_id_signature_algorithm = "sha256"
        self.generate_kyber_keypair()
        self.blinded_key = None
        self.blinded_key_signature = None

    def generate_kyber_keypair(self):
        logging.info(f"{self.name}: Generating Kyber keypair")
        self.current_kyber_pk, self.current_kyber_sk = Kyber1024.keygen()
        self.kyber_rotation_counter += 1
        logging.info(
            f"{self.name}: Kyber keypair generated. Rotation count: {self.kyber_rotation_counter}"
        )

    def generate_mailbox_id(self):
        logging.info(f"{self.name}: Generating new mailbox ID")
        mailbox_id = secrets.token_hex(16)  # 32 characters
        logging.info(f"{self.name}: New mailbox ID generated: {Fore.LIGHTCYAN_EX}{mailbox_id}")
        return mailbox_id

    def sign_mailbox_id(self, mailbox_id):
        logging.info(f"{self.name}: Signing mailbox ID")
        message = mailbox_id.encode("utf-8")
        signature = hmac.new(
            self.mailbox_id_signature_key,
            message,
            hashlib.sha256,  # Use hashlib.sha256 directly
        ).hexdigest()
        logging.info(f"{self.name}: Mailbox ID signed")
        return signature

    def verify_mailbox_id_signature(self, mailbox_id, signature, signature_key):
        logging.info(f"{self.name}: Verifying mailbox ID signature")
        message = mailbox_id.encode("utf-8")
        expected_signature = hmac.new(
            signature_key,
            message,
            hashlib.sha256,  # Use hashlib.sha256 directly
        ).hexdigest()
        if hmac.compare_digest(signature, expected_signature):
            logging.info(f"{self.name}: Mailbox ID signature verified")
            return True
        else:
            logging.warning(f"{self.name}: Mailbox ID signature verification failed")
            return False

    def rotate_mailbox(self, server, notify_user):
        logging.info(f"{self.name}: Rotating mailbox")
        new_mailbox_id = self.generate_mailbox_id()
        signature = self.sign_mailbox_id(new_mailbox_id)
        server.open_mailbox(self, new_mailbox_id)
        # Include the signature key in the notification
        notification_data = f"{new_mailbox_id}|{signature}|{self.mailbox_id_signature_key.hex()}"
        sealed_notification = self.seal_message(
            notification_data, notify_user.current_kyber_pk
        )
        # Simulate sending via TOR
        server.forward_notification(self, notify_user, sealed_notification)
        self.mailbox_rotation_counter += 1
        logging.info(
            f"{self.name}: Mailbox rotated. Rotation count: {self.mailbox_rotation_counter}"
        )

    def generate_shared_key(self, other_pk):
        # logging.info(f"{self.name}: Generating shared key with {other_pk[:10]}...")
        shared_secret, ciphertext = Kyber1024.encaps(other_pk)
        self.shared_key = self.derive_key(shared_secret)
        self.mac_key = self.derive_key(shared_secret, info=b"mac key", length=32)

        # logging.info(f"{self.name}: Shared key generated.")
        logging.info(f"{self.name}: Shared key: {Fore.LIGHTCYAN_EX}{self.shared_key.hex()}{Fore.GREEN} generated with {Fore.LIGHTCYAN_EX}{other_pk[:10]}...")
        logging.info(f"{self.name}: MAC key: {Fore.LIGHTCYAN_EX}{self.mac_key.hex()}")
        return ciphertext

    def derive_shared_key(self, ciphertext):
        # logging.info(f"{self.name}: Deriving shared key from ciphertext.")
        shared_secret = Kyber1024.decaps(self.current_kyber_sk, ciphertext)
        self.shared_key = self.derive_key(shared_secret)
        self.mac_key = self.derive_key(shared_secret, info=b"mac key", length=32)

        #nlogging.info(f"{self.name}: Shared key derived.")
        logging.info(f"{self.name}: Shared key derived: {Fore.LIGHTCYAN_EX}{self.shared_key.hex()}")
        logging.info(f"{self.name}: MAC key: {Fore.LIGHTCYAN_EX}{self.mac_key.hex()}")

    def derive_key(self, shared_secret, salt=None, info=b"application specific info", length=32):
        """Derives a key from a shared secret using HKDF."""
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            info=info,
            backend=default_backend()
        )
        return hkdf.derive(shared_secret)

    def pad_message(self, message):
        # logging.info(f"{self.name}: Padding message")
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(message) + padder.finalize()
        # logging.info(f"{self.name}: Message padded")
        return padded_data

    def unpad_message(self, padded_message):
        # logging.info(f"{self.name}: Unpadding message")
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(padded_message) + unpadder.finalize()
        # logging.info(f"{self.name}: Message unpadded")
        return unpadded_data

    def create_mac(self, message, nonce):
        # logging.info(f"{self.name}: Creating MAC")
        key = self.mac_key  # Use stored MAC key
        mac = hmac.new(key, message + nonce, hashlib.sha256).digest()
        # logging.info(f"{self.name}: MAC created")
        return mac

    def verify_mac(self, message, nonce, received_mac):
        logging.info(f"{self.name}: Verifying MAC")
        key = self.mac_key  # Use stored MAC key
        expected_mac = hmac.new(key, message + nonce, hashlib.sha256).digest()
        if hmac.compare_digest(expected_mac, received_mac):
            logging.info(f"{self.name}: MAC verified")
            return True
        else:
            logging.warning(f"{self.name}: MAC verification failed")
            return False

    def aes_gcm_encrypt(self, plaintext, nonce):
        # logging.info(f"{self.name}: Encrypting message with AES-GCM")
        cipher = Cipher(
            algorithms.AES(self.shared_key), modes.GCM(nonce), backend=default_backend() # Use stored shared key
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        # logging.info(f"{self.name}: Message encrypted")
        return ciphertext, encryptor.tag

    def aes_gcm_decrypt(self, ciphertext, nonce, tag):
        logging.info(f"{self.name}: Decrypting message with AES-GCM")
        cipher = Cipher(
            algorithms.AES(self.shared_key), modes.GCM(nonce, tag), backend=default_backend() # Use stored shared key
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        logging.info(f"{self.name}: Message decrypted")
        return plaintext

    def seal_message(self, message, public_key):
        logging.info(f"{self.name}: Sealing message with Kyber")
        shared_key, ciphertext = Kyber1024.encaps(public_key)
        nonce = os.urandom(16)  # Generate nonce here
        encrypted_message = self.aes_gcm_encrypt(
            message.encode("utf-8"), nonce
        )  # Use AES-GCM for sealing
        sealed_message = (ciphertext, encrypted_message[0], encrypted_message[1], nonce) # Include nonce
        logging.info(f"{self.name}: Message sealed")
        return sealed_message

    def unseal_message(self, sealed_message):
        logging.info(f"{self.name}: Unsealing message with Kyber")
        ciphertext, encrypted_message, tag, nonce = sealed_message # Extract nonce
        shared_key = Kyber1024.decaps(self.current_kyber_sk, ciphertext)
        plaintext = self.aes_gcm_decrypt(encrypted_message, nonce, tag)
        logging.info(f"{self.name}: Message unsealed")
        return plaintext.decode("utf-8")

    def send_message(self, server, recipient, message):
        logging.info(f"{self.name}: Sending message to {recipient.name}")
        # 1. Pad message
        padded_message = self.pad_message(message.encode("utf-8"))

        # 2. Generate unique nonce
        nonce = os.urandom(16)

        # 3. Create unique ephemeral MAC
        mac = self.create_mac(padded_message, nonce)

        # 4. AES-GCM encrypt
        ciphertext, tag = self.aes_gcm_encrypt(padded_message, nonce)

        # 5. Add authentication data (MAC, nonce, tag)
        auth_data = (mac, nonce, tag)

        # 6. Add timestamp
        timestamp = str(int(time.time()))

        # Combine everything
        sealed_message = (ciphertext, auth_data, timestamp, padded_message) # Include padded_message

        logging.info(f"{self.name}: Message content: {Fore.LIGHTCYAN_EX}{message}") # Log message content
        logging.info(f"{self.name}: Padded message: {Fore.LIGHTCYAN_EX}{padded_message.hex()}") # Log padded message
        logging.info(f"{self.name}: Nonce: {Fore.LIGHTCYAN_EX}{nonce.hex()}") # Log nonce
        logging.info(f"{self.name}: MAC: {Fore.LIGHTCYAN_EX}{mac.hex()}") # Log MAC
        logging.info(f"{self.name}: Ciphertext: {Fore.LIGHTCYAN_EX}{ciphertext.hex()}") # Log Ciphertext

        # Simulate sending via TOR
        server.forward_message(self, recipient, sealed_message)
        logging.info(f"{self.name}: Message sent to {recipient.name}")

    def receive_message(self, server, sender, sealed_message):
        logging.info(f"{self.name}: Receiving message from {sender.name}")
        ciphertext, auth_data, timestamp, padded_message = sealed_message # Extract padded_message
        mac, nonce, tag = auth_data

        logging.info(f"{self.name}: Received ciphertext: {ciphertext.hex()}") # Log received ciphertext
        logging.info(f"{self.name}: Received nonce: {nonce.hex()}") # Log received nonce
        logging.info(f"{self.name}: Received MAC: {mac.hex()}") # Log received MAC

        # 1. Verify MAC
        if not self.verify_mac(padded_message, nonce, mac): # Correct: Using padded_message
            logging.error(f"{self.name}: MAC verification failed. Message rejected.")
            return None

        # 2. Verify timestamp
        current_time = int(time.time())
        message_time = int(timestamp)
        if abs(current_time - message_time) > 60:  # 60 seconds tolerance
            logging.warning(f"{self.name}: Timestamp invalid. Possible replay attack.")
            return None

        # 3. Decrypt message
        padded_message = self.aes_gcm_decrypt(ciphertext, nonce, tag)

        # 4. Remove padding
        unpadded_message = self.unpad_message(padded_message)

        # 5. Process Reply-To mailbox (Not implemented in this simplified version)

        logging.info(f"{self.name}: Message received and processed.")
        return unpadded_message.decode("utf-8")


class Server:
    def __init__(self):
        self.mailboxes = {}
        self.user_quotas = {}  # Simulate user quotas

    def open_mailbox(self, user, mailbox_id):
        # logging.info(f"Server: Opening mailbox {Fore.LIGHTCYAN_EX}{mailbox_id}{Fore.GREEN} for {Fore.LIGHTCYAN_EX}{user.name}")
        self.mailboxes[mailbox_id] = []
        user.mailbox = mailbox_id
        logging.info(f"Server: Mailbox {Fore.LIGHTCYAN_EX}{mailbox_id}{Fore.GREEN} opened for {Fore.LIGHTCYAN_EX}{user.name}")

    def forward_message(self, sender, recipient, sealed_message):
        logging.info(
            f"Server: Forwarding message from {sender.name} to {recipient.name}'s mailbox"
        )
        if recipient.mailbox not in self.mailboxes:
            logging.error(
                f"Server: Mailbox {recipient.mailbox} not found for {recipient.name}"
            )
            return
        self.mailboxes[recipient.mailbox].append((sender, sealed_message))
        logging.info(
            f"Server: Message forwarded to {recipient.name}'s mailbox {recipient.mailbox}"
        )

    def forward_notification(self, sender, recipient, sealed_notification):
        logging.info(
            f"Server: Forwarding notification from {sender.name} to {recipient.name}"
        )
        if recipient.mailbox not in self.mailboxes:
            logging.error(
                f"Server: Mailbox {recipient.mailbox} not found for {recipient.name}"
            )
            return
        self.mailboxes[recipient.mailbox].append((sender, sealed_notification))
        logging.info(
            f"Server: Notification forwarded to {recipient.name}'s mailbox {recipient.mailbox}"
        )

    def retrieve_messages(self, user):
        logging.info(f"Server: Retrieving messages for {user.name}")
        if user.mailbox not in self.mailboxes:
            logging.error(f"Server: Mailbox {user.mailbox} not found for {user.name}")
            return []
        messages = self.mailboxes[user.mailbox]
        self.mailboxes[user.mailbox] = []  # Empty the mailbox
        logging.info(f"Server: Messages retrieved for {user.name}")
        return messages

app = Flask(__name__)
CORS(app)

# Initialize users and server
alice = User("Alice")
bob = User("Bob")
server = Server()

# Initial Setup
server.open_mailbox(alice, alice.generate_mailbox_id())
server.open_mailbox(bob, bob.generate_mailbox_id())

# Quantum-Safe Key Setup
ciphertext_to_bob = alice.generate_shared_key(bob.current_kyber_pk)
bob.derive_shared_key(ciphertext_to_bob)

# Bob generates a shared key to Alice
ciphertext_to_alice = bob.generate_shared_key(alice.current_kyber_pk)
alice.derive_shared_key(ciphertext_to_alice)

messages = []

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    logging.info(f"Received data: {data}")  # Log the received data
    sender_name = data.get('sender')
    content = data.get('content')

    if not sender_name or not content:
        logging.error("Invalid data: 'sender' and 'content' are required.")
        return jsonify({'error': 'Invalid data'}), 400

    try:
        if sender_name == "Alice":
            sender = alice
            recipient = bob
        elif sender_name == "Bob":
            sender = bob
            recipient = alice
        else:
            logging.error(f"Invalid sender: {sender_name}")
            return jsonify({'error': 'Invalid sender'}), 400

        message_to_recipient = content
        sender.send_message(server, recipient, message_to_recipient)

        messages_for_recipient = server.retrieve_messages(recipient)
        if messages_for_recipient:
            message_sender, sealed_message = messages_for_recipient[0]
            received_message = recipient.receive_message(server, sender, sealed_message)
            if received_message:
                logging.info(Fore.CYAN + f"{recipient.name} received: {received_message}" + Style.RESET_ALL)
            else:
                logging.warning(f"Message reception failed for {recipient.name}")
        else:
            logging.info(f"No messages for {recipient.name}")

        return jsonify({'status': 'Message processed and exchanged'}), 200

    except Exception as e:
        logging.exception("An error occurred during message processing:")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=4566, ssl_context=("certs/certificate.crt", "certs/private.key"))
