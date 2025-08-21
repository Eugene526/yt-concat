# YT-Concat

This is a powerful command-line tool that automates the process of finding specific content within a YouTube channel. It works by searching through the captions of a channel's videos for a given keyword, extracting the relevant video segments, and merging them into a single, cohesive video.

Whether you're compiling highlights from a long lecture series, creating a supercut of a catchphrase, or just summarizing a channel's content, this tool helps you efficiently pinpoint and combine the moments that matter.

---

## 🛠 Key Features

- **Channel-Based Search:** Target a specific YouTube channel using its ID.
- **Caption-Driven:** The tool searches video captions for a specified keyword to find exact segments.
- **Automated Pipeline:** Handles the entire process, including getting video lists, downloading captions, searching, downloading video clips, and editing the final output.
- **Concise Output:** Extracts only the relevant segments, resulting in a single, focused video file.
- **Robust Logging:** All actions and potential errors are logged to a dedicated file and the console, making it easy to track progress and debug.
- **File Cleanup:** An optional flag allows you to automatically remove all downloaded video and caption files after the process is complete.

---

## 💻 How to Use

### 1. Prerequisites

Make sure you have **Python 3.x** installed. Then, install the required libraries by running:

```bash
pip install -r requirements.txt
```
## 2. Usage

This is a command-line tool. All interactions are done via your terminal. You must provide a channel ID and a search word.

Command Syntax:
```bash
python main.py -c <channel_id> -s <search_word> 
```
| Short Option | Long Option  | Description                                                             |
| ------------ | ------------ | ----------------------------------------------------------------------- |
| -c           | --channel    | (Required) The YouTube channel ID to process.                           |
| -s           | --searchword | (Required) Keyword to find matching segments in captions.               |
| -l           | --limit      | (Optional) Maximum number of fragments to extract based on the keyword. |
|              | --cleanup    | (Optional) Automatically remove all downloaded files after processing.  |

## Examples

**Basic Usage:**
Search the specified channel for all instances of "AI" and create a single video from the found clips.

Adding a Clip Limit and Cleanup:
Find up to 10 clips containing the word "Python" and delete all temporary files after the final video is created.
```bash
python main.py -c UCjD_v1n9V7k-jQ8m_p3h9Jg -s "Python" -l 10 --cleanup
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## 📫 Contact / Support

For questions, bug reports, or feature requests, please contact the developer at: eugenechan526@gmail.com
