def menu(title, items):
    itemsString = map(lambda i: '--' + i, items)
    
    return title + '\n' + '\n'.join(itemsString)
