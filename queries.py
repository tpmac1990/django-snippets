
############################################
# Some snippets to help with model queries
############################################


# store queries in a dictionary and use the lambda function to pass in the query set
def queries_in_dictionary(qs,name):
    # store the queries in a dictionary
    dic = {
        'ausstate': lambda qs: State.objects.filter(state_tenement__in=qs).values('pk','name').distinct().order_by('name'),
        'region': lambda qs: GovernmentRegion.objects.filter(govregion_tenement__in=qs).values('pk','name').distinct().order_by('name')
    }

    # lookup the dictionary by name and pass in the qs
    return dic[name](qs)

# This will find all the states in the Tenements dataset which is all the states and territories in Australia.
states_in_dataset = queries_in_dictionary(Tenement.objects.all(),"ausstate")



# model query with all elements passed in as strings
from django.apps import apps
def query_with_variables(ds_name,query_name):
    dic = {
        "ausstate": {
            "model": "State",
            "query": "state_tenement__in",
            "values": ["pk", "name"],
            "order_by": "name"
        },
        "region": {
            "model": "GovernmentRegion",
            "query": "govregion_tenement__in",
            "values": ["pk", "name"],
            "order_by": "name"
        }
    }

    # get the group by the passed in query name
    group = dic[query_name]

    # use 'apps.get_model("App_name", "Model_name")' to get the model from a string
    model = apps.get_model('map', group["model"])
    # The query, values & order_by are all extracted from the dictionary
    query = group["query"]
    values = tuple(group["values"]) # the list needs to be converted to a tuple so it can be unpacked
    order_by = group["order_by"]

    # To pass in the query as a string, use **{} for dictionary unpacking.
    # Unpack the 'values' tuple with *
    results = model.objects.filter(**{query: qs}).values(*values).distinct().order_by(order_by)

# pass in the name of the model and the query group to lookup from the dictionary
query_with_variables("Tenement","ausstate")