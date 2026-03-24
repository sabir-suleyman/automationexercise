from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

driver = webdriver.Chrome()
driver.get("https://automationexercise.com/products")
driver.maximize_window()

time.sleep(3)

try:
    products = driver.find_elements(By.CLASS_NAME, "productinfo")

    selected_products = random.sample(products, 3)
    selected_data = []

    for product in selected_products:
        name = product.find_element(By.TAG_NAME, "p").text
        price = product.find_element(By.TAG_NAME, "h2").text
        price_int = int(price.replace("Rs. ", ""))

        selected_data.append((name, price_int))

    print("Selected Products:")
    for item in selected_data:
        print(item)

    driver.save_screenshot("figure1_products_page.png")

    all_product_cards = driver.find_elements(By.CLASS_NAME, "product-image-wrapper")

    for selected_name, selected_price in selected_data:
        found = False

        for card in all_product_cards:
            name = card.find_element(By.XPATH, ".//p").text

            if name == selected_name:
                driver.execute_script("arguments[0].scrollIntoView();", card)
                time.sleep(1)

                driver.execute_script("""
                    arguments[0].querySelector('.product-overlay').style.display = 'block';
                """, card)
                time.sleep(1)

                add_btn = card.find_element(By.XPATH, ".//a[contains(text(),'Add to cart')]")
                driver.execute_script("arguments[0].click();", add_btn)
                time.sleep(1)

                driver.find_element(By.XPATH, "//button[contains(text(),'Continue Shopping')]").click()
                time.sleep(1)

                found = True
                break

        if not found:
            raise Exception(f"Product not found: {selected_name}")

    driver.save_screenshot("figure2_selected_products_added.png")

    driver.find_element(By.XPATH, "//a[contains(text(),'Cart')]").click()
    time.sleep(3)

    driver.save_screenshot("figure3_cart_page.png")

    cart_rows = driver.find_elements(By.XPATH, "//tr[contains(@id,'product-')]")
    cart_data = []

    for row in cart_rows:
        name = row.find_element(By.XPATH, ".//td[@class='cart_description']//a").text
        price_text = row.find_element(By.XPATH, ".//td[@class='cart_price']/p").text
        price_int = int(price_text.replace("Rs. ", ""))
        quantity_text = row.find_element(By.XPATH, ".//td[@class='cart_quantity']/button").text
        quantity_int = int(quantity_text)
        total_text = row.find_element(By.XPATH, ".//td[@class='cart_total']/p").text
        total_int = int(total_text.replace("Rs. ", ""))

        cart_data.append((name, price_int, quantity_int, total_int))

    print("\nProducts in the cart:")
    for item in cart_data:
        print(item)

    selected_data_sorted = sorted(selected_data, key=lambda x: x[0])
    cart_data_sorted = sorted(cart_data, key=lambda x: x[0])

    assert len(selected_data_sorted) == len(cart_data_sorted), "The product quantities don't match!"

    for i in range(len(selected_data_sorted)):
        selected_name, selected_price = selected_data_sorted[i]
        cart_name, cart_price, cart_quantity, cart_total = cart_data_sorted[i]

        assert selected_name == cart_name, f"Name don't match: {selected_name} != {cart_name}"
        assert selected_price == cart_price, f"Price don't match: {selected_price} != {cart_price}"
        assert cart_quantity == 1, f"Quantity is incorrect: {cart_quantity} for {cart_name}"
        assert cart_total == cart_price * cart_quantity, f"The row total is incorrect: {cart_name}"

    expected_total = sum(price for _, price in selected_data_sorted)
    actual_total = sum(total for _, _, _, total in cart_data_sorted)

    assert expected_total == actual_total, f"The total is incorrect: {expected_total} != {actual_total}"

    print("\nTEST PASSED: All product names, prices, and the total price have been checked.")
    driver.save_screenshot("figure4_test_passed.png")

except Exception as e:
    print(f"\nTEST FAILED: {e}")
    driver.save_screenshot("figure_error.png")

input("\nPress ENTER to continue...")
driver.quit()
