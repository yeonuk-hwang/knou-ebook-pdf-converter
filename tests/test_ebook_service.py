# pyright: reportAny=false

"""
ebook service should be able to

- Take a screenshot of the current page
    - call the screenshot service method with correct arguments.
    - it should communicate with screenshot service


- Iterate through the following actions until the last page is reached
    - Take a screenshot of the current page
    - Navigate to the next page by clicking the 'Next' button
    - it should communicate with ebook_parser
"""
