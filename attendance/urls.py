from rest_framework import routers

from attendance.viewsets import StudentViewSet, LectureViewSet, CourseViewSet, SemesterViewSet, ClassViewSet, \
    AttendanceViewSet, CollegeDayViewSet

router = routers.DefaultRouter()

router.register('students', StudentViewSet)
router.register('lectures', LectureViewSet)
router.register('courses', CourseViewSet)
router.register('semesters', SemesterViewSet)
router.register('classes', ClassViewSet)
router.register('attendances', AttendanceViewSet)
router.register('college_days', CollegeDayViewSet)


urlpatterns = router.urls
