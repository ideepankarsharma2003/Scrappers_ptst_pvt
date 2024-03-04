# Pinterest Automation Script

This Python script automates the process of searching for images on Pinterest, extracting relevant data, generating alternative text for the images using an AI model, and displaying the results using Streamlit.

## How to Use

1. Make sure you have the necessary dependencies installed. You can install them using `pip`:

```bash
pip install streamlit playwright requests pillow beautifulsoup4
```

2. Run the streamlit app:
```bash
streamlit run pinterest_app.py
```

3. Enter the query and the number of images to consider in the Streamlit interface.
4. Click the "Generate" button to initiate the process.
5. The script will automatically search for images on Pinterest, extract relevant data, generate alternative text using an AI model, and display the results using Streamlit.

## Dependencies

- `streamlit`: For creating interactive web applications.
- `playwright`: For automating browser interactions.
- `requests`: For making HTTP requests.
- `pillow`: For working with images.
- `beautifulsoup4`: For parsing HTML content.

## Note

Make sure to replace the placeholder API keys and URLs with your actual keys and URLs. Additionally, ensure that you have the necessary permissions to access the Pinterest and AI model APIs.


## Demo 