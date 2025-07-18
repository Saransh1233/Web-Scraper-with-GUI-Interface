# 🕸️ Web Scraper GUI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A Python-based desktop GUI application to scrape and display content from web pages including text, URLs, images, meta tags, and more. This tool offers image previews, document saving, and a graphical display of scraping time complexity.

---

## 🧰 Features

- ✅ **Extract Web Content**
  - Full page **text**
  - Page **URL**
  - Webpage **title**
  - **Meta tags**
  - All **URLs** and **images**

- 🖼️ **Progressive Image Display**
  - Fetches and shows images one-by-one using multithreading

- 💾 **Save to File**
  - Saves text and metadata to `.docx`
  - Saves all images into a `.pdf`

- 📊 **Graphical Time Complexity**
  - View the scraping execution time for each feature in a matplotlib bar graph

- 🧪 **User-Friendly Interface**
  - Easy-to-navigate buttons and clear outputs
  - Tkinter-based UI with text area, image preview, and graphs

---

## 🎥 Demo

![Demo GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmI4MzU0YmNlNzMzOGM2MTQwYzMyY2IxMDE1MzI4N2E0YzFkNjEyMiZjdD1n/KeoVSRj0Xz3fVaXU5Y/giphy.gif)

---

## 📦 Requirements

Install the required Python packages using pip:

```bash
pip install requests beautifulsoup4 pillow python-docx reportlab matplotlib
