"""Initialize librocket, once the required interfaces have been set.

"""
cdef extern from "Rocket/Core.h" namespace "Rocket::Core":
    cdef bool Initialise()


def initialize():
    Initialise()
