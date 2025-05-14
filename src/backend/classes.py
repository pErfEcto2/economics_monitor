from graphene import ObjectType, Float, String

class EconomicIndicator(ObjectType):
    timestamp = String()
    value = Float()
    units = String()

