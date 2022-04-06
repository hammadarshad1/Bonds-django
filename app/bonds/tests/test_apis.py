from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.test import APIClient as Client

from bonds import models


BOND_SELL_URL = reverse("bond:sell-list")
BOND_BUY_URL = reverse("bond:buy-list")
BOND_LIST_URL = reverse("bond:list-list")


def _create_user(data):
    return get_user_model().objects.create_user(**data)


class TestBonds(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = _create_user({
            "email": "testemail@gmail.com",
            "password": "testpass@123"
        })
        self.client.force_authenticate(self.user)

    def test_sell_bonds_api_successfully(self):
        """Test to create a sell order successfully"""
        payload = {
            "name": "Test Bond",
            "number_of_bonds": 1000,
            "selling_price": 1000.0000
        }
        res = self.client.post(BOND_SELL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["user"], self.user.id)
        self.assertEqual(res.data["number_of_bonds"], payload["number_of_bonds"])
        self.assertEqual(float(res.data["selling_price"]), payload["selling_price"])

    def test_transaction_is_creating_with_bond(self):
        payload = {
            "name": "Test Bond",
            "number_of_bonds": 1000,
            "selling_price": 1000.0000
        }
        res = self.client.post(BOND_SELL_URL, payload)

        transaction = models.Transaction.objects.last()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["id"], str(transaction.bond.id))
        self.assertEqual(
            transaction.type,
            models.Transaction.TransactionType.SELL
        )
        self.assertEqual(self.user, transaction.user)

    def test_sell_bond_api_invalid_bond_fails(self):
        """Test invalid bond value fails"""
        payload = {
            "name": "Test Bond",
            "number_of_bonds": 1000000,
            "selling_price": 1000.0000
        }
        res = self.client.post(BOND_SELL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sell_bond_api_invalid_selling_price_fails(self):
        """Test invalid selling price value fails"""
        payload = {
            "name": "Test Bond",
            "number_of_bonds": 1000000,
            "selling_price": 10000000000000.0000
        }
        res = self.client.post(BOND_SELL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_bond_successfully(self):
        """Test buy own bonds fails"""
        payload = {
            "name": "Test Bond",
            "number_of_bonds": 1000,
            "selling_price": 1000.0000
        }
        self.client.post(BOND_SELL_URL, payload)
        user = _create_user({
            "email": "fakeuser@gmail.com",
        })
        self.client.force_authenticate(user)
        bond = models.Bond.objects.last()

        res = self.client.post(BOND_BUY_URL, {
            "id": str(bond.id)
        })

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["id"], str(bond.id))

    def test_buy_own_bond_fails(self):
        """Test buy own bonds fails"""
        payload = {
            "name": "Test Bond",
            "number_of_bonds": 1000,
            "selling_price": 1000.0000
        }
        self.client.post(BOND_SELL_URL, payload)
        bond = models.Bond.objects.last()

        res = self.client.post(BOND_BUY_URL, {
            "id": str(bond.id)
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_buy_already_bought_bond_fails(self):
        """Test to buy already bought bonds fails"""
        payload = {
            "name": "Test Bond",
            "number_of_bonds": 1000,
            "selling_price": 1000.0000
        }
        self.client.post(BOND_SELL_URL, payload)
        user = _create_user({
            "email": "fakeuser@gmail.com",
        })
        self.client.force_authenticate(user)
        bond = models.Bond.objects.last()
        self.client.post(BOND_BUY_URL, {
            "id": str(bond.id)
        })

        res = self.client.post(BOND_BUY_URL, {
            "id": str(bond.id)
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_bond_api_mxn_currency_successfully(self):
        """Test to list bond api with mxn currency"""
        payload1 = {
            "name": "Test Bond",
            "number_of_bonds": 1000,
            "selling_price": 1000.0000
        }
        payload2 = {
            "name": "Test Bond 1",
            "number_of_bonds": 100,
            "selling_price": 10000.0000
        }
        payload3 = {
            "name": "Test Bond 2",
            "number_of_bonds": 10,
            "selling_price": 100000.0000
        }
        self.client.post(BOND_SELL_URL, payload1)
        self.client.post(BOND_SELL_URL, payload2)
        self.client.post(BOND_SELL_URL, payload3)

        res = self.client.get(BOND_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)
        self.assertTrue("status" in res.data[0])
        self.assertEqual(
            res.data[0]["selling_price"][-3:],
            settings.DEFAULT_CURRENCY
        )

    def test_list_bond_with_usd_currency(self):
        """Test to list bond api with USD currency"""
        payload = {
            "name": "Test Bond",
            "number_of_bonds": 1000,
            "selling_price": 1000.0000
        }

        self.client.post(BOND_SELL_URL, payload)

        res = self.client.get(BOND_LIST_URL, {"currency": "usd"})

        self.assertEqual(res.data[0]["selling_price"][-3:], "USD")
