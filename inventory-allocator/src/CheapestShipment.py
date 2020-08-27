from typing import List, Dict


def produceCheapestShipment(order: Dict[str, int],
                            warehouses: List[Dict]) -> List[Dict]:

    # This is where we will store any successful warehouse shipments
    # The reason why I chose to use a dict initially rather than a list
    # is explained on line 56 in test_cheapest_shipment.py
    # shipment: dict[str, warehouse Order]
    shipment = {}

    # Can't ship anything if nothing is in the order
    # or no warehouses exist!
    if not order or not warehouses:
        return []

    # Keeps track of the number of products fulfilled
    # by the previously explored warehouses
    productsFulfilled = 0

    # warehouse: Dict
    # product: str

    # Examine each warehouse to check if they have
    # sufficient inventory
    for warehouse in warehouses:

        # Check if this portion of the warehouse data is
        # structured/formatted properly for evaluation
        # If not, we can't use this warehouse in our analysis
        if "name" not in warehouse or "inventory" not in warehouse:
            continue

        # If we have already fulfilled the order
        # With the warehouses with the cheapest prices
        # We do not need to explore the rest of the warehouses
        if productsFulfilled == len(order.keys()):
            break

        # Check the quantity of a certain product
        # we need to ship and compare against inventory in
        # the current warehouse we're exploring
        for product in order.keys():
            # We have already fulfilled this product,
            # no need to keep exploring whether
            # warehouses have inventory for this particular product
            if not order[product]:
                continue

            # It doesn't make sense to ship a negative amount
            # of products or something with an empty label.
            # Thus, make sure to immediately return an empty list
            if not product or order[product] <= 0:
                return []

            if product in warehouse["inventory"]:
                quantityNeeded = order[product]
                quantityInWareHouse = warehouse["inventory"][product]

                # Make sure warehouse data makes sense
                # If the quantity of an item is 0 or
                # negative we can't really use that warehouse
                # to fulfill this order neither in part nor in whole
                if quantityInWareHouse <= 0:
                    continue

                merchant = warehouse["name"]
                if merchant not in shipment:
                    shipment[merchant] = {merchant: {}}

                # The warehouse does not have enough of the current
                # product to completely fulfill this part of the order
                # Simply take all of the stock of the product in the warehouse
                # to partially fulfill this part of the order
                if quantityInWareHouse < quantityNeeded:
                    shipment[merchant][merchant][product] = quantityInWareHouse
                    order[product] -= quantityInWareHouse
                else:  # quantityInWarehouse >= quantityNeeded

                    # This part of the order can be completely fulfilled
                    shipment[merchant][merchant][product] = quantityNeeded

                    # Use None value as a marker that we found enough
                    # stock already to fulfill this part of the order
                    order[product] = None

                    productsFulfilled += 1

    # Check whether the order was fulfilled completely
    if productsFulfilled == len(order.keys()):
        return [shipment[merchant] for merchant in shipment]
    else:

        # The warehouses did not have all the products and quantities to
        # completely fufill the order
        return []
