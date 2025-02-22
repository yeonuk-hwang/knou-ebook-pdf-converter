# Specification

## Flow

1. Open the headed browser
2. Ask user to open the ebook viewer in pdf viewer
3. Take screenshots of the ebook
4. OCR every images
5. Create a pdf and add text layer to make it searchable

## Details

### 1. Open the headed browser

Opening the ebook in headless mode on behalf of the user would be challenging, as I do not have the user's credentials and cannot specify which ebook should be converted. Therefore, it would be better to open the browser in headed mode and ask the user to open the ebook themselves.

There is a drawback to using a headed browser, as the user cannot do anything else while the browser is in operation. The browser must remain focused, as the program continually clicks the next button and takes a screenshot. However, I believe the necessity of using headed mode outweighs this drawback; therefore, I have decided to proceed with headed mode.

I prefer using Playwright over Puppeteeer because the locators, such as `getByRole` and `getByText` are easier to work with than traditional CSS selectors used in Puppeteer. Additionally, using Playwright's inspector makes it easier to specify the selectors for the desired elements.

### 2. Ask user to open the ebook viewer in pdf viewer

Open the browser in headed mode in Step 1, then ask the user to open the eBook page in the PDF viewer.

The new eBook viewer opens the book in two-page mode, but it would be better to take a screenshot of each page, therefore, using the PDF viewer would be ideal.

I intend to use it personally; thus, there are not many requirements to validate that the user opens the correct viewer, However, it would be beneficial to add validation feature later

### 3. Take screenshots of the ebook

- Calculate the total number of pages.
- Iterate through the following actions until the last page is reached:

  - Take a screenshot of the current page.
  - Navigate to the next page by clikcing the 'Next' button.

  - Optional: Showing progress bar would be helpful.

### 4. OCR every images

I chose PaddleOCR because there are several OCR models available, such as EasyOCR and Tesseract. I have tried Tesseract before, but I was not satisfied with the result.

I selected PaddleOCR based on several blog posts that compare PaddleOCR and EasyOCR. I do not have time for an in-depth comparison; therefore, I decided to use PaddleOCR without further scrutiny.

For this reason, I have chosen to use PaddleOCR for now. However, I should consider the potential for switching OCR models in the future while writing code. Therefore, I should not rely directly on the PaddleOCR API and should add an abstraction layer on top of that.

Additionally, it is worth leveraging LLMs to refine the result of the OCR. This is not a mandatory feature, so I can add it later.

### 5. Create a pdf and add text layer to make it searchable

In Step 4, PaddleOCR returns output as a list. Each item in the list contains a `bounding box`, `text`, and `recognition confidence`.

I need to figure out how to create a pdf from multiple images, and add text layers to the pdf to make it searchable.

## Miscellaneous

### Motivation for the Project

1. Automation of repetitive tasks: Previously, I used Keyboard Maestro to semi-automatically capture screenshots, and tools like PDF Expert for OCR and to convert images to PDF. However, these tasks were cumbersome, and PDF Expert offers the features I need for a fee, so I decided to write a program to solve this issue.

2. Practicing Python: I have been developing with TypeScript, but recently I noticed that Python is widely used in AI including LLMs, Machine Learning. Personally, I believe that Python's versatility and well-structured ecosystem are worth learning, so I'm attempting to create a package in Python.
