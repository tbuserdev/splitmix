### **Prerequisites**

1. **Python:** You need Python installed on your system.

2. **FFmpeg:** This is a crucial dependency for `pydub` to work correctly. You must install it and ensure it's accessible from your system's command line (i.e., it's in your PATH).

   * **Windows:** Download from the [official FFmpeg website](https://ffmpeg.org/download.html) and add the `bin` folder to your system's PATH.

   * **macOS (using Homebrew):** `brew install ffmpeg`

   * **Linux (using apt):** `sudo apt update && sudo apt install ffmpeg`

3. **Python Libraries:** You need to install `pydub` and `mutagen`.

### **Setup Instructions**

1. **Save the Files:** Save the three files I generated (`wav_splitter.py`, `requirements.txt`, and `timestamps.txt`) into the same folder on your computer.

2. **Install Libraries:** Open your terminal or command prompt, navigate to that folder, and run this command:

```bash
pip install -r requirements.txt
```

3. **Prepare Your Files:**

* Place the large `.wav` file you want to split into the same folder.

* (Optional) Place a cover image (e.g., `cover.jpg`) in the folder if you want to add album art.

* Verify the `timestamps.txt` file contains the correct tracklist.


### **How to Run the Script**

You will run the script from your terminal or command prompt.

1. Navigate to the directory where you saved the files.

2. Activate your Python environment: 
   * On Windows: `venv\Scripts\activate`
   * On macOS/Linux: `source .venv/bin/activate`

3. Use the following command structure:

```bash
python wav_splitter.py "input.flac" --artist "Artist Name" --album "Album Name" --tracklist "timestamps.txt"
```

#### **Example Command:**

Let's say your audio file is named `live_set.wav`, the artist is `Fred again..`, and the album is `Boiler Room`. You would run:

```bash
python main.py "input.wav" --artist "Kaytranada" --album "Elevator Music" --tracklist "timestamps.txt" --cover "cover.jpg"
```


#### **To Add Album Art:**

If you have a `cover.jpg` file you want to use, add the `--cover` flag:

```bash
python3 main.py "input.wav" --artist "Sam Gellaitry" --album "Elevator Music" --tracklist "timestamps.txt" --cover "cover.jpg"
```

After running, the script will create a new folder named `output_tracks` (or a custom name if you specify one) containing all the split `.mp3` files, correctly named and tagged.
