from ariadne import QueryType, load_schema_from_path, make_executable_schema

# Load schema type definitions from graphql schema
type_defs = load_schema_from_path("schema.graphql")

query = QueryType()

@query.field("hello")
def resolve_hello(*_):
    return "Hello world!"

schema = make_executable_schema(type_defs, query)