from email._header_value_parser import Section

from rest_framework import viewsets

from attendance.models import Student, Course, Lecture, Class, CollegeDay, Semester
from attendance.serializers import StudentSerializer, CourseSerializer, LectureSerializer, SemesterSerializer, \
    CollegeDaySerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer


class CollegeDayViewSet(viewsets.ModelViewSet):
    queryset = CollegeDay.objects.all()
    serializer_class = CollegeDaySerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
