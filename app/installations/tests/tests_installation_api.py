from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status as HTTPstatus


from core.models import Installation, Status

import datetime

from installations.serializers import (
    InstallationSerializer,
    InstallationDetailSerializer,
)

INSTALLATION_URL = reverse("installations:installation-list")


def detail_url(installation_id):
    """Return installation detail URL"""
    return reverse("installations:installation-detail", args=[installation_id])


def sample_status(user, status=Status.STATUS_CHOICES[0][0]):
    """Create and return a sample status"""
    return Status.objects.create(user=user, status=status)


def sample_installation(user, **params):
    """Create and return a sample installation"""
    defaults = {
        "customer_name": "Phillip Moss",
        "address": "17 Petunia Street",
        "appointment_date": datetime.date(2022, 10, 22),
    }
    defaults.update(params)

    return Installation.objects.create(user=user, **defaults)


class PublicInstallationApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(INSTALLATION_URL)

        self.assertEqual(res.status_code, HTTPstatus.HTTP_401_UNAUTHORIZED)


class PrivateInstallationApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "ryan@vumatel.co.za", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_installations(self):
        """Test retrieving a list of installations"""
        sample_installation(user=self.user)
        sample_installation(user=self.user)

        res = self.client.get(INSTALLATION_URL)

        installations = Installation.objects.all().order_by("-id")
        serializer = InstallationSerializer(installations, many=True)
        self.assertEqual(res.status_code, HTTPstatus.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_installation_limited_to_user(self):
        """Test retrieving installations for user"""
        user2 = get_user_model().objects.create_user(
            "ryantest@vumatel.co.za", "password123"
        )
        sample_installation(user=user2)
        sample_installation(user=self.user)

        res = self.client.get(INSTALLATION_URL)

        installations = Installation.objects.filter(user=self.user)
        # List installation api returns list
        serializer = InstallationSerializer(installations, many=True)

        self.assertEqual(res.status_code, HTTPstatus.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_installation_detail(self):
        """Test viewing an installation detail"""
        installation = sample_installation(user=self.user)

        url = detail_url(installation.id)
        res = self.client.get(url)

        serializer = InstallationDetailSerializer(installation)
        self.assertEqual(res.data, serializer.data)

    def test_create_installation(self):
        """Test creating installation"""
        status1 = sample_status(user=self.user)
        status2 = sample_status(user=self.user, status=Status.STATUS_CHOICES[1][0])
        payload = {
            "customer_name": "Phillip Moss",
            "address": "17 Petunia Street",
            "appointment_date": datetime.date(2022, 10, 22),
            "status": [status1.id, status2.id],
        }
        res = self.client.post(INSTALLATION_URL, payload)

        self.assertEqual(res.status_code, HTTPstatus.HTTP_201_CREATED)
        installation = Installation.objects.get(id=res.data["id"])
        statuses = installation.status.all()
        self.assertEqual(statuses.count(), 2)
        self.assertIn(status1, statuses)
        self.assertIn(status2, statuses)

        # for key in payload.keys():
        #     # review
        #     self.assertEqual(payload[key], getattr(installation, key))

    def test_partial_update_installation(self):
        """Test updating an install with patch"""
        installation = sample_installation(user=self.user)
        new_status = sample_status(self.user, status=Status.STATUS_CHOICES[1][0])

        payload = {"customer_name": "Fred Flintstone", "status": [new_status.id]}
        url = detail_url(installation.id)
        self.client.patch(url, payload)

        installation.refresh_from_db()
        self.assertEqual(installation.customer_name, payload["customer_name"])
        status = installation.status.all()
        self.assertEqual(len(status), 1)
        self.assertIn(new_status, status)

    def test_full_update_installation(self):
        """Test updating an installation with a put"""
        installation = sample_installation(user=self.user)
        payload = {
            "customer_name": "Fred Flintstone",
            "appointment_date": datetime.date(2022, 4, 3),
            "address": "2 Longdon Avenue",
            "status": Status.STATUS_CHOICES[2][0],
        }
        url = detail_url(installation.id)
        self.client.patch(url, payload)

        installation.refresh_from_db()
        self.assertEqual(installation.customer_name, payload["customer_name"])
        self.assertEqual(installation.appointment_date, payload["appointment_date"])
        self.assertEqual(installation.address, payload["address"])
        import ipdb

        ipdb.set_trace()
        self.assertEqual(installation.status, payload["status"])
