import re  # Import the 're' module for regular expressions
import pandas as pd  # Import the 'pandas' module for data manipulation
from datetime import datetime, timedelta  # Import 'datetime' and 'timedelta' for date operations


# Function to validate the format and value of the entered ETH price
def validate_eth_price(price_str):
    # Match the numeric part of the price using a regular expression
    match = re.match(r"(\d+(\.\d+)?).*", price_str)
    if match:  # If a valid numeric value is found
        eth_price = float(match.group(1))  # Extract and convert the number to a float
        # Check if the price is unusually high
        if eth_price > 200:
            print("⚠️ Warning: The ETH price is unusually high. Please verify if you typed it correctly.")
        return eth_price  # Return the validated price
    else:  # If the price format is invalid
        print("❌ Invalid ETH price format. Please use one of the acceptable formats.")
        return None


# Function to validate if the given wallet address is valid
def validate_wallet_address(wallet_address):
    # Check if the wallet address is 42 characters long and starts with "0x"
    if len(wallet_address) == 42 and wallet_address.startswith("0x"):
        return True
    # Print an error message if the wallet address is invalid
    print("❌ Invalid wallet address. Wallet addresses must be 42 characters long and start with '0x'.")
    return False


# Function to calculate PnL (profit/loss) for a given timeframe
def calculate_time_period_pnl(purchase_date, sale_date, purchase_price, sale_price, timeframe_days, lowest_price=None):
    # If both purchase and sale dates exist, calculate PnL
    if purchase_date and sale_date:
        # Define the end of the timeframe
        timeframe_limit = purchase_date + timedelta(days=timeframe_days)
        # If the sale occurred within the timeframe
        if purchase_date < sale_date <= timeframe_limit:
            return sale_price - purchase_price  # Calculate PnL
        # If the sale occurred outside the timeframe
        elif sale_date > timeframe_limit:
            return f"The transaction is more than {timeframe_days} days, so we can't calculate the PnL"
    # If the Punk is not sold but a lowest price is provided, calculate PnL using the lowest price
    elif purchase_date and sale_date is None and lowest_price is not None:
        return lowest_price - purchase_price
    # If no valid transaction exists in the timeframe
    return "No valid transaction within the timeframe"


# Function to process PnL calculations for a Punk
def calculate_punk_pnl(main_wallet, linked_wallets, punk_id, lowest_price, timeframes, transactions_file='wallet_transactions.xlsx'):
    try:
        # Load transaction data from the Excel file
        transactions_df = pd.read_excel(transactions_file)
        # Convert the 'Date' column to datetime format
        transactions_df['Date'] = pd.to_datetime(transactions_df['Date'])

        # Filter transactions for the given wallet and Punk ID
        punk_transactions = transactions_df[
            (transactions_df['Punk ID'] == int(punk_id)) & (transactions_df['Wallet Address'] == main_wallet)
        ].copy()

        # If no transactions are found, handle the error
        if punk_transactions.empty:
            print(f"⚠️ No transactions found for Wallet Address: {main_wallet} and Punk ID: {punk_id}")
            print(f"➡️ Using the Current Lowest Price of {lowest_price} ETH for PnL calculation.")
            print(f"✅ Final PnL: -{lowest_price} ETH")
            return

        # Print transactions related to the selected Punk ID and wallet
        print("\n📜 Transactions for the selected wallet and Punk ID:")
        print(punk_transactions[['Date', 'Role', 'Event', 'Price (ETH)']])

        # Initialize variables for purchase and sale details
        purchase_price = None
        sale_price = None
        purchase_date = None
        sale_date = None

        # Extract the first "Buyer" transaction (purchase)
        bought_transaction = punk_transactions[punk_transactions['Role'] == 'Buyer']
        if not bought_transaction.empty:  # If a purchase exists
            purchase_price = bought_transaction.iloc[0]['Price (ETH)']  # Get purchase price
            purchase_date = bought_transaction.iloc[0]['Date']  # Get purchase date

        # Extract the first "Seller" transaction (sale)
        sold_transaction = punk_transactions[punk_transactions['Role'] == 'Seller']
        if not sold_transaction.empty:  # If a sale exists
            sale_price = sold_transaction.iloc[0]['Price (ETH)']  # Get sale price
            sale_date = sold_transaction.iloc[0]['Date']  # Get sale date

        # Print the calculated PnL based on available data
        if purchase_price is not None and sale_price is not None:
            print(f"\n✅ Calculated PnL: Sale Price ({sale_price}) - Purchase Price ({purchase_price}) = {sale_price - purchase_price} ETH")
        elif purchase_price is not None and sale_price is None:
            print(f"⚠️ Punk ID {punk_id} not sold yet. Using Current Lowest Price for PnL: {lowest_price - purchase_price} ETH")
        else:
            print(f"⚠️ No valid transactions found. Using Current Lowest Price for PnL: -{lowest_price} ETH")

        # Initialize a dictionary to store PnL results for each timeframe
        results = {}
        # Calculate PnL for each requested timeframe
        for timeframe in timeframes:
            if timeframe == '3':
                results['3-day PnL'] = calculate_time_period_pnl(
                    purchase_date, sale_date, purchase_price, sale_price, 3, lowest_price
                )
            elif timeframe == '7':
                results['7-day PnL'] = calculate_time_period_pnl(
                    purchase_date, sale_date, purchase_price, sale_price, 7, lowest_price
                )
            elif timeframe == '30':
                results['30-day PnL'] = calculate_time_period_pnl(
                    purchase_date, sale_date, purchase_price, sale_price, 30, lowest_price
                )
            elif timeframe == '365':
                results['365-day PnL'] = calculate_time_period_pnl(
                    purchase_date, sale_date, purchase_price, sale_price, 365, lowest_price
                )

        # Print the PnL results
        print("\n📊 Final PnL Results by Timeframe:")
        for timeframe, pnl_value in results.items():
            print(f"  - {timeframe}: {pnl_value}")

    # Handle the case where the transactions file is not found
    except FileNotFoundError:
        print("❌ The transactions file could not be found. Please ensure 'wallet_transactions.xlsx' exists.")
    # Handle any other unexpected exceptions
    except Exception as e:
        print(f"❌ An error occurred: {e}")


