import pandas as pd
import numpy as np
customers=pd.read_csv("customers.csv")
orders=pd.read_csv("orders.csv")
products=pd.read_csv("products.csv")
categories=pd.read_csv("categories.csv")
employees= pd.read_csv("employees.csv")
stores=pd.read_csv("stores.csv")
payments=pd.read_csv("payments.csv")
suppliers=pd.read_csv("suppliers.csv")
inventory=pd.read_csv("inventory.csv")
returns=pd.read_csv("returns.csv")
reviews=pd.read_csv("reviews.csv")
shipments=pd.read_csv("shipments.csv")
merged=pd.merge(orders,customers, on='Customer_ID',how='left')
merged_with_products=pd.merge(merged,products, on='Product_ID',how='left')
merged_with_category=pd.merge(merged_with_products,categories, on='Category_ID',how='left')
merged_with_employees=pd.merge(merged_with_category,employees, on='Employee_ID',how='left')
merged_with_stores=pd.merge(merged_with_employees,stores, on='Store_ID',how='left')
merged_with_payments=pd.merge(merged_with_stores,payments, on='Order_ID',how='left')
merged_with_inventory=pd.merge(merged_with_payments,inventory, on='Product_ID',how='left')
merged_with_suppliers=pd.merge(merged_with_inventory,suppliers, on='Supplier_ID',how='left')
merged_with_returns=pd.merge(merged_with_suppliers,returns, on='Order_ID',how='left')
merged_with_reviews=pd.merge(merged_with_returns,reviews, on='Order_ID',how='left')
master=pd.merge(merged_with_reviews,shipments, on='Order_ID',how='left')
master=master.drop_duplicates()
master = master.rename(columns={
    "City_x": "Customer_City",
    "City_y": "Store_City"
})

