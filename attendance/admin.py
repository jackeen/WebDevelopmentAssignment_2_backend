from django.contrib import admin

from attendance.models import Student, Lecture, Semester, CollegeDay, Course, Class, Attendance

# Register your models here.
admin.site.register(Student)
admin.site.register(Lecture)
admin.site.register(Semester)
admin.site.register(CollegeDay)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Attendance)