"""In-memory teaching sketch. Session comes from trusted middleware, never a request body."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    subject: str
    permissions: frozenset = frozenset()


class Shop:
    def __init__(self):
        self.orders = {
            'A-101': {'owner': 'alice', 'status': 'processing', 'delivery_address': '44 Maple Street'},
            'B-202': {'owner': 'bob', 'status': 'processing', 'delivery_address': '17 Oak Road'},
        }

    def _owned_order(self, session, order_id):
        order = self.orders.get(order_id)
        if not order or order['owner'] != session.subject:
            raise LookupError('Order unavailable')
        return order

    def get_order(self, session, order_id):
        return dict(self._owned_order(session, order_id))

    def update_delivery_address(self, session, order_id, changes):
        order = self._owned_order(session, order_id)
        if order['status'] != 'processing':
            raise PermissionError('Address changes close when dispatch begins')
        if type(changes) is not dict or set(changes) != {'delivery_address'}:
            raise ValueError('Only delivery_address may be changed')
        address = changes['delivery_address']
        if not isinstance(address, str) or not 1 <= len(address.strip()) <= 200:
            raise ValueError('A nonempty delivery address of at most 200 characters is required')
        order['delivery_address'] = address.strip()
        return dict(order)

    def admin_operation(self, session, request_body):
        if 'orders:admin' not in session.permissions:
            raise PermissionError('Administrative permission required')
        return 'administrative operation permitted'
