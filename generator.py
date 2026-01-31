import requests
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
    packets = []
    src_ip = "192.168.1.10"
    dst_ip = "10.0.0.5"
    
    print("Downloading images and building packets...")
    
    for i, (filename, url) in enumerate(image_urls.items()):
        try:
            # Download image data
            img_data = requests.get(url).content
            
            # Construct a fake HTTP Response header
            http_header = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: image/jpeg\r\n"
                f"Content-Length: {len(img_data)}\r\n"
                f"Connection: close\r\n\r\n"
            ).encode()
            
            payload = http_header + img_data
            
            # Wrap in Ethernet/IP/TCP layers.
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
    print("\nSuccess! Generated 'test_images.pcap' with 5 images.")

if __name__ == "__main__":
    create_pcap()

