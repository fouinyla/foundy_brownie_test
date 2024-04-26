from brownie_app.scripts.create_index_image import get_generated_index_image_name


get_generated_index_image_name(
    image_name="foundy_up.png",
    final_index_config=[
        {
            "price": 1,
            "total_price": 20,
        },
        {
            "price": 5,
            "total_price": 30,
        },
    ],
)
