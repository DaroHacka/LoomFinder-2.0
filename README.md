# LoomFinder 2.0

<!-- HTML to resize the image -->
<img src="https://github.com/DaroHacka/LoomFinder-2.0/blob/main/loomfinder.png" alt="LoomFinder Logo" width="350" align="right"/>


                                                                                                                                                                                                                             
The new and definitive version                                                                                                                                                                                           

LoomFinder is a tool created for retrieving random snippets from books hosted on the Internet Archive, offering 
users a chance to explore and discover new reads effortlessly.


Installation Instructions

To install LoomFinder 2.0, follow these steps:

1. Clone the Repository:
   from terminal
   
   git clone https://github.com/DaroHacka/LoomFinder-2.0.git
   
   cd LoomFinder-2.0

3. Create a New File in /usr/local/bin::
   
   sudo nano /usr/local/bin/loomfinder

4. Add the Shebang and paste the following Script:

   #!/bin/bash
   
   exec /home/user/.../loomfinder_section_code/main.py "$@"

   #add your own path to loomfinder folder

6. Make the Script executable:
   
   sudo chmod +x /usr/local/bin/loomfinder

7. Run loomfinder from terminal>
   
   loomfinder

-------------------

notes:

- If you need more time to evaluate whether you want to save the author because you need to read the extract first, you can modify the main.py. A single line comment # will guide you. By default, I set it to 10 seconds because the user might not want to press any key, and by the time they read the book title, the author, and the extract, the program would have terminated. For me personally 60 seconds is ideal.

- Mind that if you want to run loomfinder from anywhere in the terminal, you can. However, if you want to save the author from anywhere when asked by the program, you need to change the file=Authors_list.txt in the utilities.py file to your own path. Otherwise you need to be in the LoomFinder main folder.

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
  - https://archive.org/advancedsearch.php?q={query_string}&fl[]=identifier&fl[]=title&fl[]=creator&rows=1000&page=[1to10]&output=json
  - For minor genres and subjects, results are fetched on `page=1` minor genres usually don't get more than one or two pages of results,
    so limiting the search to page 1 is the best choice to avoid query failures. 
  - For super general categories like "history," "literature," "science," etc., that produce many results, the program fetches results
    from up to 10 different segments of the archive, significantly increasing the chances of successful results. This automated process
    is different from a user's experience on the web page, where all results are loaded on a single, continuous page, making it harder
    to explore deep into the data manually. By programmatically accessing multiple pages from 1 to 10, the code ensures a more
    comprehensive search and retrieves a broader range of relevant content. For the valid_subjects listed in queries.py, you’ll notice
    that the page number varies with each query because it’s randomized. Try loomfinder s:literature multiple times to see how page=n
    varies with each query randomly from 1 to 10.
    Additionally, the d:date flag changes behavior depending on whether the range is less than 4 years (e.g., d:1800-1804) or 5 years
    or more (e.g., d:1800-1805). In the first case, query results are fetched on page=1. In the latter case, results are fetched
    randomly from pages 1 to 10.
  - Weighing Literary Genres vs. Scientific and Cultural Subjects

    To ensure a proportional choice between literary genres and scientific/cultural subjects, we applied weighted random selection.
    This balances the literary genres against the more numerous scientific and cultural subjects, providing a fair representation
    of each category during queries.
  - Finally, with each query, LoomFinder will ask if you want to save the author to an auto-generated .txt file. If the query returns
    an unknown author, it won’t prompt you to save. There is a 10-second timer to respond with yes or no; if no response is given, the
    program will automatically terminate without saving. Additionally, all saved authors can be randomly included in a query by typing
    loomfinder prose. The prose flag simply selects a random author from the Authors_list.txt file and queries it on Internet Archive.
    This time it won't ask you to save since they are already on the list. The bigger the list, the more varied the query results.  

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
