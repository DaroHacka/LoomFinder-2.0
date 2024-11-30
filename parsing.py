def parse_parameters(params):
    title, genre, anything, author, subject, date = None, None, None, None, None, None
    
    for param in params:
        if param.startswith('t:'):
            title = param[2:]
        elif param.startswith('g:'):
            genre = param[2:]
        elif param.startswith('x:'):
            anything = param[2:]
        elif param.startswith('a:'):
            author = param[2:]
        elif param.startswith('s:'):
            subject = param[2:]
        elif param.startswith('d:'):
            date = param[2:]
    
    return title, genre, anything, author, subject, date
