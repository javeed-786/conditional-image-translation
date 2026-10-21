\# Conditional Image Translation Prototype



\## Project Overview

This project demonstrates a condition-based image translation prototype. It transforms an input image according to different conditions such as Day, Night, and Sunset.



\## Objectives

\- Apply different visual conditions to an input image.

\- Generate separate translated images for each condition.

\- Analyze how conditions affect image brightness and blue-channel intensity.

\- Compare the original image with the transformed outputs.



\## Technologies Used

\- Python

\- OpenCV

\- NumPy

\- Pandas

\- Matplotlib



\## Project Structure

\- `dataset/` – Input image and condition settings

\- `src/` – Python implementation

\- `outputs/` – Generated Day, Night, and Sunset images

\- `results/` – Analysis CSV and comparison chart

\- `screenshots/` – Project screenshots



\## How to Run

1\. Install Python.

2\. Install the required packages:



&#x20;  `py -m pip install -r requirements.txt`



3\. Run the program:



&#x20;  `py .\\src\\conditional\_translation.py`



\## Generated Outputs

\- `day\_output.png`

\- `night\_output.png`

\- `sunset\_output.png`

\- `condition\_analysis.csv`

\- `condition\_comparison.png`



\## Analysis

The prototype uses different brightness, contrast, and colour adjustments for each condition. The generated images and CSV measurements help demonstrate how changing the input condition influences the resulting image.



\## Conclusion

The project demonstrates a basic condition-based image translation workflow using Python and image-processing techniques. It generates multiple condition-specific outputs and compares their visual characteristics.



