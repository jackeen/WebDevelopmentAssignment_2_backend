from datetime import timedelta

from django.contrib.auth.models import User, Group
from rest_framework import serializers, status
from rest_framework.response import Response

from attendance.models import Student, GROUP_STUDENT, Lecture, GROUP_LECTURE, Course, Class, Semester, CollegeDay


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data, password):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


def add_user_for_staff(validated_data, group_name):
    user_data = validated_data.pop('user')
    password = validated_data['date_of_birth'].strftime('%Y%m%d')
    user = UserSerializer().create(validated_data=user_data, password=password)
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    return user


def update_for_staff(instance, validated_data):
    user_data = validated_data.pop('user', {})
    user = instance.user
    UserSerializer().update(user, validated_data=user_data)
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'student_id', 'date_of_birth', 'user']

    def create(self, validated_data):
        user = add_user_for_staff(validated_data, GROUP_STUDENT)
        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        update_for_staff(instance, validated_data)
        return instance

    def destroy(self, request, *args, **kwargs):
        student = self.get_object()
        student.delete()
        return student


class LectureSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Lecture
        fields = ['id', 'staff_id', 'date_of_birth', 'user']

    def create(self, validated_data):
        user = add_user_for_staff(validated_data, GROUP_LECTURE)
        lecture = Lecture.objects.create(user=user, **validated_data)
        return lecture

    def update(self, instance, validated_data):
        update_for_staff(instance, validated_data)
        return instance

    def destroy(self, request, *args, **kwargs):
        lecture = self.get_object()
        lecture.delete()
        return lecture


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name']


def generate_college_days(semester_instance):
    date_list = []
    current_date = semester_instance.start_date
    while current_date <= semester_instance.end_date:
        date_list.append(current_date)
        collegeDay, _ = CollegeDay.objects.get_or_create(
            semester=semester_instance,
            date=current_date,
        )
        collegeDay.save()
        current_date += timedelta(days=1)


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'year', 'semester', 'start_date', 'end_date']

    def create(self, validated_data):
        semester = Semester.objects.create(**validated_data)
        generate_college_days(semester)
        return semester

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        generate_college_days(instance)
        instance.save()
        return instance

    def destroy(self, request, *args, **kwargs):
        semester = self.get_object()
        semester.delete()
        return semester


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'number', 'semester', 'course', 'lecture', 'students']