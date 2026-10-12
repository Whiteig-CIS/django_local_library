from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.models import StudyRoom, StudyRoomBooking


User = get_user_model()


class StudyRoomViewTest(TestCase):
    def setUp(self):
        self.room = StudyRoom.objects.create(
            name='Quiet Room A',
            location='West Wing 201',
            seats=6,
            capacity=6,
            availability='a',
        )
        self.staff_user = User.objects.create_user(
            username='staff', password='test-password', is_staff=True,
        )
        self.patron = User.objects.create_user(
            username='patron', password='test-password',
        )

    def test_room_list_is_public(self):
        response = self.client.get(reverse('study-rooms'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/studyroom_list.html')
        self.assertContains(response, 'Quiet Room A')
        self.assertContains(response, 'Available')

    def test_staff_can_update_room_availability(self):
        self.client.login(username='staff', password='test-password')
        response = self.client.post(
            reverse('study-room-update', args=[self.room.pk]),
            {
                'name': self.room.name,
                'location': self.room.location,
                'seats': self.room.seats,
                'capacity': self.room.capacity,
                'availability': 'm',
                'description': '',
                'equipment': '',
                'has_windows': 'on',
            },
        )

        self.assertRedirects(response, self.room.get_absolute_url())
        self.room.refresh_from_db()
        self.assertEqual(self.room.availability, 'm')

    def test_non_staff_cannot_manage_or_reserve_room(self):
        self.client.login(username='patron', password='test-password')

        self.assertEqual(
            self.client.get(reverse('study-room-update', args=[self.room.pk])).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(reverse('study-room-booking-create', args=[self.room.pk])).status_code,
            403,
        )

    def test_staff_reservation_marks_room_reserved(self):
        self.client.login(username='staff', password='test-password')
        start_time = timezone.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=2)

        response = self.client.post(
            reverse('study-room-booking-create', args=[self.room.pk]),
            {
                'start_time': start_time.strftime('%Y-%m-%dT%H:%M'),
                'end_time': end_time.strftime('%Y-%m-%dT%H:%M'),
                'status': 'b',
                'notes': 'Exam preparation',
            },
        )

        self.assertRedirects(response, self.room.get_absolute_url())
        self.assertEqual(StudyRoomBooking.objects.count(), 1)
        self.room.refresh_from_db()
        self.assertEqual(self.room.availability, 'r')
