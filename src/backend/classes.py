from graphene import ObjectType, Int, String

class BrentCrudeOil(ObjectType):
    timestamp = String()
    value = Int()
    units = String()

