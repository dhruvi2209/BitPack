# BitPack: Huffman Coding Application
Developed by _Dhruvi Vaghela_.

## Overview

This project provides a Streamlit-based web application demonstrating Huffman Coding, a widely used compression algorithm. The app allows users to compress and decompress text, visualize the Huffman tree, and view detailed information about file sizes and character frequencies.

https://github.com/user-attachments/assets/5bef7e32-6166-444f-9295-c3cba70f4a5a

## Features

- **Text Compression**: Enter text up to 500 characters for compression.
- **Compression Information**: View original size, compressed size, and compression ratio.
- **Character Frequencies & Codes**: Display the frequency of each character and its corresponding Huffman code.
- **Huffman Tree Visualization**: Visualize the Huffman tree structure using Graphviz. (Left = 0, Right = 1)
- **File Download**: Download the compressed binary file.
- **Decompression**: Decompress the text and view the result.

## Technologies Used

- **Python**: Programming language used for the implementation.
- **Streamlit**: Framework for creating the web application.
- **Graphviz**: Used for visualizing the Huffman tree.
- **Pandas**: Used for displaying tabular data.



## Requirements

To run this application, you need to have the following Python packages installed:

- `streamlit`
- `heapq`
- `graphviz`
- `base64`
- `pandas`

You can install the required packages using pip:


1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dhruvi2209/BitPack.git
   
2. **Navigate to the Project Directory:**:
   ```bash
   cd BitPack

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt

## Running the App
To run the Streamlit app, use the following command:
  ```bash
  streamlit run main.py
```

## Usage
1. Enter up to 500 characters of text in the input field.
2. Click "Ctrl + Enter" to begin compression.
3. View the Huffman tree visualization and download the compressed file if needed.
4. Click the "Decompress" button to verify the decompressed text.
