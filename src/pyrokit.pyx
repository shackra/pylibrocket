"""Import this to bootstrap librocket so you can work with the rocket module directly.

"""

#cdef extern from "Rocket/Core.h" namespace "":
#    cdef cppclass Rectangle:
#        Rectangle(int, int, int, int)
#        int x0, y0, x1, y1
#        int getLength()
#        int getHeight()
#        int getArea()
#        void move(int, int)
#
#    cdef cppclass Foo:
#        Foo()
#
#cdef Rectangle *rec = new Rectangle(1, 2, 3, 4)
#cdef int recLength = rec.getLength()
#
#cdef Foo foo


cdef extern from "bootstrap.h":
	cdef void bootstrap()
