"""
Tier 5: Architecture Challenge - Explain the Whole System (The Online Store)

Simulates the end-to-end architectural pipeline:
Customer Input -> Application -> Instructions -> Data Processing -> Stored Data -> Result/Output
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class Product:
    sku: str
    name: str
    unit_price: float
    stock_quantity: int


@dataclass
class OrderRecord:
    order_id: str
    customer_id: str
    sku: str
    quantity: int
    unit_price_at_purchase: float
    subtotal: float
    tax: float
    total: float
    shipping_address: str
    status: str
    timestamp: float


class OnlineStoreDatabase:
    """Represents the 'Stored Data' component of the architecture."""
    def __init__(self):
        self.products: Dict[str, Product] = {
            "SKU-HEADPHONES": Product(
                sku="SKU-HEADPHONES",
                name="Noise-Canceling Wireless Headphones",
                unit_price=50000.0,
                stock_quantity=10,
            ),
            "SKU-KEYBOARD": Product(
                sku="SKU-KEYBOARD",
                name="Mechanical Gaming Keyboard",
                unit_price=25000.0,
                stock_quantity=5,
            ),
        }
        self.orders: Dict[str, OrderRecord] = {}

    def get_product(self, sku: str) -> Optional[Product]:
        return self.products.get(sku)

    def persist_order(self, order: OrderRecord):
        self.orders[order.order_id] = order


class OnlineStoreApplication:
    """
    Represents the Application / Program and Instruction Execution engine.
    """
    def __init__(self, db: OnlineStoreDatabase, tax_rate: float = 0.05):
        self.db = db
        self.tax_rate = tax_rate

    def process_order_pipeline(self, customer_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the 6-stage architectural pipeline.
        """
        trace: List[str] = []

        # Stage 1: Customer Input
        trace.append("Stage 1 [Customer Input]: Received raw customer request payload.")
        customer_id = customer_input.get("customer_id")
        sku = customer_input.get("sku")
        quantity = customer_input.get("quantity", 0)
        address = customer_input.get("shipping_address")
        payment_token = customer_input.get("payment_token")

        # Stage 2: Application / Program
        trace.append("Stage 2 [Application/Program]: Routing request to checkout controller.")
        if not customer_id or not sku or quantity <= 0 or not address or not payment_token:
            return {
                "success": False,
                "error": "Validation failed: Incomplete customer input.",
                "trace": trace,
            }

        # Stage 3: Instructions (Business Rules & Availability Check)
        trace.append("Stage 3 [Instructions]: Checking product availability and pricing.")
        product = self.db.get_product(sku)
        if not product:
            return {"success": False, "error": f"Product {sku} not found.", "trace": trace}

        if product.stock_quantity < quantity:
            return {
                "success": False,
                "error": f"Insufficient inventory. Only {product.stock_quantity} available.",
                "trace": trace,
            }

        # Stage 4: Data Processing
        trace.append("Stage 4 [Data Processing]: Performing arithmetic and financial calculations.")
        unit_price = product.unit_price
        subtotal = unit_price * quantity
        tax_amount = subtotal * self.tax_rate
        total_amount = subtotal + tax_amount

        # Decrement inventory
        product.stock_quantity -= quantity
        trace.append(f"Stage 4 [Data Processing]: Deducted {quantity} units from stock.")

        # Stage 5: Stored Data
        trace.append("Stage 5 [Stored Data]: Generating immutable database order record.")
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        record = OrderRecord(
            order_id=order_id,
            customer_id=customer_id,
            sku=sku,
            quantity=quantity,
            unit_price_at_purchase=unit_price,
            subtotal=subtotal,
            tax=tax_amount,
            total=total_amount,
            shipping_address=address,
            status="CONFIRMED",
            timestamp=time.time(),
        )
        self.db.persist_order(record)

        # Stage 6: Result / Output
        trace.append("Stage 6 [Result/Output]: Constructing customer confirmation receipt.")
        output = {
            "success": True,
            "order_id": order_id,
            "product_name": product.name,
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": subtotal,
            "tax": tax_amount,
            "total_charged": total_amount,
            "shipping_to": address,
            "status": "CONFIRMED",
            "message": f"Order confirmed. Total: ${total_amount:,.2f}.",
            "trace": trace,
        }
        return output


if __name__ == "__main__":
    database = OnlineStoreDatabase()
    store = OnlineStoreApplication(database)

    order_payload = {
        "customer_id": "CUST-94821",
        "sku": "SKU-HEADPHONES",
        "quantity": 2,
        "shipping_address": "123 Innovation Boulevard, Tech City",
        "payment_token": "TOK-PAY-99124",
    }

    print("=== EXECUTING ONLINE STORE ARCHITECTURAL PIPELINE ===")
    response = store.process_order_pipeline(order_payload)

    for step in response["trace"]:
        print(f" -> {step}")

    print("\n--- Final Customer Output ---")
    print(f"Status  : {response['status']}")
    print(f"Order ID: {response['order_id']}")
    print(f"Message : {response['message']}")
    print(f"Total   : ${response['total_charged']:,.2f}")
