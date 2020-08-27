import pytest
from typing import List, Dict
from CheapestShipment import produceCheapestShipment

testCases = [
    # Order can be fulfilled with just a single warehouse
    (
        {"apple": 1},
        [{"name": "owd", "inventory": {"apple": 1}}],
        [{"owd": {"apple": 1}}],
    ),
    # Order can be fulfilled with multiple warehouses: All warehouses used
    (
        {"apple": 10},
        [
            {"name": "owd", "inventory": {"apple": 5}},
            {"name": "dm", "inventory": {"apple": 5}},
        ],
        [{"owd": {"apple": 5}}, {"dm": {"apple": 5}}],
    ),
    # Order cannot be shipped because there is not enough inventory
    ({"apple": 1}, [{"name": "owd", "inventory": {"apple": 0}}], []),
    # Order cannot be shipped because there is not enough inventory
    ({"apple": 2}, [{"name": "owd", "inventory": {"apple": 1}}], []),
    # Order cannot be shipped because the order is blank
    ({}, [{"name": "psd", "inventory": {"guava": 3, "mango": 4}}], []),
    # Order cannot be shipped because no warehouses exist
    ({"lime": 8, "peach": 5, "milk": 3}, [], []),
    # Order cannot be shipped because of invalid quantity amount
    (
        {"toothbrush": 3, "eggs": 7, "clay": -2},
        [{"name": "tmb", "inventory": {"clay": 3, "tootbrush": 4, "eggs": 9}}],
        [],
    ),
    # Order cannot be shipped because of invalid quantity amount
    (
        {"toothbrush": 3, "eggs": 7, "clay": 0},
        [{"name": "tmb", "inventory": {"clay": 3, "tootbrush": 4, "eggs": 9}}],
        [],
    ),
    # Order can be fulfilled; A combination of warehouses will
    # fulfill all item shipments
    (
        {"markers": 32, "cookies": 43, "cheese": 21},
        [
            {"name": "fmy", "inventory": {"cookies": 18, "cheese": 13}},
            {"name": "dhs", "inventory": {"markers": 25, "cheese": 8}},
            {"name": "tjs", "inventory": {"markers": 65, "cookies": 42}},
        ],
        [
            {"fmy": {"cookies": 18, "cheese": 13}},
            {"dhs": {"markers": 25, "cheese": 8}},
            {"tjs": {"markers": 7, "cookies": 25}},
        ],
    ),
    # Order can be fulfilled: Some items in one warehouse may be more
    # expensive to ship relative to the same item in other warehouses
    # even if all the other items in that warehouse are cheaper to ship
    # I wasn't sure if the problem statement allows for this scenario,
    # but I wanted to account for it just in case
    # For example, here it's cheaper to ship oranges and crayons
    # from warehouse gje than dhs but more expensive to ship
    # eggs and grapes
    (
        {"oranges": 16, "grapes": 22, "eggs": 10, "crayons": 30},
        [
            {
                "name": "gje",
                "inventory": {"crayons": 54, "cucumbers": 13, "oranges": 2},
            },
            {
                "name": "dhs",
                "inventory": {
                    "eggs": 6,
                    "spinach": 5,
                    "crayons": 30,
                    "oranges": 14,
                    "grapes": 10,
                },
            },
            {"name": "gje", "inventory": {"grapes": 32, "eggs": 100}},
        ],
        [
            {"gje": {"crayons": 30, "oranges": 2, "grapes": 12, "eggs": 4}},
            {"dhs": {"eggs": 6, "oranges": 14, "grapes": 10}},
        ],
    ),
    # Order can be fulfilled: Navigate through warehouses
    # with quantities <= 0 and only choose valid options
    (
        {"pickles": 24, "boba": 17, "cheetos": 10},
        [
            {
                "name": "frsh",
                "inventory": {"pickles": 0, "grapefruit": -5, "boba": 6, "gum": -18},
            },
            {
                "name": "hpes",
                "inventory": {
                    "eggs": 6,
                    "spinach": -592,
                    "cheetos": -10,
                    "crayons": -30,
                    "pickles": 9,
                    "oranges": 0,
                    "grapes": 5555,
                },
            },
            {
                "name": "jffy",
                "inventory": {"grapes": 32, "boba": -11, "pickles": 24, "eggs": 100},
            },
            {
                "name": "sdcm",
                "inventory": {
                    "grapes": 32,
                    "boba": 21,
                    "pickles": 24,
                    "eggs": 100,
                    "cheetos": 10,
                },
            },
        ],
        [
            {"frsh": {"boba": 6}},
            {"hpes": {"pickles": 9}},
            {"jffy": {"pickles": 15}},
            {"sdcm": {"boba": 11, "cheetos": 10}},
        ],
    ),
    # Order cannot be shipped: Blank product/item title in order
    ({"": 1}, [{"name": "owd", "inventory": {"apple": 1}}], []),
    # Order can be fulfilled: Ignore warehouses with
    # missing name or inventory keys
    # # Order can be fulfilled with multiple warehouses: All warehouses used
    (
        {"lettuce": 300},
        [
            {"inventory": {"apple": 5}},
            {"name": "dm"},
            {"name": "amx", "inventory": {"lettuce": 150}},
            {"name": "aes", "inventory": {"corrupt": -9001, "lettuce": 200}},
        ],
        [{"amx": {"lettuce": 150}}, {"aes": {"lettuce": 150}}],
    ),
]


def sortBy(x: List[Dict]) -> str:
    return list(x.keys())[0]


@pytest.mark.parametrize("order, warehouses, expectedOutput", testCases)
def test_produce_cheapest_shipment(
    order: Dict[str, int], warehouses: List[Dict], expectedOutput: List[Dict]
):

    actualOutput = produceCheapestShipment(order, warehouses)

    assert sorted(actualOutput, key=sortBy) == sorted(expectedOutput, key=sortBy)
