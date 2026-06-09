from exercises.pipeline import paid_sales, Orders, above_threshold

reported_orders = []

if __name__ == '__main__':
    with open('./data/orders.csv') as f:
        next(f) # skip the header
        orders = Orders(f)
        paid_orders = paid_sales(orders)
        above_threshold_orders = above_threshold(paid_orders, threshold=5500)
        reported_orders = list(above_threshold_orders)
        for order in above_threshold_orders:
             print(order)