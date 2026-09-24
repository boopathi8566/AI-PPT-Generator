from ppt_generator import create_presentation


test_data = {
    "title": "Food Delivery System",
    "slides": [
        {
            "slide_number": 1,
            "title": "Introduction",
            "content": [
                "Food delivery connects customers with restaurants",
                "Orders can be placed through mobile or web apps",
                "Customers can receive food at their location"
            ]
        },
        {
            "slide_number": 2,
            "title": "Key Features",
            "content": [
                "Restaurant browsing",
                "Online ordering",
                "Digital payments",
                "Order tracking"
            ]
        }
    ]
}


create_presentation(
    test_data,
    "test_presentation.pptx"
)

print("PPT created successfully!")