"""Initialize librocket, once the required interfaces have been set.

"""
from libcpp cimport bool


cdef extern from "Rocket/Core.h" namespace "Rocket::Core":
    cdef bool Initialise()


def initialize():
    Initialise()