#-----------------------------------------------------------
#-----------------------------------------------------------
delivered=master[master["Delivery_Status"]=="Delivered"]
#-----------------------------------------------------------
#------Products--Delivered-----Revenue-----------
#-----------------------------------------------------------
delivered['Revenue']=delivered['Quantity']*delivered['Price']
total_revenue=delivered['Revenue'].sum()
#-----------------------------------------------------------
#-----Discount----Analysis-----------------------
#-----------------------------------------------------------
delivered['Discount_Amount']=delivered['Revenue'] * delivered['Discount'] /100
total_discount=delivered['Discount_Amount'].sum()
delivered['Net_Revenue']=delivered['Revenue'] - delivered['Discount_Amount']
net_revenue=delivered['Net_Revenue'].sum().round(2)
#-----------------------------------------------------------
#--------Total--order---Delivered--------------------------------
#-----------------------------------------------------------
total_order=delivered['Order_ID'].nunique()
#-----------------------------------------------------------
#------------Average--Revenue--From--Customers---------------------------------------
#-----------------------------------------------------------
average_order=round(net_revenue/total_order,2)
customer_city_revenue=delivered.groupby("Customer_City")["Net_Revenue"].sum()
stores_city_revenue=delivered.groupby("Store_City")["Net_Revenue"].sum()
#Revenue by category
category_revenue=delivered.groupby("Category")["Net_Revenue"].sum()
#Revenue by store
store_revenue=(
    delivered
    .groupby("Store_Name")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
)
#Revenue by supplier
supplier_revenue=delivered.groupby("Supplier_Name")["Net_Revenue"].sum()
#Monthly Revenue
delivered['Order_Date']=pd.to_datetime(delivered['Order_Date'])
delivered['Year_Month']=delivered['Order_Date'].dt.to_period('M')
monthly_revenue=delivered.groupby("Year_Month")["Net_Revenue"].sum()
#Quarterly revenue
delivered['Quarter']=delivered['Order_Date'].dt.to_period('Q')
quarterly_revenue=delivered.groupby("Quarter")["Net_Revenue"].sum()
#top 10 customers by revenue
top_customers=delivered.groupby("Customer_Name")["Net_Revenue"].sum()
top_10_customers=top_customers.nlargest(10)
#Above average spending customers
customers_revenue=delivered.groupby("Customer_Name")['Net_Revenue'].sum()
avg_customer_spendings=customers_revenue.mean()
above_avg_customers=customers_revenue[customers_revenue > avg_customer_spendings]
#Customers spending below avg
below_avg_customers=customers_revenue[customers_revenue < avg_customer_spendings]
#-----------------------------------------------------------
#-----------------------------------------------------------
#Most sold product
#-----------------------------------------------------------
#-----------------------------------------------------------
sold_product=delivered.groupby("Product_ID")["Quantity"].sum()
highest_sold_product=sold_product.nlargest(1)
#-----------------------------------------------------------
#-----------------------------------------------------------
#Top 10 products by revenue
#----------------------------------------
products_revenue=delivered.groupby("Product_ID")["Net_Revenue"].sum()
top_10_products_revenue=products_revenue.nlargest(10)
#-----------------------------------------------------------
#-----------------------------------------------------------
#Lowest selling product
lowest_sold_product=sold_product.nsmallest(1)
#-----------------------------------------------------------
#-----------------------------------------------------------
#Revenue by products
#-----------------------------------------------------------
#-----------------------------------------------------------
revenue_by_product=(
    delivered
    .groupby("Product_ID")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
)
#-----------------------------------------------------------
#Most Profitable Category
#-----------------------------------------------------------
#-----------------------------------------------------------
profitable_category=delivered.groupby("Category")["Net_Revenue"].sum()
most_profitable_category=profitable_category.nlargest(1)
#-----------------------------------------------------------
#-----------------------------------------------------------
#Least Profitable Category
least_profitable_category=profitable_category.nsmallest(1)
#-----------------------------------------------------------
#-----------------------------------------------------------
#Most Sold Category
sold_category=delivered.groupby("Category")["Quantity"].sum()
most_sold_category=sold_category.nlargest(1)
#-----------------------------------------------------------
#-----------------------------------------------------------
#Revenue by Employee
#-----------------------------------------------------------
employee_revenue=delivered.groupby("Employee_Name")["Net_Revenue"].sum()
#-----------------------------------------------------------
#Orders Handled by Employee
#-----------------------------------------------------------
employee_order=delivered.groupby("Employee_Name")["Order_ID"].nunique()
#-----------------------------------------------------------
#Best Employee
#-----------------------------------------------------------
best_employee_revenue=delivered.groupby("Employee_Name")["Net_Revenue"].sum()
best_employee_from_revenue=best_employee_revenue.nlargest(1)
best_employee_orders=delivered.groupby("Employee_Name")["Order_ID"].nunique()
best_employee_from_orders=best_employee_orders.nlargest(1)
#-----------------------------------------------------------
#-----------------------------------------------------------
# Store Analysis
#-----------------------------------------------------------
#-----------------------------------------------------------
#1)Orders by Store
#-----------------------------------------------------------
store_order=(
    delivered
    .groupby("Store_Name")["Order_ID"]
    .nunique()
    .sort_values(ascending=False)
)
#2)Best Performing Store
#-----------------------------------------------------------
best_store_revenue=delivered.groupby("Store_Name")["Net_Revenue"].sum()
best_store_from_revenue=best_store_revenue.nlargest(1)
best_store_orders=delivered.groupby("Store_Name")["Order_ID"].nunique()
best_store_from_orders=best_store_orders.nlargest(1)
#-----------------------------------------------------------
# Payment Analysis
#-----------------------------------------------------------
#-----------------------------------------------------------
#1)Most Used Payment Method
#-----------------------------------------------------------
payment=delivered["Payment_Method"].value_counts()
most_used_payment_method=payment.nlargest(1)
#2)Revenue by Payment Method
#-----------------------------------------------------------
revenue_from_pay_method=(
    delivered
    .groupby("Payment_Method")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
)
#-----------------------------------------------------------
#Returns Analysis
#-----------------------------------------------------------
#-----------------------------------------------------------
#1)Return Percentage
#-----------------------------------------------------------
returned_order=delivered["Return_ID"].notna().sum()
total_delivered_order=delivered["Order_ID"].nunique()
returned_order_rate=round(returned_order/total_delivered_order*100,2)
#2)Most Returned Product
#-----------------------------------------------------------
most_returned_product=(delivered
                       .groupby("Product_ID")["Return_ID"]
                       .count()
                       .sort_values(ascending=False)
                       )
#-----------------------------------------------------------
#Return Reason Analysis
#-----------------------------------------------------------
returned = delivered[
    delivered["Return_ID"].notna()
]

