from django.contrib.auth.models import User
from rest_framework import viewsets

from attendance import permissions
from attendance.models import Student, Course, Lecture, Class, CollegeDay, Semester, GROUP_LECTURE, GROUP_STUDENT, \
    Attendance
from attendance.serializers import StudentSerializer, CourseSerializer, LectureSerializer, SemesterSerializer, \
    ClassSerializer, AttendanceSerializer, CollegeDaySerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAdmin]


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAdmin]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdmin]


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAdmin]


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthorized]

    # filter data for different roles
    def get_queryset(self):
        user: User = self.request.user
        if user.is_superuser:
            return Class.objects.all()
        if user.groups.filter(name=GROUP_LECTURE).exists():
            return Class.objects.filter(lecture__user=user)
        if user.groups.filter(name=GROUP_STUDENT).exists():
            student = Student.objects.get(user=user)
            return Class.objects.filter(students=student)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsLectureWriteOnly]

    # for different roles' requirements
    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.query_params.get('class_id')
        lecture_id = self.request.query_params.get('lecture_id')
        if class_id is not None:
            queryset = queryset.filter(class_ref__id=class_id)
        if lecture_id is not None:
            queryset = queryset.filter(lecture__id=lecture_id)
        return queryset


class CollegeDayViewSet(viewsets.ModelViewSet):
    queryset = CollegeDay.objects.all()
    serializer_class = CollegeDaySerializer
    permission_classes = [permissions.IsUserReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        semester_id = self.request.query_params.get('semester_id')
        if semester_id is not None:
            queryset = queryset.filter(semester__id=semester_id)
        return queryset