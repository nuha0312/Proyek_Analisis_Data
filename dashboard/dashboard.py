import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Load data
products_items_df = pd.read_csv("https://raw.githubusercontent.com/nuha0312/Dataset_Ecommerce/main/products_items_data.csv")
orders_customers_df = pd.read_csv("https://raw.githubusercontent.com/nuha0312/Dataset_Ecommerce/main/orders_customers_data.csv")
all_df = pd.merge(
    left=products_items_df,
    right=orders_customers_df,
    how="left",
    on ="order_id"
)

# Convert 'order_purchase_timestamp' to datetime
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Set 'order_purchase_timestamp' as the index
all_df.set_index('order_purchase_timestamp', inplace=True)

# Function to plot line chart for monthly orders
def plot_monthly_orders(all_df):
    # Aggregating monthly orders
    monthly_df = all_df.resample(rule='M').agg({'order_id': 'nunique'}).reset_index()
    monthly_df['order_purchase_timestamp'] = monthly_df['order_purchase_timestamp'].dt.strftime('%B')

    # Sorting DataFrame by order_id and removing duplicates
    monthly_df = monthly_df.sort_values('order_id').drop_duplicates('order_purchase_timestamp', keep='last')

    # Mapping for numeric month
    month_mapping = {month: i for i, month in enumerate(calendar.month_name[1:], start=1)}

    # Adding numeric month column and sorting DataFrame by numeric month
    monthly_df['month_numeric'] = monthly_df['order_purchase_timestamp'].map(month_mapping)
    monthly_df = monthly_df.sort_values('month_numeric').drop('month_numeric', axis=1)

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_df['order_purchase_timestamp'], monthly_df['order_id'], marker='o', linewidth=2, color='#068DA9')
    plt.title('Number of Orders per Month (2018)', loc='center', fontsize=20)
    plt.xticks(fontsize=10, rotation=25)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(plt)

# Function to plot bar chart for best and worst performing products
def plot_best_worst_products(all_df):
    # Grouping by product category and summing quantities
    sum_order_items_df = all_df.groupby("product_category_name").quantity.sum().sort_values(ascending=False).reset_index()

    # Creating bar plots for best and worst performing products
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(x="quantity", y="product_category_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Number of Sales")
    ax[0].set_title("Best Performing Products", loc="center", fontsize=15)
    ax[0].tick_params(axis ='y', labelsize=12)

    sns.barplot(x="quantity", y="product_category_name", data=sum_order_items_df.tail(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Number of Sales")
    ax[1].set_title("Worst Performing Products", loc="center", fontsize=15)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].tick_params(axis='y', labelsize=12)

    plt.tight_layout()
    st.pyplot(plt)

# Main function to run the app
def main():
    st.sidebar.header("Navigation")
    st.sidebar.title("E-Commerce Public Dataset")
    page = st.sidebar.radio("Go to", ["Monthly Orders Overview", "Product Sales Analysis"])

    if page == "Monthly Orders Overview":
        st.title("Monthly Orders Overview")
        plot_monthly_orders(all_df)
    elif page == "Product Sales Analysis":
        st.title("Product Sales Analysis")
        plot_best_worst_products(all_df)

# Running the app
if __name__ == "__main__":
    main()