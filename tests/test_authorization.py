import unittest
from unittest.mock import patch
from demo.authorization import Shop, Session


class Controls(unittest.TestCase):
    def setUp(self):
        self.shop = Shop()
        self.alice = Session('alice')

    def test_owner_can_read(self):
        self.assertEqual(self.shop.get_order(self.alice, 'A-101')['owner'], 'alice')

    def test_cross_customer_read_denied(self):
        with self.assertRaises(LookupError): self.shop.get_order(self.alice, 'B-202')

    def test_missing_order_denied(self):
        with self.assertRaises(LookupError): self.shop.get_order(self.alice, 'missing')

    def test_owner_can_change_address_before_dispatch(self):
        updated = self.shop.update_delivery_address(self.alice, 'A-101', {'delivery_address': '  12 Birch Lane  '})
        self.assertEqual(updated['delivery_address'], '12 Birch Lane')
        self.assertEqual(self.shop.orders['A-101']['owner'], 'alice')

    def test_cross_customer_address_change_denied_without_mutation(self):
        before = dict(self.shop.orders['B-202'])
        with self.assertRaises(LookupError):
            self.shop.update_delivery_address(self.alice, 'B-202', {'delivery_address': '12 Birch Lane'})
        self.assertEqual(self.shop.orders['B-202'], before)

    def test_address_change_after_dispatch_denied(self):
        self.shop.orders['A-101']['status'] = 'dispatched'
        before = dict(self.shop.orders['A-101'])
        with self.assertRaises(PermissionError):
            self.shop.update_delivery_address(self.alice, 'A-101', {'delivery_address': '12 Birch Lane'})
        self.assertEqual(self.shop.orders['A-101'], before)

    def test_cannot_change_owner_status_or_role_through_address_endpoint(self):
        for extra in ({'owner':'alice'}, {'status':'processing'}, {'role':'admin'}):
            before = dict(self.shop.orders['A-101'])
            with self.assertRaises(ValueError):
                self.shop.update_delivery_address(self.alice, 'A-101', {'delivery_address':'12 Birch Lane', **extra})
            self.assertEqual(self.shop.orders['A-101'], before)

    def test_address_validation_preserves_state_on_error(self):
        for value in ('', '  ', 123, None, 'x'*201):
            before = dict(self.shop.orders['A-101'])
            with self.assertRaises(ValueError):
                self.shop.update_delivery_address(self.alice, 'A-101', {'delivery_address':value})
            self.assertEqual(self.shop.orders['A-101'], before)

    def test_customer_cannot_claim_admin_in_body(self):
        with self.assertRaises(PermissionError):
            self.shop.admin_operation(self.alice, {'role':'admin'})

    def test_admin_can_act(self):
        self.assertIn('permitted',self.shop.admin_operation(Session('operator',frozenset({'orders:admin'})), {}))

    def test_ownership_negative_tests_detect_removed_guard(self):
        with patch.object(Shop, '_owned_order', lambda self, session, oid: self.orders[oid]):
            for name in ('test_cross_customer_read_denied', 'test_cross_customer_address_change_denied_without_mutation'):
                result = unittest.TestResult(); Controls(name).run(result)
                self.assertEqual(len(result.failures),1)
                self.assertEqual(len(result.errors),0)

    def test_admin_negative_test_detects_removed_guard(self):
        with patch.object(Shop, 'admin_operation', lambda *args: 'permitted'):
            result = unittest.TestResult(); Controls('test_customer_cannot_claim_admin_in_body').run(result)
            self.assertEqual(len(result.failures),1)
            self.assertEqual(len(result.errors),0)
