def peewee_get_kwargs(model_class, **kwargs):
    expression = None

    fields = model_class._meta.fields

    filter_fields = set(kwargs.keys())
    model_fields = set(fields)

    if not filter_fields.issubset(model_fields):
        raise Exception("Extra fields provided " + str(filter_fields - model_fields))

    for field in filter_fields.intersection(model_fields):
        expression = (fields[field] == kwargs[field])

    return model_class.select().where(expression)