def clean_nonserializable_attributes(dictionary):
    # normalize the name for 'id'
    if '_id' in dictionary:
        dictionary['id'] = str(dictionary.pop('_id'))
