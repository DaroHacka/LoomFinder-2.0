# LoomFinder-2.0
##########################
The new and definitive version 

LoomFinder is a tool created for retrieving random snippets from books hosted on the Internet Archive, offering 
users a chance to explore and discover new reads effortlessly.

## Installation Instructions

To install LoomFinder 2.0, follow these steps:

1. Clone the Repository:
   from terminal
   
   git clone https://github.com/DaroHacka/LoomFinder-2.0.git
   
   cd LoomFinder-2.0

3. Create a New File in /usr/local/bin::
   
   sudo nano /usr/local/bin/loomfinder

4. Add the Shebang and paste the following Script:

   #!/bin/bash
   
   exec /home/dan/myscripts/loomfinder_section_code/main.py "$@"

5. Make the Script executable:
   
   sudo chmod +x /usr/local/bin/loomfinder

6. Run loomfinder from terminal>
   
   loomfinder

-------------------
I decided to segment LoomFinder 2.0 into multiple files to better manage future implementations. This structure allows for:

- Easier Maintenance: Quick edits and updates to individual modules without affecting the entire program.
- Scalability: Adding new features becomes simpler and more organized.
- Tidiness: A clearer and more logical organization of code, making it more readable and maintainable.

## Major Changes in LoomFinder 2.0

Significant changes have been done to improve the success rate of retrieving random book fragments. The old query used a fixed 
page number, but in the new version, the query adapts based on the specificity of the genre and subject.

### Advanced Search Changes

- Previous Version:
  
  https://archive.org/advancedsearch.php?q={query_string}&fl[]=identifier&fl[]=title&fl[]=creator&rows=50&page=1&output=json
  

- New Version:
  - https://archive.org/advancedsearch.php?q={query_string}&fl[]=identifier&fl[]=title&fl[]=creator&rows=1000& [dynamic]page=[1to10]&output=json
  - For minor genres and subjects, results are fetched on `page=1`, avoiding unnecessary additional pages.
  - For super general categories like "history," "literature," "science," etc., that produce many results, the program fetches results
    from up to 10 different segments of the archive, significantly increasing the chances of successful results. This automated process
    is different from a user's experience on the web page, where all results are loaded on a single, continuous page, making it harder
    to explore deep into the data manually. By programmatically accessing multiple pages from 1 to 10, the code ensures a more
    comprehensive search and retrieves a broader range of relevant content.

## Positional Arguments

- **params**: Search parameters: `[t:title] [g:genre] [x:anything] [a:author] [s:subject] [d:date] [prose]`

## Options

- **-h, --help**: Show this help message and exit
- **--save**: Save the output to a file
- **--list-genres**: List available genres or subgenres of a specific genre
- **--list-subjects**: List available subjects or specific subfields

how to use it:

loomfinder a:"Emily Bronte"

loomfinder s:literature d:1800-1820

loomfinder g:poetry x:nature

It is possible to combine different flags

## Parameters

- **t:title**: The title of the book or text.
- **g:genre**: The genre of the book or text.
- **x:anything**: The general attribute of the book or text.
- **a:author**: The author of the book or text.
- **s:subject**: The subject of the book or text.
- **d:date**: The date or date range of the book or text.
- **prose**: loomfinder prose
  
  the prose flag randomly selects an author from the saved Authors_list.txt generated by LoomFinder. 
  When running without the prose parameter, LoomFinder will prompt the user to save the 
  resulting author from their query. If the user ignores the prompt, the program will 
  terminate after ten seconds. If the user decides to save the author, it will be added 
  to a generated text file, which can be accessed with the prose flag. 
  Thus, having more authors is advantageous.
  

If you need some inspiration for your queries just type the following command for a comprehensive list

loomfinder --list-genres

loomfinder --list-subjects