# Main function to handle user inputs and start the program
def main():
    # Prompt the user to enter the main wallet address
    main_wallet = input("Enter the main Wallet Address (42 characters long): ").strip()
    if not validate_wallet_address(main_wallet):  # Validate the wallet address
        return

    # Initialize the list of linked wallets with the main wallet
    linked_wallets = [main_wallet]
    print("\nDo you want to provide additional linked wallet addresses?")
    print("1. No, proceed with main wallet only")
    print("2. Yes, provide linked addresses")
    choice = input("Enter your choice (1 or 2): ").strip()

    # If the user wants to add linked wallets, validate and append them
    if choice == '2':
        additional_addresses = input("Enter linked wallet addresses separated by commas: ").strip().split(',')
        for address in additional_addresses:
            address = address.strip()
            if validate_wallet_address(address):
                linked_wallets.append(address)

    # Prompt the user to enter the Punk ID
    punk_id = input("Enter the Punk ID: ").strip()
    if not punk_id.isdigit():  # Validate that the Punk ID is numeric
        print("❌ Invalid Punk ID. Punk IDs must be numeric.")
        return

    # Prompt the user to enter the current lowest price for the Punk
    price_str = input("Enter the Current Lowest Price (e.g., '35.99 ETH ($112,683.97 USD)'): ").strip()
    lowest_price = validate_eth_price(price_str)  # Validate the price
    if lowest_price is None:
        return

    # Prompt the user to select timeframes for PnL calculation
    timeframes = []
    print("\nSelect the timeframes for PnL calculation (choose multiple by separating with commas):")
    print("1. 3 days\n2. Weekly\n3. Monthly\n4. Yearly")
    choices = input("Enter your choices (e.g., 1,3): ").strip().split(',')

    # Map user choices to valid timeframes
    for choice in choices:
        choice = choice.strip()
        if choice == '1':
            timeframes.append('3')
        elif choice == '2':
            timeframes.append('7')
        elif choice == '3':
            timeframes.append('30')
        elif choice == '4':
            timeframes.append('365')

    if not timeframes:  # Ensure at least one timeframe is selected
        print("❌ No valid timeframes selected. Exiting.")
        return

    # Call the function to calculate PnL for the provided Punk and wallet
    calculate_punk_pnl(main_wallet, linked_wallets, punk_id, lowest_price, timeframes)


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
