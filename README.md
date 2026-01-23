# MockPacket
A Python-based network traffic generator designed for security researchers and digital forensics practitioners. This tool programmatically "forges" valid PCAP files by downloading real-world image data and encapsulating it into a TCP/IP stack.

MockPacket is essentially a "Network Simulator in a Box." Instead of having to open a browser and capture traffic with Wireshark manually, it "hand-crafts" the traffic from scratch.

## Run: 
```bash
sudo python generator.py 
[sudo] password for kali: 
Downloading images and building packets...
 [+] Added face.jpg (30215 bytes)
 [+] Added nature.jpg (13489 bytes)
 [+] Added car.jpg (14077 bytes)
 [+] Added dog.jpg (31048 bytes)
 [+] Added fruit.jpg (26855 bytes)

Success! Generated 'test_images.pcap' with 5 images.
```

Now you have 'test_images.pcap' file. 