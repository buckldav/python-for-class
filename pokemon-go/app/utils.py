def list_to_string(my_list):
    """
    Input: ['thing1', 'thing2']
    Output: 'Thing1, Thing2'
    """
    output = ""
    for item in my_list:
        output += str(item).title() + ", "
    return output[:-2]

def list_to_string_sql(my_list):
    """
    Like the list_to_string function above
    For use when inserting values in a SQL command
    """
    output = ""
    for item in my_list:
        if type(item) is str:
            item = f"'{item}'"
        output += str(item) + ", "
    return output[:-2]