return_reason = returned["Reason"].value_counts()
#-----------------------------------------------------------
#-----------------------------------------------------------
#Reviews
#-----------------------------------------------------------
#-----------------------------------------------------------
#1)Average rating
#-----------------------------------------------------------
total_review_rating=delivered["Rating"].sum()
avg_review_rating=total_review_rating.mean().round(2)
#-----------------------------------------------------------
#2)Highest rated product
#-----------------------------------------------------------
product_rate=master.groupby("Product_ID")["Rating"].nunique()
highest_rated_product_max=product_rate.max()
highest_rated_product=product_rate[product_rate ==highest_rated_product_max]
#3)Lowest rated product
#-----------------------------------------------------------
lowest_rated_product_min=product_rate.min()
lowest_rated_product=product_rate[product_rate ==lowest_rated_product_min]
#-----------------------------------------------------------
#Inventory
#-----------------------------------------------------------
#-----------------------------------------------------------
#1) Low stock products
#-----------------------------------------------------------
low_stock_product = (
    inventory
    .sort_values("Stock")
    .head(5)
)
#-----------------------------------------------------------
#2)Inventory value
#-----------------------------------------------------------
master['Inventory_Value'] = (
    master["Stock"] *
    master["Price"]
)

total_inventory_value = master["Inventory_Value"].sum()
#-----------------------------------------------------------
#3)Supplier contribution
#-----------------------------------------------------------
supplier_inventory_value = (
    master
    .groupby("Supplier_Name")["Inventory_Value"]
    .sum()
    .sort_values(ascending=False)
)

#-----------------------------------------------------------


print(f"\n1:Total discount given: {total_discount}")
print(f"\n2:Total_revenue generated :{total_revenue}")
print(f"\n3:Total revenue after discount: {net_revenue}")
print(f"\n4:Total number of delivered orders: {total_order}")
print(f"\n5:Average revenue per order: {average_order}")
print(f"\n6:Revenue by Customer city :\n {customer_city_revenue}")
print(f"\n7:Revenue by Stores city: \n{stores_city_revenue}")
print(f"\n8:Revenue by Category : \n{category_revenue}")
print(f"\n9:Revenue by Store : \n{store_revenue}")
print(f"\n10:Revenue by Supplier : \n{supplier_revenue}")
print(f"\n11:Monthly revenue: \n{monthly_revenue}")
print(f"\n12:Quarterly revenue of a year: \n{quarterly_revenue}")
print(f"\n13:Top 10 customers: \n{top_10_customers}")
print(f"\n14:Above average revenue spending customers:\n {above_avg_customers}")
print(f"\n15:Below average revenue spending customers:\n {below_avg_customers}")
print(f"\n16:Average customers spending: {avg_customer_spendings.round(2)}")
print(f"\n17:Highest sold product: \n{highest_sold_product}")
print(f"\n18:Top 10 most sold products by revenue:\n{top_10_products_revenue}")
print(f"\n19:Lowest selling product: \n{lowest_sold_product}")
print(f"\n20:Revenue by product: \n{revenue_by_product}")
print(f"\n21:Most profitable category: \n{most_profitable_category}")
print(f"\n22:Least profitable category: \n{least_profitable_category}")
print(f"\n23:Most sold category: \n{most_sold_category}")
print(f"\n24:Revenue generated by employees: \n{employee_revenue}")
print(f"\n25:Orders handled by employees: \n{employee_order}")
print(f"\n26:Best employee from revenue: \n{best_employee_from_revenue}")
print(f"\n27:Best employee from order: \n{best_employee_from_orders}")
print(f"\n28:Stores by order: \n{store_order}")
print(f"\n29:Best  store: \n1)According to Revenue: \n{best_store_from_revenue}\n2)According to order:\n{best_store_from_orders}")
print(f"\n30:Most used payment method: \n{most_used_payment_method}")
print(f"\n31Revenue by payment method: \n{revenue_from_pay_method}")
print(f"\n32:Percentage of order returned : {returned_order_rate}")
print(f"\n33 Most returned product: \n{most_returned_product}")
print(f"\n34)Returned item reason: \n{return_reason}")
print(f"\n35)Average review rating: \n{avg_review_rating}")
print(f"\n36)Highest rated product: \n{highest_rated_product}")
print(f"\n37)Lowest rated product: \n{lowest_rated_product}")
print(f"\n38)Low stock product : \n{low_stock_product}")
print(f"\n39)Inventory value: {total_inventory_value}")
print(f"\n40)Inventory value by supplier.\n{supplier_inventory_value}")
master.to_csv("master_dataset.csv", index=False)