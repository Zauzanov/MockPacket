import requests                                                                                                     # Allows to call requests to fetsh URLs.
from scapy.all import Ether, IP, TCP, Raw, wrpcap

# URLs for test images:
image_urls = {
    "face.jpg": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80",
    "nature.jpg": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=300&q=80",
    "car.jpg": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=300&q=80",
    "dog.jpg": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=300&q=80",
    "fruit.jpg": "https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&w=300&q=80"
}

def create_pcap():
    packets = []                                                                                                    # An empty list for Scapy packet objects.
    src_ip = "192.168.1.10"                                                                                         # I am simulating traffic.
    dst_ip = "10.0.0.5"                                                                                             # Private addresses; They are not publicly routable from the global internet.
    
    print("Downloading images and building packets...")
    
    for i, (filename, url) in enumerate(image_urls.items()):                                                        # Loops over the dict entries.
        # Preventing one failed download from killing the script
        try:
            # Download image data
            img_data = requests.get(url).content                                                                    # Raw response bodt as bytes for images. 
            
            # Construct a fake HTTP Response header
            http_header = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: image/jpeg\r\n"
                f"Content-Length: {len(img_data)}\r\n"                                                              # Length in bytes of the body. 
                f"Connection: close\r\n\r\n"                                                                        # The end of headers. 
            ).encode()                                                                                              # Converts the header string into bytes.
            
            # Contatenates header and body into one payload
            payload = http_header + img_data 
            

            # Build a fake packet, wrapping in Ethernet/IP/TCP layers.
            # Each image gets a unique port to simulate different requests:
            pkt = (Ether() / 
                   IP(src=src_ip, dst=dst_ip) / 
                   TCP(sport=443, dport=5000 + i, flags="PA") / 
                   Raw(load=payload))
            
            packets.append(pkt)
            print(f" [+] Added {filename} ({len(img_data)} bytes)")
            
        except Exception as e:
            print(f" [!] Error with {filename}: {e}")

    # Write all packets to a .pcap file
    wrpcap("test_images.pcap", packets)
    print(f"\nSuccess! Generated 'test_images.pcap' {len(packets)} images.")

if __name__ == "__main__":
    create_pcap()

