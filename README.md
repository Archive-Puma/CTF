# 📝 CTF Cheatsheet

## 📚 Table of content

- [🔐 Crypto](##-🔐-Crypto)
    - [Ping Pong](###-Ping-Pong)
    - [XOR (1-byte)](###-XOR-(1-byte))

## 🔐 Crypto

### Ping Pong

The message is encoded in binary using the words `PING` and `PONG`.

Example:

```sh
PONG PING PONG PONG PONG PONG PING PING PONG PING PONG PING PONG PING PONG PONG PONG PING PONG PONG PONG PING PING PONG PONG PING PING PING PING PONG PING PING PONG PING PING PONG PONG PING PING PONG PONG PING PING PONG PING PING PONG PONG PONG PING PING PONG PONG PONG PONG PING PONG PING PING PONG PONG PING PING PING PONG PING PING PING PING PING PONG PING
```

Solution:

```sh
cat flag.txt | tr '[:lower:]' '[:upper:]' | tr -cd 'IO' | tr 'IO' '10' | perl -lpe '$_=pack"B*",$_'
```

### XOR (1-byte)

Since it is a simple `XOR` operation of only one-byte length, a brute force attack is possible, because there are only 256 possible keys.

Example:

```sh
b7a0b28f9298959389
```

Solution:

```sh
KNOWN = "CTF"
CHALLENGE = ""

guesses = [(k, ''.join([chr(c^k) for c in bytes.fromhex(CHALLENGE)])) for k in range(256)]
for (k,m) in filter(lambda x: KNOWN in x[1], guesses): print(f'{chr(45) * 10}\nKey: {hex(k)}\nMessage: {m}')
```