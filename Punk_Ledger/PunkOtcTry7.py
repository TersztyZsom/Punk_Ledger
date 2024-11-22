# Import required libraries
from web3 import Web3  # Web3.py library for interacting with Ethereum blockchain
import pandas as pd  # Library for handling data in tabular form
import datetime  # For handling dates and timestamps
import time  # For adding delays during retries
import re  # Regular expression module for parsing user input

# Infura setup
INFURA_API_KEY = "fc3f2e17f2a049e2a421c0164e0534c6"  # Infura API key for connecting to Ethereum
INFURA_URL = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"  # Infura endpoint URL for Ethereum mainnet
web3 = Web3(Web3.HTTPProvider(INFURA_URL))  # Initialize Web3 with Infura as the HTTP provider

# Load CryptoPunks contract address in checksum format
CRYPTOPUNKS_CONTRACT = web3.to_checksum_address("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb")

# Read the ABI (Application Binary Interface) for the CryptoPunks contract from a JSON file
with open("abi.json", "r") as abi_file:
    cryptopunks_abi = abi_file.read()

# Initialize the contract object using the ABI and contract address
contract = web3.eth.contract(address=CRYPTOPUNKS_CONTRACT, abi=cryptopunks_abi)

# Constants for batching events
INITIAL_BLOCK_STEP = 1000000  # Number of blocks to process in one batch initially
MIN_BLOCK_STEP = 10000  # Minimum number of blocks to process in a batch when reducing due to errors
START_BLOCK = 0  # Start from the genesis block
LATEST_BLOCK = web3.eth.block_number  # Get the latest block number on the Ethereum mainnet


def get_wallet_addresses():
    """
    Prompt the user to input wallet addresses.
    Ensure the user inputs between 1 and 10 valid Ethereum wallet addresses.
    """
    while True:
        try:
            # Ask the user to enter wallet addresses separated by commas
            addresses = input("Enter wallet addresses separated by commas (1-10 addresses): ").split(",")
            addresses = [addr.strip() for addr in addresses]  # Remove extra whitespace from input
            if len(addresses) < 1 or len(addresses) > 10:  # Ensure 1-10 addresses are entered
                raise ValueError("You must enter between 1 and 10 wallet addresses.")
            for addr in addresses:
                # Validate each address as a proper checksum Ethereum address
                if not web3.is_checksum_address(addr) or len(addr) != 42:
                    raise ValueError(f"Invalid wallet address: {addr}")
            return addresses  # Return the valid wallet addresses
        except ValueError as e:
            print(e)  # Print error message for invalid input
            print("Please enter valid Ethereum wallet addresses. Each address must be 42 characters long.")


