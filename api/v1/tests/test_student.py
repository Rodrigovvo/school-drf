from unittest import result
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from api.v1.serializers.students import StudentSerializer
from apps.students.models import Student

client = Client()
factory = APIRequestFactory()


class StudentTest(APITestCase):

    def setUp(self):
        """
        Disclaimer: The Doc numbers were generated at https://www.4devs.com.br/gerador_de_cnpj
        """
        self.heitor = Student.objects.create(
            nickname="Heitor01",
            address= "Rua das flores, 150, Troia",
            age= "15",
            doc= "458.444.810-89",
            email= "student@email.com",
            first_name= "Heitor",
            last_name= "de Tróia",
            course= "Biologia"
        )
        self.paris = Student.objects.create(
            nickname="Paris",
            address= "Rua das flores, 150, Troia",
            age= "13",
            doc= "45459078067",
            email= "paris@email.com",
            first_name= "Páris",
            last_name= "de Tróia",
            course= "Matemática"
        )
        self.valid = {
            "nickname":"Aquiles",
            "address": "Rua do Pomo de Ouro, 10, Atenas",
            "age": "16",
            "doc": "80690875010",
            "email": "heitor@email.com",
            "first_name": "Heitor",
            "last_name": "da Grécia",
            "course": "Ed. Física"
        }

    def test_create_student(self):
        response = self.client.post('/api/v1/students/', self.valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_student(self):
        response = client.get(f'/api/v1/students/{self.heitor.pk}/')
        heitor = Student.objects.get(pk=self.heitor.pk)
        serializer = StudentSerializer(heitor)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_with_patch(self):
        response = self.client.patch(
            f'/api/v1/students/{self.heitor.pk}/', 
            {'address' : 'Rua do Pomo de Ouro, 10, Atenas'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.heitor.address, 'Rua do Pomo de Ouro, 10, Atenas')        

    def test_update_student_with_put(self):
        student = Student.objects.get(pk=self.heitor.pk)
        student.address = 'Rua do Pomo de Ouro, 10, Atenas'
        serializer = StudentSerializer(student)
        response = self.client.put(f'/api/v1/students/{student.pk}/', serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(student.address, 'Rua das flores, 150, Troia')
        self.assertEqual(student.address, 'Rua do Pomo de Ouro, 10, Atenas')

    def test_soft_delete_student(self):
        student = Student.objects.get(pk=self.heitor.pk)
        
        response = self.client.delete(f'/api/v1/students/{student.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        student = Student.objects.get(pk=self.heitor.pk)
        self.assertEqual(student.is_active, False)

    def test_search_student_by_first_name(self):
        response = self.client.get(
            f'/api/v1/students/search/?name=Hei'
        )
        students = Student.objects.filter(
            first_name__icontains='Hei'
        ).order_by('-modified_at')

        serializer = StudentSerializer(students, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_search_student_by_last_name(self):
        response = self.client.get(
            f'/api/v1/students/search/?name=Tróia'
        )
        students = Student.objects.filter(
            last_name__icontains='Tróia'
        ).order_by('-modified_at')

        serializer = StudentSerializer(students, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_student_by_enrollment_number(self):
        response = self.client.get(
            f'/api/v1/students/search/?enrollment=1'
        )
        students = Student.objects.filter(
            enrollment_number=1
        ).order_by('-modified_at')

        serializer = StudentSerializer(students, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_student_by_course(self):
        response = self.client.get(
            f'/api/v1/students/search/?course=bio'
        )
        students = Student.objects.filter(
            course__icontains='bio'
        ).order_by('-modified_at')

        serializer = StudentSerializer(students, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)