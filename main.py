import streamlit as st
import heapq
import graphviz
import base64
import pandas as pd

class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.root = None

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if other is None:
                return False
            if not isinstance(other, HuffmanCoding.HeapNode):
                return False
            return self.freq == other.freq

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)  

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1  
            merged.right = node2 

            heapq.heappush(self.heap, merged)

        self.root = heapq.heappop(self.heap)  

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        self.make_codes_helper(self.root, "")

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text, extra_padding

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            st.error("Encoded text not padded properly")
            return None

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text


def main():
    st.set_page_config(page_title="Bit Pack", page_icon=":page_facing_up:", layout="centered", initial_sidebar_state="auto", menu_items=None)

    st.title("Bit Pack: Huffman Coding")

    
    user_text = st.text_area("Enter text to compress (up to 500 characters):", max_chars=500)

    if user_text:
        
        huffman = HuffmanCoding()
        frequency = huffman.make_frequency_dict(user_text)
        huffman.make_heap(frequency)
        huffman.merge_nodes()
        huffman.make_codes()

        
        original_size = len(user_text.encode('utf-8')) * 8  # in bits

        
        encoded_text = huffman.get_encoded_text(user_text)
        padded_encoded_text, extra_padding = huffman.pad_encoded_text(encoded_text)

      
        compressed_size = len(padded_encoded_text)

        
        compression_ratio = original_size / compressed_size if compressed_size != 0 else 0

        
        size_data = {
            "Original Size (bits)": [original_size],
            "Compressed Size (bits)": [compressed_size],
            "Compression Ratio": [f"{compression_ratio:.2f}"],
        }
        size_df = pd.DataFrame(size_data)

       
        st.subheader("File Size Information")
        st.table(size_df)

       
        char_freq = []
        for char, freq in frequency.items():
            char_freq.append([char, freq, huffman.codes[char]])

        char_freq_df = pd.DataFrame(char_freq, columns=["Character", "Frequency", "Huffman Code"])

        st.subheader("Character Frequencies and Huffman Codes")
        st.table(char_freq_df)

        
        st.subheader("Encoded Text")
        encoded_text_formatted = format_encoded_text(encoded_text)
        st.markdown(f"``{encoded_text_formatted}``")

        
        st.subheader("Huffman Tree Visualization")
        huffman_tree = visualize_huffman_tree(huffman)
        st.graphviz_chart(huffman_tree)

       
        compressed_data = huffman.get_byte_array(padded_encoded_text)
        if compressed_data:
            compressed_file = base64.b64encode(bytes(compressed_data)).decode()
            st.download_button(label="Download Compressed File",
                               data=compressed_file,
                               file_name="compressed.bin")

       
        if st.button("Decompress"):
            decompressed_text = huffman.decode_text(encoded_text)
            st.subheader("Decompressed Text")
            st.write(decompressed_text)


def format_encoded_text(encoded_text, chunk_size=8):
    
    return ' '.join(encoded_text[i:i+chunk_size] for i in range(0, len(encoded_text), chunk_size))


def visualize_huffman_tree(huffman):
    
    dot = graphviz.Digraph()
    build_graph(dot, huffman.root, "") 
    return dot

def build_graph(dot, node, code):
    
    if node is None:
        return
    if node.char is not None:
        dot.node(code, label=f"'{node.char}'\n{node.freq}")
    else:
        dot.node(code, label=f"{node.freq}")

    if node.left:
        dot.edge(code, code + "0")
        build_graph(dot, node.left, code + "0")
    if node.right:
        dot.edge(code, code + "1")
        build_graph(dot, node.right, code + "1")


if __name__ == "__main__":
    main()
