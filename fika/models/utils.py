

def find_all_db_objects(context):
    """ Return all objects stored in context.values(), and all subobjects.
        Great for reindexing the catalog or other database migrations.
    """
    result = set()
    result.add(context)
    for obj in context.values():
        result.update(find_all_db_objects(obj))
    return result