def fetch_events_with_retries(event_type, argument_filters, from_block, to_block, block_step):
    """
    Fetch events with retries for RPC errors by dynamically reducing the block range.
    """
    events = []  # List to store fetched events
    while from_block <= to_block:  # Loop through the block range
        try:
            # Print the block range being queried
            print(f"Querying {event_type} from block {from_block} to {min(from_block + block_step, to_block)}...")
            # Prepare filter parameters
            filter_params = {
                "from_block": from_block,
                "to_block": min(from_block + block_step, to_block),
                "argument_filters": argument_filters,
            }
            # Fetch events based on the event type
            if event_type == "PunkBought":
                fetched_events = contract.events.PunkBought.create_filter(**filter_params).get_all_entries()
            else:
                raise ValueError("Unknown event type.")
            
            events.extend(fetched_events)  # Add fetched events to the list
            from_block += block_step  # Move to the next block range
        except Exception as e:
            # Handle errors and reduce block step for retry
            print(f"Error fetching {event_type}: {e}")
            if block_step > MIN_BLOCK_STEP:
                print(f"Reducing block step from {block_step} to {block_step // 10} and retrying...")
                block_step = max(MIN_BLOCK_STEP, block_step // 10)
            else:
                print(f"Retrying with block step {block_step} after 5 seconds...")
                time.sleep(5)

    return events  # Return the list of events


def fetch_wallet_events(wallet_addresses):
    """
    Fetch PunkBought events for specified wallet addresses using retries for RPC errors.
    """
    events_data = []  # List to store event details
    for wallet in wallet_addresses:  # Loop through each wallet address
        print(f"Fetching events for Wallet Address {wallet}...")

        # Fetch PunkBought events where wallet is buyer or seller
        bought_events = fetch_events_with_retries(
            "PunkBought",
            {"fromAddress": wallet},
            START_BLOCK,
            LATEST_BLOCK,
            INITIAL_BLOCK_STEP,
        ) + fetch_events_with_retries(
            "PunkBought",
            {"toAddress": wallet},
            START_BLOCK,
            LATEST_BLOCK,
            INITIAL_BLOCK_STEP,
        )

        # Process each event and extract details
        for event in bought_events:
            try:
                tx_hash = event["transactionHash"].hex()  # Transaction hash
                seller = event["args"]["fromAddress"]  # Seller address
                buyer = event["args"]["toAddress"]  # Buyer address
                punk_id = event["args"]["punkIndex"]  # Punk ID
                value = event["args"]["value"]  # Transaction value
                price = web3.from_wei(value, "ether") if value else 0  # Convert price to ETH

                # Determine the role of the wallet in the transaction
                role = "Buyer" if buyer == wallet else "Seller" if seller == wallet else "Unknown"

                block_number = event["blockNumber"]  # Block number of the transaction
                block = web3.eth.get_block(block_number)  # Fetch block details
                date = datetime.datetime.fromtimestamp(block["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp

                # Append transaction details to the list
                events_data.append({
                    "Punk ID": punk_id,
                    "Wallet Address": wallet,
                    "Event": "Bought",
                    "Role": role,
                    "Transaction Hash": tx_hash,
                    "Seller": seller,
                    "Buyer": buyer,
                    "Price (ETH)": price,
                    "Date": date
                })
            except KeyError as e:
                print(f"Error processing event for Wallet {wallet}: Missing key {e}")  # Handle missing data
            except Exception as e:
                print(f"Error processing event: {e}")  # Handle general errors

    return events_data  # Return processed events


def save_to_excel(data):
    """
    Save the collected data to an Excel file.
    """
    df = pd.DataFrame(data)  # Convert data to a Pandas DataFrame
    # Ensure correct column order
    df = df[["Punk ID", "Wallet Address", "Role", "Event", "Transaction Hash", "Seller", "Buyer", "Price (ETH)", "Date"]]
    # Sort data by Punk ID, Wallet Address, and Date
    df.sort_values(by=["Punk ID", "Wallet Address", "Date"], inplace=True)
    # Save the DataFrame to an Excel file
    df.to_excel("wallet_transactions.xlsx", index=False)
    print("Data saved to wallet_transactions.xlsx")  # Inform the user


def get_lowest_punk_price():
    """
    Prompt the user to input the current lowest CryptoPunk price in a flexible format.
    """
    while True:
        try:
            # Prompt the user for input
            user_input = input(
                "Enter the current lowest CryptoPunk price (format examples: '35.99 ETH ($112,546.85 USD)', '35.99 ETH $112,546.85 USD', '35.99 $112,546.85'): "
            )
            # Extract ETH and USD prices using regex
            match = re.match(r"(\d+\.?\d*)\s*ETH.*?(\d+\.?\d*)", user_input, re.IGNORECASE)
            if not match:
                raise ValueError("Invalid format. Please follow the examples provided.")

            eth_price = float(match.group(1))  # Extract ETH price
            usd_price = float(match.group(2))  # Extract USD price

            # Confirm if ETH price exceeds a certain threshold
            if eth_price > 200:
                confirmation = input(
                    f"The entered ETH price is {eth_price}. Are you sure you want to proceed? (yes/no): "
                ).strip().lower()
                if confirmation != "yes":
                    print("Please re-enter the correct prices.")
                    continue

            print(f"Before the data fetching, the current lowest price is: {eth_price} ETH (${usd_price:.2f} USD)")
            return eth_price, usd_price  # Return the prices
        except ValueError as e:
            print(e)  # Inform the user about invalid input
            print("Invalid input. Please enter the price in one of the supported formats.")


def main():
    """
    Main function to orchestrate fetching and saving Punk events.
    """
    wallet_addresses = get_wallet_addresses()  # Get wallet addresses from the user
    get_lowest_punk_price()  # Prompt the user for the lowest Punk price
    print("Fetching wallet events with retries for RPC errors...")
    wallet_events = fetch_wallet_events(wallet_addresses)  # Fetch wallet events
    save_to_excel(wallet_events)  # Save the events to an Excel file


if __name__ == "__main__":
    if web3.is_connected():  # Check if connected to Ethereum
        print("Connected to Ethereum Mainnet")
        main()  # Run the main function
    else:
        print("Failed to connect to Ethereum Mainnet")  # Print error if connection fails
