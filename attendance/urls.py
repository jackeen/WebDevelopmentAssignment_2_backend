from rest_framework import routers

from attendance.viewsets import StudentViewSet, LectureViewSet, CourseViewSet, SemesterViewSet, ClassViewSet

router = routers.DefaultRouter()

router.register('students', StudentViewSet)
router.register('lectures', LectureViewSet)
router.register('courses', CourseViewSet)
router.register('semesters', SemesterViewSet)
router.register('classes', ClassViewSet)


urlpatterns = router.urls
