import pandas as pd

new_data = {
    'Name': "name.get_text()",
    'Category':" url",
    'Product_details': 'product_details_container}',
    'Price': "price.get_text()",
    'Image_1': '',
    'Image_2': '',
    'Image_3': '',
    'Image_4': ''
}
# Create a DataFrame with the current data
new_product_df = pd.DataFrame([new_data])

print(new_product_df)